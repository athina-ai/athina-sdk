import requests
from magik.internal_logger import logger
from magik.utils import substitute_vars
from magik.openai_helper import OpenAI
from magik.test_loader import TestLoader
from magik.config import get_open_ai_default_model, get_magik_api_key
from magik.constants import RUN_URL
from magik.metrics import calculate_flakiness_index
from magik.types.test_run import (
    Test,
    TestRunStats,
    TestRunDetails,
    TestRunResult,
    TestSuiteResults,
    EvalResult,
    IndividualTestRunResult,
)
from magik.run_logger import log_test_suite_results, log_test_run
from typing import TypedDict, Any, List, Dict, Optional


# This class is responsible for running tests
class Run:
    def __init__(self, test_dir: str, test_runs_dir: str):
        self.saved_prompt_response = ""
        self.test_loader = TestLoader(test_dir=test_dir)
        self.test_runs_dir = test_runs_dir

    def run_tests(self, test_name: str, response=None, number_of_runs=1):
        test_context = self.test_loader._load_context(test_name)
        test_suite = self.test_loader._load_test_suite(
            test_name, test_context=test_context
        )
        raw_prompt = self.test_loader._load_prompt(test_name)
        log_file_path = self._log_file_path()
        if response:
            self._run_tests_for_prompt_response(
                test_suite=test_suite,
                raw_prompt=raw_prompt,
                prompt_response=response,
                log_file_path=log_file_path,
                number_of_runs=number_of_runs,
            )
        else:
            self._run_tests_for_prompt(
                test_suite=test_suite,
                raw_prompt=raw_prompt,
                log_file_path=log_file_path,
                number_of_runs=number_of_runs,
            )

    def run_tests_in_prod(self, start_date, end_date, prompt_slug, test_slug):
        request_data = {
            "source": "CLI",
            "start_date": start_date,
            "end_date": end_date,
            "prompt_tests": [
                {
                    "prompt_slug": prompt_slug,
                    "test_slugs": "*" if test_slug == "*" else test_slug.split(","),
                }
            ],
        }
        # Remove None fields from the payload
        payload = {k: v for k, v in request_data.items() if v is not None}

        logger.debug(f"Sending request to {RUN_URL} with data: {request_data}\n")
        response = requests.post(
            RUN_URL,
            json=payload,
            headers={
                "magik-api-key": get_magik_api_key(),
            },
        )
        if response.status_code != 200:
            logger.error(f"ERROR: Failed to trigger test in prod: {response.text}")
            return

    def _calculate_test_run_stats(self, test_suite_result_stats: TestSuiteResults):
        for _, test_run_result in test_suite_result_stats.items():
            # calculate percentage pass / fail for each test
            stats = test_run_result["run_stats"]
            for test_run_instance in test_run_result["run_details"]:
                if test_run_instance["result"] == None:
                    stats["error"] += 1
                elif test_run_instance["result"]:
                    stats["passed"] += 1
                else:
                    stats["failed"] += 1

            number_of_successful_runs = stats["passed"] + stats["failed"]
            if number_of_successful_runs > 0:
                pass_rate_percentage: float = round(
                    (stats["passed"] / number_of_successful_runs) * 100, 2
                )
                stats["pass_rate"] = pass_rate_percentage
                stats["flakiness"] = calculate_flakiness_index(pass_rate_percentage)

    def _run_tests_for_prompt(
        self, test_suite: list, raw_prompt: str, log_file_path: str, number_of_runs: int
    ):
        # Use this object to store the stats for each test
        test_suite_results = self._initialize_test_suite_result(test_suite)

        # Run the tests for the specified number of runs
        for test in test_suite:
            for _ in range(number_of_runs):
                test_run_result = self._run_individual_test_for_prompt(
                    test=test,
                    raw_prompt=raw_prompt,
                    log_file_path=log_file_path,
                )
                test_suite_results[test["description"]]["run_details"].append(
                    test_run_result["run_details"]
                )

        self._calculate_test_run_stats(test_suite_results)
        log_test_suite_results(test_suite_results)

    def _run_tests_for_prompt_response(
        self,
        test_suite: list,
        raw_prompt: str,
        prompt_response: str,
        log_file_path: str,
        number_of_runs: int,
    ):
        # Use this object to store the stats for each test
        test_suite_results = self._initialize_test_suite_result(test_suite)

        for test in test_suite:
            for _ in range(number_of_runs):
                test_run_result = self._run_individual_test_for_prompt_response(
                    test=test,
                    prompt=raw_prompt,
                    prompt_response=prompt_response,
                    log_file_path=log_file_path,
                )
                test_suite_results[test["description"]]["run_details"].append(
                    test_run_result["run_details"]
                )

        self._calculate_test_run_stats(test_suite_results)
        log_test_suite_results(test_suite_results)

    def _run_individual_test_for_prompt(
        self, test: Test, raw_prompt: str, log_file_path: str
    ) -> IndividualTestRunResult:
        openai = OpenAI()
        prompt_vars = test["prompt_vars"]
        model = get_open_ai_default_model()
        if len(prompt_vars) == 0:
            prompt = raw_prompt
            if len(self.saved_prompt_response) == 0:
                self.saved_prompt_response = openai.openai_chat_completion_message(
                    model=model, prompt=prompt
                )
            prompt_response = self.saved_prompt_response
        else:
            prompt = substitute_vars(raw_prompt, prompt_vars)
            prompt_response = openai.openai_chat_completion_message(
                model=model, prompt=prompt
            )

        return self._run_individual_test_for_prompt_response(
            test=test,
            prompt=prompt,
            prompt_response=prompt_response,
            log_file_path=log_file_path,
        )

    def _run_individual_test_for_prompt_response(
        self, test: Test, prompt: str, prompt_response: str, log_file_path: str
    ) -> IndividualTestRunResult:
        eval_result = test["eval"](prompt_response)
        individual_test_run_result = self._generate_test_run_result(
            test=test,
            eval_result=eval_result,
            prompt=prompt,
            prompt_response=prompt_response,
        )

        log_test_run(
            individual_test_run_result=individual_test_run_result,
            log_file_path=log_file_path,
        )

        return individual_test_run_result

    def _generate_test_object(self, test: Test) -> Test:
        test_function_name = test["eval"].__name__
        return {
            "description": test["description"],
            "eval": test_function_name,
            "prompt_vars": test["prompt_vars"],
            "failure_labels": test["failure_labels"],
        }

    def _generate_test_run_result(
        self, test: Test, eval_result: EvalResult, prompt, prompt_response
    ) -> IndividualTestRunResult:
        did_test_pass = eval_result["result"]
        eval_result_reason = eval_result["reason"]
        failure_labels = test["failure_labels"] if not did_test_pass else []
        return {
            "test": self._generate_test_object(test),
            "prompt": prompt,
            "prompt_response": prompt_response,
            "run_details": {
                "result": did_test_pass,
                "reason": eval_result_reason,
                "failure_labels": failure_labels,
            },
        }

    def _log_file_path(self):
        log_file_path = f"{self.test_runs_dir}/log.txt"
        return log_file_path

    def _initialize_test_suite_result(self, test_suite: List[Test]) -> TestSuiteResults:
        # Use this object to store the stats for each test
        test_suite_results: TestSuiteResults = {}
        for test in test_suite:
            test_suite_results[test["description"]] = {
                "test": self._generate_test_object(test),
                "prompt": "",
                "prompt_response": "",
                "run_stats": {
                    "number_of_runs": 0,
                    "passed": 0,
                    "failed": 0,
                    "error": 0,
                    "pass_rate": None,
                    "flakiness": None,
                    "runtime": None,
                },
                "run_details": [],
            }
        return test_suite_results

import os
import requests
import sys
import importlib.util
from datetime import datetime
from magik.internal_logger import logger
from magik.utils import substitute_vars
from magik.openai_helper import OpenAI
from magik.sys_exec import read_from_file, create_file
from magik.config import get_open_ai_default_model, get_magik_api_key
from magik.constants import RUN_URL


class Run:
    def __init__(self, test_dir, test_runs_dir):
        self.saved_prompt_response = ""
        self.test_dir = test_dir
        self.test_runs_dir = test_runs_dir

    def run_tests(self, test_name, response):
        test_context = self._load_context(test_name)
        tests = self._load_tests(test_name, test_context=test_context)
        raw_prompt = self._load_prompt(test_name)
        log_file_path = self._log_file_path()
        if response:
            self._run_tests_for_prompt_response(
                tests=tests, raw_prompt=raw_prompt, prompt_response=response, log_file_path=log_file_path
            )
        else:
            self._run_tests_for_prompt(
                tests=tests, raw_prompt=raw_prompt, log_file_path=log_file_path
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

        logger.debug(
            f"Sending request to {RUN_URL} with data: {request_data}\n")
        response = requests.post(
            RUN_URL,
            json=payload,
            headers={
                "magik-api-key": get_magik_api_key(),
            },
        )
        if response.status_code != 200:
            logger.error(
                f"ERROR: Failed to trigger test in prod: {response.text}")
            return

    def _run_tests_for_prompt(self, tests, raw_prompt, log_file_path):
        self._log_to_file_and_console("---------------")
        self._log_to_file_and_console("TEST RESULTS")
        self._log_to_file_and_console("---------------")
        self._log_to_file_and_console("\n")

        num_tests_passed = 0
        for test in tests:
            test_result_obj = self._run_individual_test_for_prompt(
                test=test, raw_prompt=raw_prompt, log_file_path=log_file_path
            )
            if test_result_obj["test_result"]["result"]:
                num_tests_passed += 1

        num_tests_failed = len(tests) - num_tests_passed

        logger.info("\n------------")
        if num_tests_passed == len(tests):
            logger.info("✅ All tests passed")
            logger.info("\n\n")
        else:
            logger.info(
                f"""
    ✅ {num_tests_passed}/{len(tests)} tests passed
    ❌ {num_tests_failed}/{len(tests)} tests failed
            """
            )

    def _run_tests_for_prompt_response(self, tests, raw_prompt, prompt_response, log_file_path):
        self._log_to_file_and_console("---------------")
        self._log_to_file_and_console("TEST RESULTS")
        self._log_to_file_and_console("---------------")
        self._log_to_file_and_console("\n")

        num_tests_passed = 0
        for test in tests:
            test_result_obj = self._run_individual_test_for_prompt_response(
                test=test, prompt=raw_prompt, prompt_response=prompt_response, log_file_path=log_file_path
            )
            if test_result_obj["test_result"]["result"]:
                num_tests_passed += 1

        num_tests_failed = len(tests) - num_tests_passed

        logger.info("\n------------")
        if num_tests_passed == len(tests):
            logger.info("✅ All tests passed")
            logger.info("\n\n")
        else:
            logger.info(
                f"""
    ✅ {num_tests_passed}/{len(tests)} tests passed
    ❌ {num_tests_failed}/{len(tests)} tests failed
            """
            )

    def _run_individual_test_for_prompt(self, test, raw_prompt, log_file_path):
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
        self, test, prompt, prompt_response, log_file_path
    ):
        test_function_result_obj = test["eval"](prompt_response)
        result_obj = self._generate_result_object(
            test=test,
            test_result=test_function_result_obj,
            prompt=prompt,
            prompt_response=prompt_response,
        )

        self._log_results(
            result_obj,
            log_file_path=log_file_path,
        )

        return result_obj

    def _load_prompt(self, test_name):
        test_file_path = f"{self.test_dir}/{test_name}/prompt.txt"
        absolute_path = os.path.abspath(test_file_path)
        return read_from_file(absolute_path)

    def _load_attr_from_test_file(self, test_name, attr_name, default_value=None):
        test_file_path = f"{self.test_dir}/{test_name}/assertions.py"
        # Get the absolute path by resolving against the current working directory
        absolute_path = os.path.abspath(test_file_path)

        # Get the directory path and module name from the absolute path
        directory, module_name = os.path.split(absolute_path)
        module_name = os.path.splitext(module_name)[0]

        # Load the module dynamically
        spec = importlib.util.spec_from_file_location(
            module_name, absolute_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Access the `tests` array from the module
        return getattr(module, attr_name, default_value)

    def _load_define_tests_fn(self, test_name):
        return self._load_attr_from_test_file(
            test_name=test_name, attr_name="define_tests", default_value=lambda _: []
        )

    def _load_context(self, test_name):
        return self._load_attr_from_test_file(
            test_name=test_name, attr_name="test_context", default_value=None
        )

    def _load_tests(self, test_name, test_context):
        define_tests_fn = self._load_define_tests_fn(test_name)
        return define_tests_fn(test_context)

    def _generate_test_object(self, test):
        test_function_name = test["eval"].__name__
        return {
            **test,
            "eval": test_function_name,
        }

    def _generate_result_object(self, test, test_result, prompt, prompt_response):
        did_test_pass = test_result["result"]
        failure_labels = test["failure_labels"] if not did_test_pass else []
        return {
            "test": self._generate_test_object(test),
            "test_result": test_result,
            "prompt": prompt,
            "prompt_response": prompt_response,
            "failure_labels": failure_labels,
        }

    def _log_results(self, result_obj, log_file_path=None):
        sys.stdout.flush()  # Flush the stdout buffer to ensure immediate printing to the console
        test_description = result_obj["test"]["description"]
        if log_file_path is not None:
            create_file(log_file_path)
            with open(log_file_path, "a") as log_file:
                self._log_to_file_and_console(
                    f"Test: {test_description}", log_file, color="cyan"
                )
                self._log_to_file_and_console(f"-----", log_file, color="cyan")
                self._log_prompt_results(result_obj, log_file)
                self._log_test_results(result_obj, log_file)
        else:
            self._log_to_file_and_console(
                f"Test: {test_description}", color="cyan")
            self._log_to_file_and_console(f"-----", color="cyan")
            self._log_prompt_results(result_obj)
            self._log_test_results(result_obj)

    def _log_to_file_and_console(self, output, log_file=None, color=None):
        if log_file is not None:
            log_file.write(output + "\n")
            log_file.flush()  # Ensure immediate writing to the file

        if color is not None:
            logger.log_with_color(output, color)
        else:
            logger.info(output)

    def _log_prompt_results(self, result_obj, log_file=None):
        prompt = result_obj["prompt"]
        prompt_response = result_obj["prompt_response"]
        self._log_to_file_and_console(f"Prompt: {prompt}\n", log_file)
        self._log_to_file_and_console(
            f"Prompt Response: {prompt_response}\n", log_file)

    def _log_test_results(self, result_obj, log_file=None):
        test_function_result_bool = result_obj["test_result"]["result"]
        test_result_str = "✅ Passed" if test_function_result_bool else "❌ Failed"
        test_result_reason = result_obj["test_result"]["reason"]
        failure_labels = result_obj["failure_labels"]

        self._log_to_file_and_console(
            f"Test Result: {test_result_str}", log_file)
        self._log_to_file_and_console(
            f"Reason: {test_result_reason}", log_file)
        self._log_to_file_and_console(
            f"Failure Labels: {failure_labels}", log_file)
        self._log_to_file_and_console("\n", log_file)

    def _log_file_path(self):
        log_file_path = f"{self.test_runs_dir}/log.txt"
        return log_file_path

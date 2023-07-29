import sys
from typing import Optional
from .types.test_run import TestSuiteResults, IndividualTestRunResult
from .internal_logger import logger
from .sys_exec import create_file


def log_test_suite_results(test_suite_result_stats: TestSuiteResults):
    logger.to_file_and_console("---------------")
    logger.to_file_and_console("TEST RESULTS")
    logger.to_file_and_console("---------------\n")

    for test_name, test_run_result in test_suite_result_stats.items():
        stats = test_run_result["run_stats"]
        logger.info(f"{test_name}:")
        logger.info(f" ✅ {stats['passed']} passed")
        logger.info(f" ❌ {stats['failed']} failed")
        logger.info(f" ! {stats['error']} error")
        logger.info(f" Pass Rate: {stats['pass_rate']}%")
        logger.info(f" Flake Rate: {stats['flakiness']}%")
        logger.info("")


def log_test_run(
    individual_test_run_result: IndividualTestRunResult,
    log_file_path: Optional[str] = None,
):
    sys.stdout.flush()  # Flush the stdout buffer to ensure immediate printing to the console
    test_description = individual_test_run_result["test"]["description"]
    if log_file_path is not None:
        create_file(log_file_path)
        with open(log_file_path, "a") as log_file:
            logger.to_file_and_console(
                f"Test: {test_description}", log_file, color="cyan"
            )
            logger.to_file_and_console(f"-----", log_file, color="cyan")
            _log_prompt_results(
                individual_test_run_result=individual_test_run_result,
                log_file=log_file,
            )
            _log_test_results(
                individual_test_run_result=individual_test_run_result,
                log_file=log_file,
            )
    else:
        logger.to_file_and_console(f"Test: {test_description}", color="cyan")
        logger.to_file_and_console(f"-----", color="cyan")
        _log_prompt_results(individual_test_run_result=individual_test_run_result)
        _log_test_results(individual_test_run_result=individual_test_run_result)


def _log_prompt_results(
    individual_test_run_result: IndividualTestRunResult, log_file=None
):
    prompt = individual_test_run_result["prompt"]
    prompt_response = individual_test_run_result["prompt_response"]
    logger.to_file_and_console(f"Prompt: {prompt}\n", log_file)
    logger.to_file_and_console(f"Prompt Response: {prompt_response}\n", log_file)


def _log_test_results(
    individual_test_run_result: IndividualTestRunResult, log_file=None
):
    test_function_result_bool = individual_test_run_result["run_details"]["result"]
    test_result_str = "✅ Passed" if test_function_result_bool else "❌ Failed"
    test_result_reason = individual_test_run_result["run_details"]["reason"]
    failure_labels = individual_test_run_result["run_details"]["failure_labels"]

    logger.to_file_and_console(f"Test Result: {test_result_str}", log_file)
    logger.to_file_and_console(f"Reason: {test_result_reason}", log_file)
    logger.to_file_and_console(f"Failure Labels: {failure_labels}", log_file)
    logger.to_file_and_console("\n", log_file)


def _log_test_suite_results_as_csv(test_suite: TestSuiteResults, csv_file_path):
    logger.info("Logging file to CSV: " + csv_file_path)
    with open(csv_file_path, "w") as csv_file:
        logger.to_file(
            "description,prompt,response,number_of_runs,passed,failed,error,pass_rate,flakiness,runtime",
            csv_file,
        )
        for _, test_run_result in test_suite.items():
            test_description = test_run_result["test"]["description"]
            prompt = test_run_result["prompt"]
            prompt_response = test_run_result["prompt_response"]
            test_run_stats = test_run_result["run_stats"]
            passed = test_run_stats["passed"]
            failed = test_run_stats["failed"]
            error = test_run_stats["error"]
            pass_rate = test_run_stats["pass_rate"]
            flakiness = test_run_stats["flakiness"]
            number_of_runs = test_run_stats["number_of_runs"]
            runtime = test_run_stats["runtime"]

            logger.to_file(
                ""
                + str(test_description)
                + ","
                + str(prompt)
                + ","
                + str(prompt_response)
                + ","
                + str(number_of_runs)
                + ","
                + str(passed)
                + ","
                + str(failed)
                + ","
                + str(error)
                + ","
                + str(pass_rate)
                + ","
                + str(flakiness)
                + ","
                + str(runtime)
                + "",
                csv_file,
            )

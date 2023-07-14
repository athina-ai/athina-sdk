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
from magik.constants import TESTRUNS_DIR, TEST_DIR, RUN_URL


def run_tests(test_name):
    tests = _load_tests(test_name)
    raw_prompt = _load_prompt(test_name)
    log_file_path = _log_file_path(test_name)
    _run_tests_for_prompt(test_name, tests, raw_prompt, log_file_path=log_file_path)


def run_tests_in_prod(start_date, end_date, prompt_slug):
    request_data = {
        "source": "CLI",
        "startDate": start_date,
        "endDate": end_date,
        "promptSlug": prompt_slug,
    }
    print(f"Sending request to {RUN_URL} with data: {request_data}")
    requests.post(
        RUN_URL,
        json=request_data,
        headers={
            "magik-api-key": get_magik_api_key(),
        },
    )


def _run_tests_for_prompt(test_name, tests, raw_prompt, log_file_path):
    _log_to_file_and_console("---------------")
    _log_to_file_and_console("TEST RESULTS")
    _log_to_file_and_console("---------------")
    _log_to_file_and_console("\n")

    num_tests_passed = 0
    for test in tests:
        test_result = _run_individual_test_for_prompt(
            test_name, test, raw_prompt, log_file_path
        )
        if test_result:
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


def _run_individual_test_for_prompt(test_name, test, raw_prompt, log_file_path):
    openai = OpenAI()
    prompt = substitute_vars(raw_prompt, test["prompt_vars"])
    model = get_open_ai_default_model()
    prompt_response = openai.openai_chat_completion_message(model=model, prompt=prompt)
    return _run_individual_test_for_prompt_response(
        test_name, test, prompt, prompt_response, log_file_path=log_file_path
    )


def _run_individual_test_for_prompt_response(
    test_name, test, prompt, prompt_response, log_file_path
):
    test_function_result_obj = test["eval_function"](
        prompt_response, *test["eval_function_args"]
    )
    result_obj = _generate_result_object(
        test=test,
        test_result=test_function_result_obj,
        prompt=prompt,
        prompt_response=prompt_response,
    )

    _log_results(
        result_obj,
        log_file_path=log_file_path,
    )

    return result_obj["test_result"]["result"]


def _load_prompt(test_name):
    test_file_path = f"{TEST_DIR}/{test_name}/prompt.txt"
    absolute_path = os.path.abspath(test_file_path)
    return read_from_file(absolute_path)


def _load_tests(test_name):
    test_file_path = f"{TEST_DIR}/{test_name}/assertions.py"
    # Get the absolute path by resolving against the current working directory
    absolute_path = os.path.abspath(test_file_path)

    # Get the directory path and module name from the absolute path
    directory, module_name = os.path.split(absolute_path)
    module_name = os.path.splitext(module_name)[0]

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location(module_name, absolute_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Access the `tests` array from the module
    return getattr(module, "tests", [])


def _generate_result_object(test, test_result, prompt, prompt_response):
    did_test_pass = test_result["result"]
    failure_labels = test["failure_labels"] if not did_test_pass else []
    test_function_name = test["eval_function"].__name__
    return {
        "test": {
            **test,
            "eval_function": test_function_name,
        },
        "test_result": test_result,
        "prompt": prompt,
        "prompt_response": prompt_response,
        "failure_labels": failure_labels,
    }


def _log_results(result_obj, log_file_path=None):
    sys.stdout.flush()  # Flush the stdout buffer to ensure immediate printing to the console
    if log_file_path is not None:
        create_file(log_file_path)
        with open(log_file_path, "a") as log_file:
            _log_prompt_results(result_obj, log_file)
            _log_test_results(result_obj, log_file)
    else:
        _log_prompt_results(result_obj)
        _log_test_results(result_obj)


def _log_to_file_and_console(output, log_file=None):
    if log_file is not None:
        log_file.write(output + "\n")
        log_file.flush()  # Ensure immediate writing to the file
    logger.info(output)


def _log_prompt_results(result_obj, log_file=None):
    prompt = result_obj["prompt"]
    prompt_response = result_obj["prompt_response"]
    _log_to_file_and_console(f"Prompt: {prompt}", log_file)
    _log_to_file_and_console(f"Prompt Response: {prompt_response}", log_file)


def _log_test_results(result_obj, log_file=None):
    test_description = result_obj["test"]["description"]
    test_function_result_bool = result_obj["test_result"]["result"]
    test_result_str = "✅ Passed" if test_function_result_bool else "❌ Failed"
    test_result_reason = result_obj["test_result"]["reason"]
    failure_labels = result_obj["failure_labels"]

    _log_to_file_and_console(f"Test: {test_description}", log_file)
    _log_to_file_and_console(f"Test Result: {test_result_str}", log_file)
    _log_to_file_and_console(f"Reason: {test_result_reason}", log_file)
    _log_to_file_and_console(f"Failure Labels: {failure_labels}", log_file)
    _log_to_file_and_console("\n", log_file)


def _log_file_path(test_name):
    current_timestamp = datetime.now()
    formatted_timestamp = current_timestamp.strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = f"{TESTRUNS_DIR}/{test_name}/{formatted_timestamp}.txt"
    return log_file_path

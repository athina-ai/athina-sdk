import os
import importlib.util
from magik_prompt_sdk.logger import logger
from magik_prompt_sdk.utils import normalize_output_string, substitute_vars
from magik_prompt_sdk.openai import OpenAI
from magik_prompt_sdk.sys_exec import read_from_file
from magik_prompt_sdk.config import get_open_ai_api_key, get_open_ai_default_model


def run_tests(test_name):
    tests = _load_tests(test_name)
    raw_prompt = _load_prompt(test_name)
    _run_tests_for_prompt(tests, raw_prompt)


def _run_tests_for_prompt(tests, raw_prompt):
    logger.info("---------------")
    logger.info("TEST RESULTS")
    logger.info("---------------")
    logger.info("\n")

    num_tests_passed = 0
    for test in tests:
        test_result = _run_individual_test_for_prompt(test, raw_prompt)
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


def _run_individual_test_for_prompt(test, raw_prompt):
    openai = OpenAI()
    prompt = substitute_vars(raw_prompt, test["vars"])
    model = get_open_ai_default_model()
    prompt_response = openai.openai_chat_completion_message(model=model, prompt=prompt)
    return _run_individual_test_for_prompt_response(test, prompt, prompt_response)


def _run_individual_test_for_prompt_response(test, prompt, prompt_response):
    test_function_result_obj = test["eval_function"](prompt_response, *test["args"])
    result_obj = _generate_result_object(
        test=test,
        test_result=test_function_result_obj,
        prompt=prompt,
        prompt_response=prompt_response,
    )

    _log_results(result_obj)

    return result_obj["test_result"]["result"]


def _load_prompt(test_name):
    test_file_path = f"./magik_tests/{test_name}/prompt.txt"
    absolute_path = os.path.abspath(test_file_path)
    return read_from_file(absolute_path)


def _load_tests(test_name):
    test_file_path = f"./magik_tests/{test_name}/assertions.py"
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
    return {
        "test": test,
        "test_result": test_result,
        "prompt": prompt,
        "prompt_response": prompt_response,
        "failure_labels": failure_labels,
    }


def _log_results(result_obj):
    _print_prompt_results(result_obj)
    _print_test_results(result_obj)


def _print_prompt_results(result_obj):
    prompt = result_obj["prompt"]
    prompt_response = result_obj["prompt_response"]
    logger.info(f"Prompt: {prompt}")
    logger.info(f"Prompt Response: {prompt_response}")


def _print_test_results(result_obj):
    test_description = result_obj["test"]["name"]
    test_function_result_bool = result_obj["test_result"]["result"]
    test_result_str = "✅ Passed" if test_function_result_bool else "❌ Failed"
    test_result_reason = result_obj["test_result"]["reason"]
    failure_labels = result_obj["failure_labels"]

    logger.info(f"Test: {test_description}")
    logger.info(f"Test Result: {test_result_str}")
    logger.info(f"Reason: {test_result_reason}")
    logger.info(f"Failure Labels: {failure_labels}")
    logger.info("\n")

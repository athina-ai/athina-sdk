import os
import importlib.util
from magik_prompt_sdk.logger import logger
from magik_prompt_sdk.utils import normalize_output_string, substitute_vars
from magik_prompt_sdk.openai import OpenAI
from magik_prompt_sdk.constants import OPEN_AI_API_KEY, OPEN_AI_DEFAULT_MODEL
from magik_prompt_sdk.sys_exec import read_from_file


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
    openai = OpenAI(OPEN_AI_API_KEY)
    prompt = substitute_vars(raw_prompt, test["vars"])
    prompt_response = openai.openai_chat_completion_message(
        model=OPEN_AI_DEFAULT_MODEL, prompt=prompt
    )
    return _run_individual_test_for_prompt_response(test, prompt, prompt_response)


def _run_individual_test_for_prompt_response(test, prompt, prompt_response):
    _print_prompt_results(prompt, prompt_response)
    test_description = test["name"]
    test_function_result = test["eval_function"](prompt_response, *test["args"])
    test_function_result_bool = test_function_result["result"]
    test_passed = "✅ Passed" if test_function_result["result"] else "❌ Failed"
    test_result_reason = test_function_result["reason"]

    logger.info(f"Test: {test_description}")
    logger.info(f"Test Result: {test_passed}")
    logger.info(f"Reason: {test_result_reason}")
    logger.info("\n")

    if test_function_result_bool:
        return True


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


def _print_prompt_results(prompt, prompt_response):
    logger.info(f"Prompt: {prompt}")
    logger.info(f"Prompt Response: {prompt_response}")

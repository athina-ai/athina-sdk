import os
import importlib.util
from magik_prompt_sdk.logger import logger
from magik_prompt_sdk.utils import normalize_output_string
from magik_prompt_sdk.openai import OpenAI
from magik_prompt_sdk.constants import OPEN_AI_API_KEY, OPEN_AI_DEFAULT_MODEL


def run_test(test_name):
    # initialize OpenAI
    openai = OpenAI(OPEN_AI_API_KEY)

    tests = load_tests(test_name)

    # Get the prompt and output from the test
    prompt = "Tranlate this to French: Hello World"
    output = openai.openai_chat_completion_message(
        model=OPEN_AI_DEFAULT_MODEL, prompt=prompt
    )

    # Normalize the output of the prompt response
    normalized_output = normalize_output_string(output)

    # Output prompt results
    logger.info("---------------")
    logger.info("PROMPT RESULTS")
    logger.info("---------------")
    logger.info("\n")
    logger.info(f"Prompt: {prompt}")
    logger.info(f"Prompt Response: {output}")
    logger.info(f"Normalized Response: {normalized_output}")

    # output test results
    logger.info("\n")
    logger.info("---------------")
    logger.info("TEST RESULTS")
    logger.info("---------------")
    logger.info("\n")

    num_tests_passed = 0
    for index, test in enumerate(tests):
        test_name = test["name"]
        test_function_result = test["eval_function"](normalized_output, *test["args"])
        test_function_result_bool = test_function_result["result"]
        test_passed = "✅ Passed" if test_function_result["result"] else "❌ Failed"
        test_result_reason = test_function_result["reason"]

        if test_function_result_bool:
            num_tests_passed += 1

        logger.info(f"Test Case {index}: {test['name']}")
        logger.info(f"Test Result: {test_passed}")
        logger.info(f"Reason: {test_result_reason}")
        logger.info("\n")

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


def load_tests(test_name):
    test_file_path = f"./magik_tests/{test_name}/assertions.py"
    # Get the absolute path by resolving against the current working directory
    absolute_path = os.path.abspath(test_file_path)

    # Get the directory path and module name from the absolute path
    directory, module_name = os.path.split(absolute_path)
    module_name = os.path.splitext(module_name)[0]

    # Set the current working directory to the test directory
    os.chdir(directory)

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location(module_name, absolute_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Access the `tests` array from the module
    return getattr(module, "tests", [])

import os
import importlib.util
from magik_prompt_sdk.logger import logger


def run_test(test_name):
    tests = load_tests(test_name)

    # Perform your custom logic to run the tests
    for test in tests:
        # Execute the test logic
        print(f"Running test: {test}")


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

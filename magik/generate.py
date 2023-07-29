from .internal_logger import logger
from .constants import TEST_DIR
from .sys_exec import read_from_file, write_to_file
from .constants import EXAMPLES_DIR
import inspect


# Get the path of the file within the module
def _get_module_file_path(file_name):
    module = inspect.getmodule(_get_module_file_path)
    module_file_path = inspect.getfile(module)
    module_dir = module_file_path.rpartition(
        "/")[0]  # Extract the directory path
    file_path = module_dir + "/" + file_name  # Combine with the file name
    return file_path


def _generate_example_prompt(test_path):
    example_prompt = (
        "Write a tweet about my new app named {app_name}. Make sure to include a link."
    )
    write_to_file(f"{test_path}/prompt.txt", example_prompt)


def _generate_example_assertions(test_path):
    abs_assertions_filepath = _get_module_file_path("./examples/assertions.py")
    example_assertions = read_from_file(abs_assertions_filepath)
    write_to_file(f"{test_path}/assertions.py", example_assertions)


def generate_test(test_name):
    logger.debug(f"Generating test {test_name}...\n")
    test_path = f"{TEST_DIR}/{test_name}"

    _generate_example_prompt(test_path)
    _generate_example_assertions(test_path)
    logger.success(
        f"""Generated test {test_name}
- {test_path}/assertions.py
- {test_path}/prompt.txt
"""
    )
    return 1

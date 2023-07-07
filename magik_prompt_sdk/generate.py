import os
from magik_prompt_sdk.logger import logger
from magik_prompt_sdk.constants import TEST_DIR
from magik_prompt_sdk.sys_exec import read_from_file, write_to_file
from magik_prompt_sdk.constants import MAGIK_SDK_DIR


def generate_test(test_name):
    logger.debug(f"Generating test {test_name}...\n")
    test_path = f"./{TEST_DIR}/{test_name}"
    example_assertions = read_from_file(
        f"{MAGIK_SDK_DIR}/magik_prompt_sdk/examples/assertions.py"
    )
    example_prompt = read_from_file(
        f"{MAGIK_SDK_DIR}/magik_prompt_sdk/examples/prompt.txt"
    )
    write_to_file(f"{test_path}/assertions.py", example_assertions)
    write_to_file(f"{test_path}/prompt.txt", example_prompt)
    logger.success(
        f"""Generated test {test_name}
- {test_path}/assertions.py
- {test_path}/prompt.txt
    """
    )
    return 1
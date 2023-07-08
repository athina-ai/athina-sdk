import os
from magik_prompt_sdk.logger import logger
from magik_prompt_sdk.sys_exec import write_to_file
from magik_prompt_sdk.constants import (
    TESTRUNS_DIR,
    TEST_DIR,
    CONFIG_FILE_PATH,
    EXAMPLE_CONFIG_PATH,
)
from magik_prompt_sdk.sys_exec import read_from_file


# Create magik_tests directory
# Create magik_test_runs directory
# Create magik_config.json
def initialize():
    create_magik_tests_dir()
    create_magik_test_runs_dir()
    create_magik_config_file()


def create_magik_tests_dir():
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR, exist_ok=True)
        logger.info(f"✅ Created {TEST_DIR} directory")
    else:
        logger.info(f"{TEST_DIR} directory already exists")


def create_magik_test_runs_dir():
    if not os.path.exists(TESTRUNS_DIR):
        os.makedirs(TESTRUNS_DIR, exist_ok=True)
        logger.info(f"✅ Created {TESTRUNS_DIR} directory")
    else:
        logger.info(f"{TESTRUNS_DIR} directory already exists")


def create_magik_config_file():
    # Check if magik_config.json already exists
    if os.path.exists(CONFIG_FILE_PATH):
        logger.info(f"{CONFIG_FILE_PATH} already exists!")
        return

    # Create file magik_config.json
    logger.debug("Creating magik_config.json...")
    example_config_contents = _read_example_config_file()
    write_to_file(
        CONFIG_FILE_PATH,
        example_config_contents,
    )

    logger.info(f"✅ Created {CONFIG_FILE_PATH} (config file)")
    logger.info("")
    logger.log_with_color(
        f"IMP: Please fill in the API keys in {CONFIG_FILE_PATH}", "yellow"
    )
    logger.info("")


def _read_example_config_file():
    return read_from_file(EXAMPLE_CONFIG_PATH)

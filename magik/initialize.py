import os
from internal_logger import logger
from sys_exec import write_to_file
from constants import (
    TESTRUNS_DIR,
    TEST_DIR,
    CONFIG_FILE_PATH,
)
from magik.sys_exec import read_from_file


# Create magik_tests directory
# Create magik_test_runs directory
# Create magik_config.json
def initialize():
    _create_magik_tests_dir()
    _create_magik_test_runs_dir()
    _create_magik_config_file()
    _add_config_file_to_gitignore()


def _create_magik_tests_dir():
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR, exist_ok=True)
        logger.info(f"✅ Created {TEST_DIR} directory")
    else:
        logger.info(f"{TEST_DIR} directory already exists")


def _create_magik_test_runs_dir():
    if not os.path.exists(TESTRUNS_DIR):
        os.makedirs(TESTRUNS_DIR, exist_ok=True)
        logger.info(f"✅ Created {TESTRUNS_DIR} directory")
    else:
        logger.info(f"{TESTRUNS_DIR} directory already exists")


def _create_magik_config_file():
    # Check if magik_config.json already exists
    if os.path.exists(CONFIG_FILE_PATH):
        logger.info(f"{CONFIG_FILE_PATH} already exists!")
        return

    # Create file magik_config.json
    logger.debug("Creating magik_config.json...")
    example_config_contents = """{
    "MAGIK_API_KEY": "",
    "OPEN_AI_API_KEY": "",
    "OPEN_AI_DEFAULT_MODEL": "gpt-3.5-turbo"
}"""
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


def _add_config_file_to_gitignore():
    gitignore_path = ".gitignore"
    if not os.path.exists(gitignore_path):
        logger.info(f"{gitignore_path} does not exist!")
        logger.info(f"Make sure to add {CONFIG_FILE_PATH} to your gitignore file")
        return

    with open(gitignore_path, "a") as gitignore_file:
        gitignore_file.write("\n# Magik config file\nmagik_config.json\n")

    logger.info(f"✅ Added {CONFIG_FILE_PATH} to {gitignore_path}")

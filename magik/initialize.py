import os
from magik.internal_logger import logger
from magik.sys_exec import write_to_file
from magik.constants import (
    TEST_RUNS_DIR,
    TEST_DIR,
    CONFIG_FILE_PATH,
    SCHEDULE_CONFIG_FILE_PATH,
)


# Create magik_tests directory
# Create magik_test_runs directory
# Create magik_tests/magik_config.json
# Create magik_tests/schedule.json
def initialize():
    _create_magik_tests_dir()
    _create_magik_test_runs_dir()
    _create_magik_config_file()
    _create_schedule_config_file()


def _create_magik_tests_dir():
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR, exist_ok=True)
        logger.info(f"✅ Created {TEST_DIR} directory")
    else:
        logger.info(f"{TEST_DIR} directory already exists")


def _create_magik_test_runs_dir():
    if not os.path.exists(TEST_RUNS_DIR):
        os.makedirs(TEST_RUNS_DIR, exist_ok=True)
        logger.info(f"✅ Created {TEST_RUNS_DIR} directory")
    else:
        logger.info(f"{TEST_RUNS_DIR} directory already exists")


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

    # add config file to gitignore
    _add_to_gitignore()

    logger.info("")
    logger.log_with_color(
        f"IMP: Please fill in the API keys in {CONFIG_FILE_PATH}", "yellow"
    )
    logger.info("")


def _create_schedule_config_file():
    # Check if magik_config.json already exists
    if os.path.exists(SCHEDULE_CONFIG_FILE_PATH):
        logger.info(f"{SCHEDULE_CONFIG_FILE_PATH} already exists!")
        return

    # Create file magik_config.json
    logger.debug("Creating schedule_config.json...")

    example_schedule_config_contents = """[
  {
    "trigger_type": "by-slug",
    "trigger_data": [
      {
        "prompt_slug": "*",
        "test_slugs": "*"
      }
    ]
  }
]"""
    write_to_file(
        SCHEDULE_CONFIG_FILE_PATH,
        example_schedule_config_contents,
    )

    logger.info(f"✅ Created {SCHEDULE_CONFIG_FILE_PATH} (schedule config)")
    logger.info("")


def _add_to_gitignore():
    gitignore_path = ".gitignore"
    if not os.path.exists(gitignore_path):
        logger.info(f"{gitignore_path} does not exist!")
        logger.info(
            f"Make sure to add {CONFIG_FILE_PATH} to your gitignore file")
        return

    with open(gitignore_path, "a") as gitignore_file:
        gitignore_file.write(
            "\n# Magik config file\nmagik_config.json\nmagik_tests/test_runs/*\n"
        )

    logger.info(f"✅ Added {CONFIG_FILE_PATH} to {gitignore_path}")

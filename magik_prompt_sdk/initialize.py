import os
from magik_prompt_sdk.logger import logger
from magik_prompt_sdk.sys_exec import write_to_file


# Create magik_tests directory
# Create magik_test_runs directory
# Create magik_config.json
def initialize():
    create_magik_tests_dir()
    create_magik_test_runs_dir()
    create_magik_config_file()


def create_magik_tests_dir():
    if not os.path.exists("./magik_tests"):
        os.mkdir("./magik_tests")
        logger.info("✅ Created ./magik_tests directory")
    else:
        logger.info("./magik_tests directory already exists")


def create_magik_test_runs_dir():
    if not os.path.exists("./magik_test_runs"):
        os.mkdir("./magik_test_runs")
        logger.error("✅ Created ./magik_test_runs directory")
    else:
        logger.info("./magik_test_runs directory already exists")


def create_magik_config_file():
    magik_config_path = "./magik_tests/magik_config.json"

    # Check if magik_config.json already exists
    if os.path.exists(magik_config_path):
        logger.info(f"{magik_config_path} already exists!")
        return

    # Create file magik_config.json
    logger.debug("Creating magik_config.json...")
    write_to_file(
        magik_config_path,
        """{
    "MAGIK_API_KEY": "",
    "OPEN_AI_API_KEY": ""
}""",
    )

    logger.info("✅ Created ./magik_tests/magik_config.json (config file)")
    logger.info("")
    logger.log_with_color(
        "IMP: Please fill in the API keys in magik_config.json", "yellow"
    )
    logger.info("")

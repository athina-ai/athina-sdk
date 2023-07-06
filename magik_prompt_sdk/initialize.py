import os
from magik_prompt_sdk.logger import logger
from magik_prompt_sdk.sys_exec import write_to_file


def initialize():
    magik_config_path = "./magik_tests/magik_config.json"
    # If magik_config exists, exit
    if os.path.exists(magik_config_path):
        logger.error("magik_config.json already exists!")
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

    logger.info("✅ Created magik_config.json...")
    logger.info("")
    logger.log_with_color(
        "IMP: Please fill in the API keys in magik_config.json", "yellow"
    )
    logger.info("")

import json
from magik_prompt_sdk.sys_exec import read_json_file
from magik_prompt_sdk.constants import CONFIG_FILE_PATH


def _load_config():
    return read_json_file(CONFIG_FILE_PATH)


def get_magik_api_key():
    config = _load_config()
    return config.get("MAGIK_API_KEY")


def get_open_ai_api_key():
    config = _load_config()
    return config.get("OPEN_AI_API_KEY")


def get_open_ai_default_model():
    config = _load_config()
    return config.get("OPEN_AI_DEFAULT_MODEL")

import os
import requests
from magik.internal_logger import logger
from magik.constants import CONFIG_FILE_PATH, DEPLOY_URL, TEST_DIR
from magik.config import get_magik_api_key


def deploy_test(test_name: str):
    api_key = get_magik_api_key()
    if api_key == None:
        logger.error(f"No API key found. Please add your API key to {CONFIG_FILE_PATH}")

    # construct the file path
    file_path = f"{TEST_DIR}/{test_name}/assertions.py"

    # check if the file exists
    if not os.path.isfile(file_path):
        logger.info(f"No assertions.py file found for test_name {test_name}")
        return

    # read file
    with open(file_path, "rb") as f:
        file_content = f.read()

    # prepare data for API request
    headers = {"magik-api-key": api_key}
    data = {"testId": test_name}
    files = {"file": ("assertions.py", file_content)}

    # make a POST request to the API
    response = requests.post(DEPLOY_URL, files=files, data=data, headers=headers)

    # check the response
    if response.status_code == 200:
        logger.info(f"Successfully uploaded {file_path}")
    else:
        logger.info(
            f"Failed to upload {file_path}. Status code: {response.status_code}"
        )


def deploy_all(api_key: str):
    # find all test_ids in {TEST_DIR}
    test_names = os.listdir(TEST_DIR)

    for test_name in test_names:
        deploy_test(test_name, api_key)

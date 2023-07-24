# API URLs
API_BASE_URL = "https://api.magiklabs.app"
DEPLOY_URL = f"{API_BASE_URL}/api/v1/testDeploy"
RUN_URL = f"{API_BASE_URL}/api/v1/testRun/group"

# Directory paths
TEST_DIR = "./magik_tests/tests"
TESTRUNS_DIR = "./magik_tests/test_runs"
CONFIG_FILE_PATH = f"./magik_tests/magik_config.json"
SCHEDULE_CONFIG_FILE_PATH = f"./magik_tests/schedule.json"
MAGIK_SDK_DIR = "./magik"  # TODO: This should come from the directory that one will have on running pip install magik
EXAMPLES_DIR = f"{MAGIK_SDK_DIR}/examples"
EXAMPLE_CONFIG_PATH = f"{EXAMPLES_DIR}/magik_config.example.json"

# Open AI defaults
OPEN_AI_DEFAULT_MODEL = "gpt-3.5-turbo"

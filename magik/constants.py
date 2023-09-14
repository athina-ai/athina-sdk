# API URLs
# API_BASE_URL = "https://api.magiklabs.app"
API_BASE_URL = "http://localhost:9000"
DEPLOY_URL = f"{API_BASE_URL}/api/v1/testDeploy"
RUN_URL = f"{API_BASE_URL}/api/v1/testRun/trigger/byPromptSlug"

# Directory paths
TEST_DIR = "./magik_tests/tests"
TEST_RUNS_DIR = "./magik_tests/test_runs"
CONFIG_FILE_PATH = f"./magik_tests/magik_config.json"
SCHEDULE_CONFIG_FILE_PATH = f"./magik_tests/schedule.json"
# TODO: This should come from the directory that one will have on running pip install magik
MAGIK_SDK_DIR = "./magik"
EXAMPLES_DIR = f"{MAGIK_SDK_DIR}/examples"
EXAMPLE_CONFIG_PATH = f"{EXAMPLES_DIR}/magik_config.example.json"

# Open AI defaults
OPEN_AI_DEFAULT_MODEL = "gpt-3.5-turbo"

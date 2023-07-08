from magik_prompt_sdk.evaluators import (
    contains_any,
)


# Define custom functions here
# Should return { 'result': boolean, 'reason': string }
def custom_function(*args):
    # Your logic here
    return {"result": False, "reason": "custom reason."}


# Define tests here
tests = [
    # Test 1: Test that output contains any of the keywords
    {
        "description": "output contains any of the keywords",
        "eval_function": contains_any,
        "vars": {"text_to_translate": "Hello World"},
        "args": [["salut", "bonjour"]],
        "failure_labels": ["inaccurate"],
    },
    # Test 2: Test that output contains all of the keywords
    {
        "description": "output contains any of the keywords",
        "eval_function": contains_any,
        "vars": {"text_to_translate": "Hello World"},
        "args": [["monde", "bonjour"]],
        "failure_labels": ["missing_keywords"],
    },
]

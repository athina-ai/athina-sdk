from magik_prompt_sdk.evaluators import contains, regex_match
from magik_prompt_sdk.matchers import phone_number, email


# Define custom functions here
# Should return { 'result': boolean, 'reason': string }
def custom_function():
    return {"result": True, "reason": "Your custom reason here."}


# Define tests here
tests = [
    # Test 1: Test that output contains "Hello World"
    {
        "name": "output contains phone number",
        "eval_function": regex_match,
        "vars": {"text_to_translate": "Hello World"},
        "args": [phone_number],
        "failure_labels": ["contains_pii"],
    },
    {
        "name": "output contains email",
        "eval_function": regex_match,
        "vars": {"text_to_translate": "Hello World"},
        "args": [email],
        "failure_labels": ["contains_pii"],
    },
]

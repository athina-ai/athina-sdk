# from magik_prompt_sdk import eval


# Define custom functions here
# Should return { 'result': boolean, 'reason': string }
def custom_function():
    return {"result": True, "reason": "Your custom reason here."}


# Define tests here
tests = [
    # Test 1: Test that output contains "Hello World"
    {
        "name": "output contains hello world",
        "eval_function": custom_function,
        "vars": {"name": "Shiv"},
        "args": ["Hello World"],
    },
]

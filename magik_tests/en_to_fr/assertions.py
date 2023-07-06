from magik_prompt_sdk.evaluators import contains_all, contains_any, negate


# Define custom functions here
# Should return { 'result': boolean, 'reason': string }
def custom_function(*args):
    return {"result": True, "reason": "Your custom reason here."}


# Define tests here
tests = [
    # Test 1: Test that output contains "Hello World"
    {
        "name": "output contains Bonjour",
        "eval_function": negate,
        "vars": {"text_to_translate": "Hello World"},
        "args": [custom_function, ("boNjourss", "bonjour", "Monde"), False],
    },
]

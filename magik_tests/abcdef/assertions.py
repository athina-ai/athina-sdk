from magik_prompt_sdk.evaluators import contains, equals, regex_match


# Define custom functions here
# Should return { 'result': boolean, 'reason': string }
def custom_function():
    return {"result": True, "reason": "Your custom reason here."}


# Define tests here
tests = [
    # Test 1: Test that output contains "Hello World"
    {
        "name": "output contains",
        "vars": {"language": "French", "text_to_translate": "Hello good people"},
        "eval_function": contains,
        "args": ["Bonjour"],
    },
    {
        "name": "output matches regex",
        "vars": {"language": "French", "text_to_translate": "Hello good people"},
        "eval_function": regex_match,
        "args": [".*lem.*"],
    },
]

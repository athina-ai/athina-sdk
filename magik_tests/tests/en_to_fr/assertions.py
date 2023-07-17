from magik.evaluators import (
    contains_all,
    contains_any,
    ends_with,
)


# Define custom functions here
# Should return { 'result': boolean, 'reason': string }
def custom_function(*args):
    # Your logic here
    return {"result": False, "reason": "Hallucination detected."}


# Define tests here
tests = [
    # Test 1: Test that output contains any of the keywords
    {
        "description": "output contains any of the keywords",
        "eval_function": contains_any,
        "prompt_vars": {"text_to_translate": "Hello World"},
        "eval_function_args": [["salut", "bonjour"]],
        "failure_labels": ["inaccurate"],
    },
    # Test 2: Test that output contains all of the keywords
    {
        "description": "output contains all of the keywords",
        "eval_function": contains_all,
        "prompt_vars": {"text_to_translate": "Hello World"},
        "eval_function_args": [["bonjour", "Monde"]],
        "failure_labels": ["inaccurate"],
    },
    # Test 3: Test that output contains all of the keywords
    {
        "description": "output is a question - ends with a question mark",
        "eval_function": ends_with,
        "prompt_vars": {
            "text_to_translate": "Who is the president of the united states?"
        },
        "eval_function_args": ["?"],
        "failure_labels": ["inaccurate"],
    },
]

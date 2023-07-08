from magik_prompt_sdk.evaluators import (
    contains,
    contains_all,
    contains_any,
    negate,
    contains_none,
    grade_using_llm,
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
        "name": "output contains any of the keywords",
        "eval_function": contains_any,
        "vars": {"text_to_translate": "Hello World"},
        "args": [["boNjourss", "bonjour", "Monde"]],
        "failure_labels": ["inaccurate"],
    },
    # Test 2: Test that output contains all of the keywords
    {
        "name": "output contains all of the keywords",
        "eval_function": contains_all,
        "vars": {"text_to_translate": "Hello World"},
        "args": [["boNjourss", "bonjour", "Monde"]],
        "failure_labels": ["inaccurate"],
    },
    # Test 3: Test that output contains a specific keyword
    {
        "name": "output contains all of the keywords",
        "eval_function": contains,
        "vars": {"text_to_translate": "Hello World"},
        "args": ["boNjour"],
        "failure_labels": ["inaccurate"],
    },
    # Test 4: Test that output contains any of the keywords
    {
        "name": "output contains all of the keywords",
        "eval_function": contains_any,
        "vars": {"text_to_translate": "Hello World"},
        "args": [["boNjourss", "bonjour", "Monde"]],
        "failure_labels": ["inaccurate"],
    },
    # Test 5: Test that output contains none of the keywords
    {
        "name": "output contains none of the keywords",
        "eval_function": contains_none,
        "vars": {"text_to_translate": "Hello World"},
        "args": [["boNjourss", "bonjour", "Monde"]],
        "failure_labels": ["inaccurate"],
    },
    # Test 6: Test that output passes a custom test function
    {
        "name": "output passes custom function",
        "eval_function": custom_function,
        "vars": {"text_to_translate": "Hello World"},
        "args": [],
        "failure_labels": ["hallucination"],
    },
    # Test 7: Test that output fails a custom test function
    {
        "name": "output does not pass custom_function",
        "eval_function": negate,
        "vars": {"text_to_translate": "Hello World"},
        "args": [contains, "Hello World"],
        "failure_labels": ["bad_response_format"],
    },
    # Test 8: Grade using LLM
    {
        "name": "grade using LLM",
        "eval_function": grade_using_llm,
        "vars": {"text_to_translate": "Hello World"},
        "args": ["If the output contains Bonjour, then pass the Test"],
        "failure_labels": ["bad_response_format"],
    },
]

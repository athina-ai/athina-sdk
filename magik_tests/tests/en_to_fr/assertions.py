from magik.evaluators import (
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
    return {"result": False, "reason": "Hallucination detected."}


# Define tests here
tests = [
    # Test 1: Test that output contains any of the keywords
    {
        "description": "output contains any of the keywords",
        "eval_function": contains_any,
        "prompt_vars": {"text_to_translate": "Hello World"},
        "eval_function_args": [["salut", "bonjour", "Monde"]],
        "failure_labels": ["inaccurate"],
    },
    # Test 2: Test that output contains all of the keywords
    {
        "description": "output contains all of the keywords",
        "eval_function": contains_all,
        "prompt_vars": {"text_to_translate": "Hello World"},
        "eval_function_args": [["boNjourss", "bonjour", "Monde"]],
        "failure_labels": ["inaccurate"],
    },
    # Test 3: Test that output contains a specific keyword
    {
        "description": "output contains a specific keyword",
        "eval_function": contains,
        "eval_function_args": ["boNjour"],
        "prompt_vars": {"text_to_translate": "Hello World"},
        "failure_labels": ["inaccurate"],
    },
    # Test 4: Test that output contains any of the keywords
    {
        "description": "output contains any of the keywords",
        "eval_function": contains_any,
        "prompt_vars": {"text_to_translate": "Hello World"},
        "eval_function_args": [["boNjourss", "bonjour", "Monde"]],
        "failure_labels": ["critical"],
    },
    # Test 5: Test that output contains none of the keywords
    {
        "description": "output does not contain restricted keywords",
        "eval_function": contains_none,
        "prompt_vars": {"text_to_translate": "Hello World"},
        "eval_function_args": [["artificial", "intelligence"]],
        "failure_labels": ["contains_pii"],
    },
    # Test 6: Test that output passes a custom test function
    {
        "description": "output passes custom function",
        "eval_function": custom_function,
        "prompt_vars": {"text_to_translate": "Hello World"},
        "eval_function_args": [],
        "failure_labels": ["hallucination"],
    },
    # Test 7: Test that output fails a custom test function
    {
        "description": "output does not pass custom_function",
        "eval_function": negate,
        "prompt_vars": {"text_to_translate": "Hello World"},
        "eval_function_args": [contains, "Hello World"],
        "failure_labels": ["bad_response_format"],
    },
    # Test 8: Grade using LLM
    {
        "description": "grade using LLM",
        "eval_function": grade_using_llm,
        "prompt_vars": {"text_to_translate": "Hello World"},
        "eval_function_args": ["If the output contains Bonjour, then pass the Test"],
        "failure_labels": ["bad_response_format"],
    },
]

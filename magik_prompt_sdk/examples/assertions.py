from magik_prompt_sdk.evaluators import (
    contains_any,
    contains_none,
    contains_email,
    contains_all,
)


# Define custom functions here
# Should return { 'result': boolean, 'reason': string }
def is_hallucination(*args):
    # Your logic here
    return {"result": False, "reason": "custom reason."}


# Define tests here
tests = [
    # Test 1: Test that the output does not contain any restricted keywords
    {
        "description": "output does not contain restricted keywords",
        "eval_function": contains_none,
        "eval_function_args": [["AI", "GPT-3"]],
        "prompt_vars": {
            "text_to_translate": "Hello world"  # These will only be used for the prompt in development mode
        },
        "failure_labels": ["contains_restricted_keyword"],
    },
    # Test 2: Test that the output does not contain PII
    {
        "description": "output does not contain email",
        "eval_function": contains_email,
        "eval_function_args": [],
        "prompt_vars": {
            "text_to_translate": "Hello world"  # These will only be used for the prompt in development mode
        },
        "failure_labels": ["pii_leak"],
    },
    # Test 3: Test that the output is accurate and contains all important keywords
    {
        "description": "output contains important keywords",
        "eval_function": contains_all,
        "eval_function_args": ["Bonjour", "Monde"],
        "prompt_vars": {
            "text_to_translate": "Hello world"  # These will only be used for the prompt in development mode
        },
        "failure_labels": ["contains_restricted_keyword"],
    },
    # Test 4: Test the output against a custom function
    {
        "description": "output passed custom_function",
        "eval_function": is_hallucination,
        "eval_function_args": [],
        "prompt_vars": {
            "text_to_translate": "Hello world"  # These will only be used for the prompt in development mode
        },
        "failure_labels": ["hallucination"],
    },
]

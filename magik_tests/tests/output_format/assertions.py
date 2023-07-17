from magik.evaluators import (
    is_json,
    contains_json,
    contains_email,
    contains_phone_number,
    contains_link,
    contains_valid_link,
    contains_credit_card_number,
    grade_using_llm,
)


# Define custom functions here
# Should return { 'result': boolean, 'reason': string }
def is_hallucination(*args):
    # Your logic here
    return {"result": False, "reason": "custom reason."}


# Define tests here
tests = [
    {
        "description": "output contains json",
        "eval_function": contains_json,
        "eval_function_args": [],
        "prompt_vars": {},
        "failure_labels": ["bad_format"],
    },
    {
        "description": "output is json",
        "eval_function": is_json,
        "eval_function_args": [],
        "prompt_vars": {},
        "failure_labels": ["bad_format"],
    },
    {
        "description": "output contains email",
        "eval_function": contains_email,
        "eval_function_args": [],
        "prompt_vars": {},
        "failure_labels": ["missing_information"],
    },
    {
        "description": "output contains credit card information",
        "eval_function": contains_credit_card_number,
        "eval_function_args": [],
        "prompt_vars": {},
        "failure_labels": ["missing_information"],
    },
    {
        "description": "output contains link",
        "eval_function": contains_link,
        "eval_function_args": [],
        "prompt_vars": {},
        "failure_labels": ["missing_information"],
    },
    {
        "description": "output contains valid link",
        "eval_function": contains_valid_link,
        "eval_function_args": [],
        "prompt_vars": {},
        "failure_labels": ["missing_information"],
    },
]

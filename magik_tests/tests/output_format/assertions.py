from magik.evaluators import (
    is_json,
    contains_json,
    contains_email,
    contains_link,
    contains_valid_link,
    contains_credit_card_number,
)

# Define tests here
test_context = {}


# Define tests here
def define_tests(context: dict):
    return [
        {
            "description": "output contains json",
            "eval": contains_json(),
            "prompt_vars": {},
            "failure_labels": ["bad_format"],
        },
        {
            "description": "output is json",
            "eval": is_json(),
            "prompt_vars": {},
            "failure_labels": ["bad_format"],
        },
        {
            "description": "output contains email",
            "eval": contains_email(),
            "prompt_vars": {},
            "failure_labels": ["missing_information"],
        },
        {
            "description": "output contains credit card information",
            "eval": contains_credit_card_number(),
            "prompt_vars": {},
            "failure_labels": ["missing_information"],
        },
        {
            "description": "output contains link",
            "eval": contains_link(),
            "prompt_vars": {},
            "failure_labels": ["missing_information"],
        },
        {
            "description": "output contains valid link",
            "eval": contains_valid_link(),
            "prompt_vars": {},
            "failure_labels": ["missing_information"],
        },
    ]

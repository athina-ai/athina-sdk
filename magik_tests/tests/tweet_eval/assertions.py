from magik.evaluators import (
    contains_none,
    contains_link,
    contains_valid_link,
    not_contains_pii,
    is_positive_sentiment,
    length_less_than,
)

# Define tests here
tests = [
    {
        "description": "output does not contain pii",
        "eval_function": not_contains_pii,
        "eval_function_args": [],
        "prompt_vars": {},
        "failure_labels": ["sensitive_data"],
    },
    {
        "description": "output contains a link",
        "eval_function": contains_link,
        "eval_function_args": [],
        "prompt_vars": {},
        "failure_labels": ["bad_response_format"],
    },
    {
        "description": "output contains a valid link",
        "eval_function": contains_valid_link,
        "eval_function_args": [],
        "prompt_vars": {},
        "failure_labels": ["bad_response_format"],
    },
    {
        "description": "output sentiment is positive",
        "eval_function": is_positive_sentiment,
        "eval_function_args": [],
        "prompt_vars": {},
        "failure_labels": ["negative_sentiment"],
    },
    {
        "description": "output length is less than 280 characters",
        "eval_function": length_less_than,
        "eval_function_args": [280],
        "prompt_vars": {},
        "failure_labels": ["negative_sentiment"],
    },
    {
        "description": "output does not contain hashtags",
        "eval_function": contains_none,
        "eval_function_args": ["#"],
        "prompt_vars": {},
        "failure_labels": ["bad_response_format"],
    },
]

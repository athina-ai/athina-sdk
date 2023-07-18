from magik.evaluators import (
    contains_none,
    contains_link,
    contains_valid_link,
    not_contains_pii,
    is_positive_sentiment,
    length_less_than,
    contains,
    negate,
)


def is_hallucination(output):
    return {"result": False, "reason": "Custom reason for is_hallucination"}


# Define tests here
tests = [
    {
        # not_contains_pii(output)
        "description": "output does not contain pii",
        "eval_function": not_contains_pii,
        "eval_function_args": [],
        "prompt_vars": {
            "name": "Ola!",
            "num_chars": 280,
        },
        "failure_labels": ["sensitive_data"],
    },
    {
        # contains_link(output)
        "description": "output contains a link",
        "eval_function": contains_link,
        "eval_function_args": [],
        "prompt_vars": {
            "name": "Uber",
            "num_chars": 280,
        },
        "failure_labels": ["bad_response_format"],
    },
    {
        # contains_valid_link(output)
        "description": "output contains a valid link",
        "eval_function": contains_valid_link,
        "eval_function_args": [],
        "prompt_vars": {
            "name": "Magik",
            "num_chars": 280,
        },
        "failure_labels": ["bad_response_format"],
    },
    {
        # is_positive_sentiment(output)
        "description": "output sentiment is positive",
        "eval_function": is_positive_sentiment,
        "eval_function_args": [],
        "prompt_vars": {
            "name": "Lyft",
            "num_chars": 280,
        },
        "failure_labels": ["negative_sentiment"],
    },
    {
        # length_less_than(output, 280)
        "description": "output length is less than 280 characters",
        "eval_function": length_less_than,
        "eval_function_args": [280],
        "prompt_vars": {
            "name": "Facebook",
            "num_chars": 280,
        },
        "failure_labels": ["negative_sentiment", "critical"],
    },
    {
        # contains_all(output, ["#"])
        "description": "output does not contain hashtags",
        "eval_function": contains_none,
        "eval_function_args": ["#"],
        "prompt_vars": {
            "name": "Datadog",
            "num_chars": 280,
        },
        "failure_labels": ["bad_response_format"],
    },
]

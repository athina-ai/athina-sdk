from magik.evaluators import (
    contains_all,
    contains_any,
    ends_with,
    negate,
)

# Define tests here
tests = [
    {
        "description": "output contains any of the keywords",
        "eval": 'contains_any(["bonjour", "salut", "coucou"])',
        "prompt_vars": {"text_to_translate": "Hello World"},
        "failure_labels": ["inaccurate"],
    },
    {
        "description": "output contains all of the keywords",
        "eval": 'contains_all(["bonjour", "monde"], case_sensitive=False)',
        "prompt_vars": {"text_to_translate": "Hello World"},
        "failure_labels": ["inaccurate"],
    },
    {
        "description": "output is a question - ends with a question mark",
        "eval": 'ends_with("?")',
        "prompt_vars": {
            "text_to_translate": "Who is the president of the united states?"
        },
        "failure_labels": ["inaccurate"],
    },
    {
        "description": "output is a question - ends with a question mark",
        "eval": 'negate(ends_with("?"))',
        "prompt_vars": {
            "text_to_translate": "Who is the president of the united states?"
        },
        "failure_labels": ["inaccurate"],
    },
]

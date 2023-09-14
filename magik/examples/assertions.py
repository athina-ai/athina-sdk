from magik.decorators import magik_eval
from magik.evaluators import (
    contains_valid_link,
)


# Define a custom test like this
#
# output_to_test is automatically passed in when we run the test
# as long as we have the @magik_eval decorator
#
@magik_eval
def is_valid_length(output_to_test):
    result = len(output_to_test) < 1000
    return {
        "result": result,
        "reason": "Output length is correct" if result else "Output length is invalid",
    }


# Context is the ground truth data
# If you have access to ground truth data, you can use it to define your tests
test_context = {}


# Every test must contain:
# - description: a description of the test
# - eval: the function to run to evaluate the output
# - prompt_vars:
#   - dictionary of variable values to pass into the prompt
#   - these will replace variables in curly {braces} in your prompt.txt file in local tests
# - failure_labels: the labels to tag the failure with - used for the analytics dashboard
def define_tests(context: dict):
    return [
        {
            "description": "output contains a valid link (no 404)",
            "eval": contains_valid_link(),
            "prompt_vars": {
                "app_name": "Magik",
            },
            "failure_labels": [""],
        },
        {
            "description": "output passes custom function",
            "eval": is_valid_length(),
            "prompt_vars": {
                "app_name": "Magik",
            },
            "failure_labels": ["response_too_long"],
        },
    ]

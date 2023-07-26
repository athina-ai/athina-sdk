from magik.decorators import magik_eval
from magik.evaluators import (
    contains_any,
    contains_valid_link,
    matches_desired_classification,
)


classification_labels_and_descriptions = [
    {
        "label": "Unsubscribe_Response",
        "description": "Offers the user a free trial to keep them subscribed. For example: 'We're sorry to hear that. We'd like to offer you a free trial to keep you subscribed.'",
    },
    {
        "label": "Refer_To_Human_Response",
        "description": "Refers the user to a human agent. For example: 'I'm sorry to hear that. I'll refer you to a human agent who can help you.'",
    },
    {
        "label": "Appreciation_Response",
        "description": "Responds with appreciation. For example: 'Thank you for your feedback. We're glad you like our app.'",
    },
    {
        "label": "Instructions_Response",
        "description": "Responds with instructions. For example: 'To change your password, go to the settings page and click on the 'Change Password' button.'",
    },
]
input_description = "The AI response to a human's query."
task_description = "Classify the AI response into one of the classification labels."


# Define a custom test like this
#
# output_to_test is automatically passed in when we run the test
# as long as we have the @magik_eval decorator
#
@magik_eval
def is_valid_length(max_length, output_to_test):
    result = len(output_to_test) < max_length
    return {
        "result": result,
        "reason": "Output length is correct" if result else "Output length is invalid",
    }


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
            "description": "Response is within length limits",
            "eval": is_valid_length(max_length=500),
            "prompt_vars": {
                "query": "How can I change my password?",
            },
            "failure_labels": ["response_too_long"],
        },
        {
            "description": "Response to a question must contain a valid link",
            "eval": contains_valid_link(),
            "prompt_vars": {
                "query": "How can I change my password?",
            },
            "failure_labels": ["missing_link"],
        },
        {
            "description": "Response to a compliment should ask for feedback",
            "eval": contains_any(["feedback", "better", "improve"]),
            "prompt_vars": {
                "query": "I love the app!",
            },
            "failure_labels": ["no_feedback"],
        },
        {
            "description": "Response to a question should contain instructions",
            "eval": matches_desired_classification(
                classification_labels_and_descriptions=classification_labels_and_descriptions,
                input_description=input_description,
                task_description=task_description,
                desired_classification_label="Refer_To_Human_Response",
            ),
            "prompt_vars": {
                "query": "How can I change my password?",
            },
            "failure_labels": ["no_instructions"],
        },
        {
            "description": "Response to a complaint should refer to a human agent",
            "eval": matches_desired_classification(
                classification_labels_and_descriptions=classification_labels_and_descriptions,
                input_description=input_description,
                task_description=task_description,
                desired_classification_label="Refer_To_Human_Response",
            ),
            "prompt_vars": {
                "query": "The app is very slow - it's not easy to use.",
            },
            "failure_labels": ["complaint_not_referred_to_human"],
        },
        {
            "description": "Response to a compliment should be appreciative",
            "eval": matches_desired_classification(
                classification_labels_and_descriptions=classification_labels_and_descriptions,
                input_description=input_description,
                task_description=task_description,
                desired_classification_label="Appreciation_Response",
            ),
            "prompt_vars": {
                "query": "The app is really user-friendly!",
            },
            "failure_labels": ["wrong_intent"],
        },
        {
            "description": "Response to unsubscribe query should offer the user a free trial",
            "eval": matches_desired_classification(
                classification_labels_and_descriptions=classification_labels_and_descriptions,
                input_description=input_description,
                task_description=task_description,
                desired_classification_label="Unsubscribe_Response",
            ),
            "prompt_vars": {
                "query": "I want to unsubscribe from the mailing list.",
            },
            "failure_labels": ["wrong_intent"],
        },
    ]

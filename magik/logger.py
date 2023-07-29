import requests
from .constants import API_BASE_URL
from .config import get_magik_api_key


# Log the request and response from OpenAI chat completion to Magik API
#
# prompt_slug: name of the prompt for analytics and grouping
# messages: "messages" json array sent to OpenAI chat completion
# model: string id of the language model used
# chat_completion: "choices" json response from OpenAI chat completion
def log_open_ai_chat_response(
    prompt_slug, messages, model, chat_completion, response_time, context=None
):
    """
    Track the request and response.
    """
    payload = {
        "prompt_slug": prompt_slug,
        "prompt_data": messages,
        "language_model_id": model,
        "completion": chat_completion,
        "response_time": response_time,
        "context": context,
    }
    # Remove None fields from the payload
    payload = {k: v for k, v in payload.items() if v is not None}
    requests.post(
        f"{API_BASE_URL}/api/v1/savePromptAndResponse",
        json=payload,
        headers={
            "magik-api-key": get_magik_api_key(),
        },
    )


def log_open_ai_completion_response(
    prompt_slug, message, model, completion, response_time, context=None
):
    """
    Track the request and response.
    """
    payload = {
        "prompt_slug": prompt_slug,
        "prompt_data": {
            "text": message
        },
        "language_model_id": model,
        "completion": completion,
        "response_time": response_time,
        "context": context,
    }
    # Remove None fields from the payload
    payload = {k: v for k, v in payload.items() if v is not None}
    requests.post(
        f"{API_BASE_URL}/api/v1/savePromptAndResponse",
        json=payload,
        headers={
            "magik-api-key": get_magik_api_key(),
        },
    )

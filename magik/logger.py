import requests
from magik.constants import API_BASE_URL
from magik.config import get_magik_api_key


# Log the request and response from OpenAI chat completion to Magik API
#
# prompt_slug: name of the prompt for analytics and grouping
# messages: "messages" json array sent to OpenAI chat completion
# model: string id of the language model used
# chat_completion: "choices" json response from OpenAI chat completion
def log_open_ai_chat_response(
    prompt_slug, messages, model, chat_completion, response_time
):
    """
    Track the request and response.
    """
    requests.post(
        f"{API_BASE_URL}/api/v1/savePromptAndResponse",
        json={
            "prompt_slug": prompt_slug,
            "prompt_data": messages,
            "language_model_id": model,
            "completion": chat_completion,
            "response_time": response_time,
        },
        headers={
            "magik-api-key": get_magik_api_key(),
        },
    )

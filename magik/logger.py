import requests
from .constants import API_BASE_URL
from .config import get_magik_api_key


# Log the request and response from OpenAI chat completion to Magik API
#
# prompt_slug: name of the prompt for analytics and grouping
# messages: "messages" json array sent to OpenAI chat completion
# model: string id of the language model used (ex: gpt-3.5-turbo)
# chat_completion: "choices" json response from OpenAI chat completion
# response_time: response_time in milliseconds (optional)
# context: any structured json data you wish to associate with the prompt response (useful for analytics and testing)
def log_open_ai_chat_response(
    prompt_slug, messages, model, chat_completion, response_time=None, context=None
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


# Log the request and response from OpenAI completion endpoint to Magik API
#
# prompt_slug: name of the prompt for analytics and grouping
# message: the prompt string sent to OpenAI completion endpoint
# model: string id of the language model used (ex: text-davinci-003)
# completion: json response from OpenAI completion endpoint
# response_time: response_time in milliseconds (optional)
# context: any structured json data you wish to associate with the prompt response (useful for analytics and testing)
def log_open_ai_completion_response(
    prompt_slug: str,
    message: str,
    model: str,
    completion,
    response_time=None,
    context=None,
):
    payload = {
        "prompt_slug": prompt_slug,
        "prompt_data": {"text": message},
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


# Log a generic llm response (not specific to any provider)
#
# prompt_slug: name of the prompt for analytics and grouping
# message: the prompt string used to generate this response
# llm_response: The string response you received from the LLM used
# response_time: response_time in milliseconds (optional)
# context: any structured json data you wish to associate with the prompt response (useful for analytics and testing)
def log_generic_response(
    prompt_slug: str, message: str, llm_response: str, response_time=None, context=None
):
    payload = {
        "prompt_slug": prompt_slug,
        "prompt_data": {"text": message},
        "language_model_id": "generic",
        "completion": {"text": llm_response},
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

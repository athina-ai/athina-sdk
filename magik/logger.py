import requests
from constants import API_BASE_URL
from config import get_magik_api_key


def logChatResponse(prompt_slug, prompt_sent, model, chat_completion, testId):
    """
    Track the request and response.
    """
    requests.post(
        f"{API_BASE_URL}/api/v1/savePromptAndResponse",
        json={
            "promptSlug": prompt_slug,
            "promptSent": prompt_sent,
            "languageModelId": model,
            "completion": chat_completion,
            "testId": testId,
        },
        headers={
            "magik-api-key": get_magik_api_key(),
        },
    )

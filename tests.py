import openai
from magik_prompt_sdk.logger import logChatResponse
from magik_prompt_sdk.config import get_open_ai_api_key

if __name__ == "__main__":
    openai.api_key = get_open_ai_api_key()

    prompt_text = "Hello, I'm a human"
    model = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt_text}],
    )
    logChatResponse(
        prompt_slug="hello_human",  # This is used for you to separate different prompts on our analytics dashboard
        prompt_sent=prompt_text,
        model=model,
        chat_completion=response,
        testId="human_test",  # This is how we associate which tests are run with which prompts
    )

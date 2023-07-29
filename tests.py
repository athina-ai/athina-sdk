import openai
from magik.config import get_open_ai_api_key

if __name__ == "__main__":
    openai.api_key = get_open_ai_api_key()

    prompt_text = "Hello, I'm a human"
    model = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt_text}],
    )

import openai
from tenacity import retry, stop_after_attempt, wait_fixed
from magik.constants import API_BASE_URL
from magik.config import (
    get_open_ai_api_key,
    get_open_ai_default_model,
    get_magik_api_key,
)


class OpenAI:
    def __init__(self):
        self.openai = openai
        self.default_model = get_open_ai_default_model()
        self.magik_api_key = get_magik_api_key()
        self.openai.api_key = get_open_ai_api_key()

    # Methods that call OpenAI API
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def openai_chat_completion(self, model, prompt):
        """
        Call the OpenAI API to generate a chat completion for models like GPT 3.5 turbo and GPT 4
        """
        return self.openai.ChatCompletion.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def openai_completion(self, model, prompt):
        """
        Call the OpenAI API to generate a completion for models like text davinci 003
        """
        return self.openai.Completion.create(model=model, prompt=prompt)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def get_embedding(self, text: str, model="text-embedding-ada-002") -> list[float]:
        return self.openai.Embedding.create(input=[text], model=model)["data"][0][
            "embedding"
        ]

    # Convenience methods that call OpenAI and return just the message content string
    def openai_chat_completion_message(self, model, prompt):
        """
        Call the OpenAI API to generate a chat completion for models like GPT 3.5 turbo and GPT 4
        Returns just the message content string
        """
        response = self.openai_chat_completion(model, prompt)
        return response.choices[0].message.content

    def openai_completion_message(self, model, prompt):
        """
        Call the OpenAI API to generate a completion for models like text davinci 003
        Returns just the message content string
        """
        response = self.openai_completion(model, prompt)
        return response.choices[0].text

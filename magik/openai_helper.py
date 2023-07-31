import openai
from tenacity import retry, stop_after_attempt, wait_fixed
from .constants import API_BASE_URL
from .config import (
    get_open_ai_api_key,
    get_open_ai_default_model,
    get_magik_api_key,
)

chat_completion_models = ["gpt-3.5-turbo", "gpt-4"]
completion_models = ["text-davinci-003"]
is_chat_model = lambda model: model in chat_completion_models
is_completion_model = lambda model: model in completion_models


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

    # Convenience method to call openai completion or chat completion
    def get_openai_response(self, model, prompt):
        if is_chat_model(model):
            return self.openai_chat_completion(model=model, prompt=prompt)
        elif is_completion_model(model):
            return self.openai_completion(model=model, prompt=prompt)
        else:
            raise ValueError("Invalid model: {}".format(model))

    # Convenience methods that call OpenAI and return just the message content string
    def get_openai_response_message(self, model, prompt):
        if is_chat_model(model):
            return self.openai_chat_completion_message(model=model, prompt=prompt)
        elif is_completion_model(model):
            return self.openai_completion_message(model=model, prompt=prompt)
        else:
            raise ValueError("Invalid model: {}".format(model))

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

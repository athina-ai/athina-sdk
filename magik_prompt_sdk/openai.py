import requests
import openai
import json
from magik_prompt_sdk.constants import API_BASE_URL

GPT3_MODELS = ["text-davinci-003", "text-davinci-002"]


class OpenAI:
    def __init__(self, API_KEY, MAGIK_API_KEY):
        self.openai = openai
        self.openai.api_key = API_KEY
        self.magik_api_key = MAGIK_API_KEY

    # ----------
    # --- Functions that simply call OpenAI --- #
    # ----------
    def openai_completion(self, model, prompt):
        """
        Call the OpenAI API to generate a completion for models like davinci-003 and davinci-002
        """
        return self.openai.Completion.create(model=model, prompt=prompt)

    def openai_chat_completion(self, model, prompt):
        """
        Call the OpenAI API to generate a chat completion for models like GPT 3.5 turbo and GPT 4
        """
        return self.openai.ChatCompletion.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )

    def openai_chat_completion_message(self, model, prompt):
        """
        Call the OpenAI API to generate a chat completion for models like GPT 3.5 turbo and GPT 4
        Returns just the message content string
        """
        response = self.openai_chat_completion(model, prompt)
        return response.choices[0].message.content

    # ----------
    # --- Functions that call OpenAI and also save prompts / prompt runs --- #
    # ----------

    def chat_completion(self, model, prompt, save_to_db=True):
        """
        Call the OpenAI API to generate a chat completion for models like gpt3.5 turbo and gpt 4
        """
        if save_to_db:
            promptResponse = requests.post(
                f"{API_BASE_URL}/api/v1/prompt", data={"text": prompt}, headers={
                    "magik-api-key": self.magik_api_key,
                }
            ).json()

        completion = self.openai_chat_completion(model, prompt)

        if save_to_db:
            self.save_prompt_run_chat_completion(
                model, completion, promptResponse
            )
        return completion

    def completion(self, model, prompt, save_to_db=True):
        """
        Call the OpenAI API to generate a completion for models like davinci-003 and davinci-002
        """
        if save_to_db:
            promptResponse = requests.post(
                f"{API_BASE_URL}/api/v1/prompt", data={"text": prompt}, headers={
                    "magik-api-key": self.magik_api_key,
                }
            ).json()

        completion = self.openai_completion(model, prompt)

        if save_to_db:
            self.save_prompt_run_completion(model, completion, promptResponse)
        return completion

    # ----------
    # --- Functions that save prompts / prompt runs --- #
    # ----------

    def save_prompt_run_chat_completion(self, model, completion, promptResponse):
        """
        Save prompt run to the database
        """
        requests.post(
            f"{API_BASE_URL}/api/v1/promptRun",
            json={
                "promptId": promptResponse["data"]["prompt"]["id"],
                "languageModelId": model,
                "promptSent": promptResponse["data"]["prompt"]["text"],
                "promptResponse": completion.choices[0].message.content,
                "tokensUsed": int(completion.usage.total_tokens),
            },
            headers={
                "magik-api-key": self.magik_api_key,
            }
        )

    def save_prompt_run_completion(self, model, completion, promptResponse):
        """
        Save prompt run to the database
        """
        requests.post(
            f"{API_BASE_URL}/api/v1/promptRun",
            json={
                "promptId": promptResponse["data"]["prompt"]["id"],
                "languageModelId": model,
                "promptSent": promptResponse["data"]["prompt"]["text"],
                "promptResponse": completion.choices[0].text,
                "tokensUsed": int(completion.usage.total_tokens),
            },
            headers={
                "magik-api-key": self.magik_api_key,
            }
        )

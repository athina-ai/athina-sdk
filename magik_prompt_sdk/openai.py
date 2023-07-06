import requests
import openai
import json
from magik_prompt_sdk.constants import API_BASE_URL

GPT3_MODELS = ["text-davinci-003", "text-davinci-002"]


class OpenAI:
    def __init__(self, API_KEY):
        self.openai = openai
        self.openai.api_key = API_KEY

    def chat_completion(self, model, prompt):
        """
        Call the OpenAI API to generate a chat completion for models like gpt3.5 turbo and gpt 4
        """
        promptResponse = requests.post(
            f"{API_BASE_URL}/api/v1/prompt", data={"text": prompt}
        ).json()
        completion = self.openai.ChatCompletion.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        self.save_prompt_run_chat_completion(model, completion, promptResponse)
        return completion

    def completion(self, model, prompt):
        """
        Call the OpenAI API to generate a completion for models like davinci-003 and davinci-002
        """
        promptResponse = requests.post(
            f"{API_BASE_URL}/api/v1/prompt", data={"text": prompt}
        ).json()
        completion = self.openai.Completion.create(model=model, prompt=prompt)
        self.save_prompt_run_completion(model, completion, promptResponse)
        return completion

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
        )
        # requests.post("http://localhost:9000/api/v1/promptRun", json={"promptId": promptResponse["data"]["prompt"]["id"], "languageModelId": completion.model,"promptSent": promptResponse["data"]["prompt"]["text"],"promptResponse": completion.choices[0].text, "tokensUsed": int(completion.usage.total_tokens)})

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
        )

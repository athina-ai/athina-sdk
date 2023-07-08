from magik_prompt_sdk import OpenAI

if __name__ == "__main__":
    openAI = OpenAI()
    print(openAI.completion("text-davinci-003", "Hello, how are you?"))

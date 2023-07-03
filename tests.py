from magik_prompt_sdk import OpenAI
if __name__ == '__main__':
    openAI = OpenAI('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')
    print(openAI.completion('text-davinci-003', 'Hello, how are you?'))
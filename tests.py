from magik_prompt_sdk import OpenAI
if __name__ == '__main__':
    openAI = OpenAI("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",
                    "-7wZmc77VeuwIEnz088lN8myKzVmzMDh")
    openAI.chat_completion(model="gpt-3.5-turbo",
                           prompt="What is the meaning of life?")

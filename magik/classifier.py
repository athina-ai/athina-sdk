from magik.openai_helper import OpenAI

classifier_prompt = """
You are acting as a classifier. 
I want you to classify this output into one of the classification labels I am describing.
I am giving you the classification labels along with a description of the label.

Use the description to understand what each label means.
Then classify the output I am providing you as one of the labels, depending on which description matches most closely.

Your response should contain ONLY the classification label, and nothing else.
If no description matches, then return "None"

For example:
"""

classifier_prompt_example = """
Classification Labels and Descriptions: {[
    {"label": "plod", "description": "Represents a mammal."},
    {"label": "zazu", "description": "Represents a bird"},
    {"label": "goon", "description": "Represents a fish or sea animal"},
]}

Output to classify: "Eagles are majestic birds that fly high in the sky."
AI: "zazu"

Output to classify: "Sharks are dangerous and should be avoided."
AI: "goon"

Output to classify: "Lions are kings of the jungle."
AI: "plod"
"""


def classify_output(
    classification_labels_and_descriptions: list[dict],
    input_description: str,
    task_description: str,
    output_to_test=None,
):
    openai = OpenAI()
    response_message = openai.openai_chat_completion_message(
        model="gpt-3.5-turbo",
        prompt=f"""
            {classifier_prompt}
            {classifier_prompt_example}
            
            Now here is my data to classify:
            ---
            My input represents: {input_description}
            I want to determine: {task_description}
            Classification Labels and Descriptions: {classification_labels_and_descriptions}
            Output to classify: {output_to_test}
            
        """,
    )
    return response_message

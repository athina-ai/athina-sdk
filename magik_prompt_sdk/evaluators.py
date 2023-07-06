# Contains functions to evaluate assertions.
import re
import ast
from magik_prompt_sdk.openai import OpenAI
from magik_prompt_sdk.constants import OPEN_AI_API_KEY, OPEN_AI_DEFAULT_MODEL


def generate_grading_prompt(output_to_evaluate, grading_criteria):
    return (
        """
    You are grading a response string according to a grading criteria given to you.
    
    If the gradient criteria is true, then the test_result is True. Otherwise, it is false.
    
    Explain the reason for the test_result in the reason field.
    
    Respond with a python dictionary object that looks like this:
    {test_result: boolean; reason: string;}
    
    Examples:

    String: Qui est le président des États-Unis?
    Grading Criteria: Contains the french words for 'president' and 'United States'
    {"test_result": True, "reason": "the content contains the word 'world'"}

    String: Earth is the second planet from the sun.
    Grading Criteria: If the fact is true, then the test_result is True. Otherwise, it is false.
    {"test_result": False, "reason": "The string is factually inaccurate - Earth is actually the third planet from the sun."}`
    """
        + f"""
        String: {output_to_evaluate}
        Grading Criteria: {grading_criteria}
    """
    )


# Define the evaluation functions
def equals(
    output_to_test,
    expected_output,
    case_sensitive=False,
):
    if case_sensitive == False:
        output_to_test = output_to_test.lower()
        expected_output = expected_output.lower()
    if output_to_test == expected_output:
        result = True
        reason = "✅ output exactly matches expected output"
    else:
        result = False
        reason = "output does not exactly match expected output"
    return {"result": result, "reason": reason}


def contains_all(output_to_test, keywords, case_sensitive=False):
    if case_sensitive == False:
        output_to_test = output_to_test.lower()
        keywords = list(map(lambda k: k.lower(), keywords))
    missing_keywords = []
    for keyword in keywords:
        if keyword not in output_to_test:
            result = False
            missing_keywords.append(keyword)
    if (len(missing_keywords)) > 0:
        result = False
        reason = f"keywords not found in output: " + ", ".join(missing_keywords)
    else:
        result = True
        reason = f"{len(keywords)}/{len(keywords)} keywords found in output"

    return {"result": result, "reason": reason}


def contains_any(output_to_test, keywords, case_sensitive=False):
    if not case_sensitive:
        output_to_test = output_to_test.lower()
        keywords = list(map(lambda k: k.lower(), keywords))

    found_keywords = []
    for keyword in keywords:
        if keyword in output_to_test:
            found_keywords.append(keyword)

    if found_keywords:
        result = True
        reason = f"One or more keywords were found in output: " + ", ".join(
            found_keywords
        )
    else:
        result = False
        reason = "No keywords found in output"

    return {"result": result, "reason": reason}


def negate(output_to_test, eval_function, *args, **kwargs):
    eval_result = eval_function(output_to_test, *args, **kwargs)
    return {
        "result": not eval_result["result"],
        "reason": f"{eval_function.__name__} returned {eval_result['result']} with reason {eval_result['reason']}",
    }


def contains(output_to_test, keyword, case_sensitive=False):
    if case_sensitive == False:
        output_to_test = output_to_test.lower()
        keyword = keyword.lower()
    if keyword not in output_to_test:
        result = False
        reason = f"keyword not found in output: " + keyword
    else:
        result = True
        reason = f"keyword {keyword} found in output"

    return {"result": result, "reason": reason}


def regex_match(output_to_test, pattern):
    match = re.match(pattern, output_to_test)
    if match:
        return {"result": True, "reason": f"regex pattern {pattern} found in output"}
    else:
        return {
            "result": False,
            "reason": f"regex pattern {pattern} not found in output",
        }


def starts_with(output_to_test, substring, case_sensitive=False):
    if case_sensitive == False:
        output_to_test = output_to_test.lower()
        substring = substring.lower()
    result = output_to_test.startswith(substring)
    if result == True:
        return {"result": result, "reason": "output starts with " + substring}
    else:
        return {"result": result, "reason": "output does not start with " + substring}


def ends_with(output_to_test, substring, case_sensitive=False):
    if case_sensitive == False:
        output_to_test = output_to_test.lower()
        substring = substring.lower()
    result = output_to_test.endswith(substring)
    if result == True:
        return {"result": result, "reason": "output ends with " + substring}
    else:
        return {"result": result, "reason": "output does not end with " + substring}


def grade_using_llm(output_to_test, eval_rubric):
    openai = OpenAI(OPEN_AI_API_KEY)
    # eval_rubric is a string that contains the rubric by which to evaluate the output
    evaluation_prompt = generate_grading_prompt(output_to_test, eval_rubric)
    llm_response = openai.openai_chat_completion_message(
        model=OPEN_AI_DEFAULT_MODEL, prompt=evaluation_prompt
    )

    # llm_response_dict is a dictionary that contains the response from the LLM
    llm_response_dict = ast.literal_eval(llm_response)

    # result is the true / false value from the LLM
    result = llm_response_dict["test_result"]
    reason = llm_response_dict["reason"]

    # output the result of the evaluation
    if result != True and result != False:
        result = False
        reason = "LLM response does not contain a boolean value"
    return {"result": result, "reason": reason}

# Contains functions to evaluate assertions.
import requests
import json
import re
import ast
from openai_helper import OpenAI
from utils import standardize_url
from constants import OPEN_AI_DEFAULT_MODEL


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


def contains_none(output_to_test, keywords, case_sensitive=False):
    if not case_sensitive:
        output_to_test = output_to_test.lower()
        keywords = list(map(lambda k: k.lower(), keywords))

    found_keywords = []
    for keyword in keywords:
        if keyword in output_to_test:
            found_keywords.append(keyword)

    if found_keywords:
        result = False
        reason = f"One or more keywords were found in output: " + ", ".join(
            found_keywords
        )
    else:
        result = True
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


def regex(output_to_test, pattern):
    match = re.search(pattern, output_to_test)
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
    openai = OpenAI()
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


def is_email(output_to_test):
    return regex(output_to_test, r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def is_phone_number(output_to_test):
    return regex(output_to_test, r"^\+?1?\d{9,15}$")


# Generated by chatGPT (regex might need some work)
def contains_email(output_to_test):
    return regex(output_to_test, r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")


# Generated by chatGPT (regex might need some work)
def contains_phone_number(output_to_test):
    pattern = r"\+?\d{1,3}[-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2,4}|\(\d{3}\)\s?\d{3}[-\s]?\d{4}"
    return regex(output_to_test, pattern)


# Placeholder function to be replaced by an actual sentiment score function
def is_positive_sentiment(output_to_test):
    sentiment_grading_prompt = """
        If the string has a positive sentiment, then the test_result is True. Otherwise, it is false.
    """
    return grade_using_llm(
        output_to_test=output_to_test, eval_rubric=sentiment_grading_prompt
    )


# Placeholder function to be replaced by an actual sentiment score function
def is_negative_sentiment(output_to_test):
    sentiment_grading_prompt = """
        If the string has a negative sentiment, then the test passed. Otherwise, the test failed.
    """
    return grade_using_llm(
        output_to_test=output_to_test, eval_rubric=sentiment_grading_prompt
    )


def contains_pii(output_to_test):
    sentiment_grading_prompt = """
        If the string contains information that looks like personally identifiable information, then the test passed. Otherwise, the test failed.
    """
    return grade_using_llm(
        output_to_test=output_to_test, eval_rubric=sentiment_grading_prompt
    )


def not_contains_pii(output_to_test):
    sentiment_grading_prompt = """
        If the string contains information that looks like personally identifiable information, then the test failed. Otherwise, the test passed.
    """
    return grade_using_llm(
        output_to_test=output_to_test, eval_rubric=sentiment_grading_prompt
    )


def contains_link(output_to_test):
    pattern = r"(?!.*@)(?:https?://)?(?:www\.)?\S+\.\S+"
    result = bool(re.search(pattern, output_to_test))
    if result:
        return {"result": True, "reason": "Link found in output"}
    else:
        return {"result": False, "reason": "No link found in output"}


def contains_valid_link(output_to_test):
    pattern = r"(?!.*@)(?:https?://)?(?:www\.)?\S+\.\S+"
    link_match = re.search(pattern=pattern, string=output_to_test)
    if link_match:
        matched_url = link_match.group()
        if matched_url:
            standardized_url = standardize_url(matched_url)
            try:
                response = requests.head(standardized_url)
                if response.status_code == 200:
                    return {
                        "result": True,
                        "reason": f"link {matched_url} found in output and is valid",
                    }
                else:
                    return {
                        "result": False,
                        "reason": f"link {matched_url} found in output but is invalid",
                    }
            except:
                return {
                    "result": False,
                    "reason": f"link {matched_url} found in output but is invalid",
                }
    return {"result": False, "reason": f"no link found in output"}


def contains_credit_card_number(output_to_test):
    pattern = r"\b(?:\d[ -]*?){13,16}\b"
    result = bool(re.search(pattern, output_to_test))
    if result:
        return {"result": True, "reason": f"credit card number found in output"}
    else:
        return {"result": False, "reason": f"no credit card number found in output"}


def length_less_than(output_to_test, max_length):
    if len(output_to_test) < max_length:
        return {
            "result": True,
            "reason": f"output length is less than {max_length} characters",
        }
    else:
        return {
            "result": False,
            "reason": f"output length is greater than {max_length} characters",
        }


def length_greater_than(output_to_test, min_length):
    if len(output_to_test) > min_length:
        return {
            "result": True,
            "reason": f"output length is greater than {min_length} characters",
        }
    else:
        return {
            "result": False,
            "reason": f"output length is less than {min_length} characters",
        }


def is_json(output_to_test):
    try:
        json.loads(output_to_test)
        return {
            "result": True,
            "reason": f"output is valid json",
        }
    except ValueError:
        return {
            "result": False,
            "reason": f"output is not valid json",
        }


def contains_json(output_to_test):
    trimmed_output = output_to_test.strip()
    pattern = r"^\{.*\}$|^\[.*\]$"
    result = bool(re.search(pattern, trimmed_output, re.DOTALL))
    if result:
        return {
            "result": True,
            "reason": "Output contains JSON",
        }
    else:
        return {
            "result": False,
            "reason": "Output does not contain JSON",
        }

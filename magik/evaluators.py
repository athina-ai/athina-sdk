# Contains functions to evaluate assertions.
import requests
import json
import re
import ast
import numpy as np
from magik.openai_helper import OpenAI
from magik.utils import standardize_url, generate_grading_prompt
from magik.constants import OPEN_AI_DEFAULT_MODEL
from magik.decorators import magik_eval
from magik.similarity import similarity_score
from magik.classifier import classify_output


@magik_eval
def equals(expected_output, case_sensitive=False, output_to_test=None):
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


@magik_eval
def contains_all(keywords, case_sensitive=False, output_to_test=None):
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


@magik_eval
def contains_any(keywords, case_sensitive=False, output_to_test=None):
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


@magik_eval
def contains_none(keywords, case_sensitive=False, output_to_test=None):
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


@magik_eval
def negate(eval_function, output_to_test=None, *args, **kwargs):
    eval_result = eval_function(output_to_test=output_to_test, *args, **kwargs)
    return {
        "result": not eval_result["result"],
        "reason": f"Negated function {eval_function.__name__} returned {eval_result['result']} with reason '{eval_result['reason']}'",
    }


@magik_eval
def contains(keyword, case_sensitive=False, output_to_test=None):
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


@magik_eval
def regex(pattern, output_to_test=None):
    match = re.search(pattern, output_to_test)
    if match:
        return {"result": True, "reason": f"regex pattern {pattern} found in output"}
    else:
        return {
            "result": False,
            "reason": f"regex pattern {pattern} not found in output",
        }


@magik_eval
def starts_with(substring, case_sensitive=False, output_to_test=None):
    if case_sensitive == False:
        output_to_test = output_to_test.lower()
        substring = substring.lower()
    result = output_to_test.startswith(substring)
    if result == True:
        return {"result": result, "reason": "output starts with " + substring}
    else:
        return {"result": result, "reason": "output does not start with " + substring}


@magik_eval
def ends_with(substring, case_sensitive=False, output_to_test=None):
    if case_sensitive == False:
        output_to_test = output_to_test.lower()
        substring = substring.lower()
    result = output_to_test.endswith(substring)
    if result == True:
        return {"result": result, "reason": "output ends with " + substring}
    else:
        return {"result": result, "reason": "output does not end with " + substring}


@magik_eval
def grade_using_llm(eval_rubric, output_to_test=None):
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


@magik_eval
def is_email(output_to_test=None):
    return regex(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")(output_to_test)


@magik_eval
def is_phone_number(output_to_test=None):
    return regex(r"^\+?1?\d{9,15}$")(output_to_test)


# Generated by chatGPT (regex might need some work)
@magik_eval
def contains_email(output_to_test=None):
    return regex(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")(output_to_test)


# Generated by chatGPT (regex might need some work)
@magik_eval
def contains_phone_number(output_to_test=None):
    pattern = r"\+?\d{1,3}[-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2,4}|\(\d{3}\)\s?\d{3}[-\s]?\d{4}"
    return regex(pattern)(output_to_test)


# Placeholder function to be replaced by an actual sentiment score function
@magik_eval
def is_positive_sentiment(output_to_test=None):
    sentiment_grading_prompt = """
        If the string has a positive sentiment, then the test_result is True. Otherwise, it is false.
    """
    return grade_using_llm(sentiment_grading_prompt)(output_to_test)


# Placeholder function to be replaced by an actual sentiment score function
@magik_eval
def is_negative_sentiment(output_to_test=None):
    sentiment_grading_prompt = """
        If the string has a negative sentiment, then the test passed. Otherwise, the test failed.
    """
    return grade_using_llm(sentiment_grading_prompt)(output_to_test)


@magik_eval
def contains_pii(output_to_test=None):
    sentiment_grading_prompt = """
        If the string contains information that looks like personally identifiable information, then the test passed. Otherwise, the test failed.
    """
    return grade_using_llm(sentiment_grading_prompt)(output_to_test)


@magik_eval
def not_contains_pii(output_to_test=None):
    sentiment_grading_prompt = """
        If the string contains information that looks like personally identifiable information, then the test failed. Otherwise, the test passed.
    """
    return grade_using_llm(sentiment_grading_prompt)(output_to_test)


@magik_eval
def contains_link(output_to_test=None):
    pattern = r"(?!.*@)(?:https?://)?(?:www\.)?\S+\.\S+"
    print("output_to_test", output_to_test)
    result = bool(re.search(pattern, output_to_test))
    if result:
        return {"result": True, "reason": "Link found in output"}
    else:
        return {"result": False, "reason": "No link found in output"}


@magik_eval
def contains_valid_link(output_to_test=None):
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


@magik_eval
def contains_credit_card_number(output_to_test=None):
    pattern = r"\b(?:\d[ -]*?){13,16}\b"
    result = bool(re.search(pattern, output_to_test))
    if result:
        return {"result": True, "reason": f"credit card number found in output"}
    else:
        return {"result": False, "reason": f"no credit card number found in output"}


@magik_eval
def length_less_than(max_length, output_to_test=None):
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


@magik_eval
def length_greater_than(min_length, output_to_test=None):
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


@magik_eval
def is_json(output_to_test=None):
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


@magik_eval
def contains_json(output_to_test=None):
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


@magik_eval
def cosine_similarity_above_threshold(
    compare_against: str,
    threshold: float,
    model="text-embedding-ada-002",
    output_to_test=None,
):
    score = similarity_score(output_to_test, compare_against, model)
    print(f"score is {score}")
    result = score > threshold
    return {
        "result": result,
        "reason": f"cosine similarity score is {score} and is above threshold {threshold}",
    }


@magik_eval
def cosine_similarity_below_threshold(
    compare_against: str,
    threshold: float,
    model="text-embedding-ada-002",
    output_to_test=None,
):
    score = similarity_score(output_to_test, compare_against, model)
    print(f"score is {score}")
    result = score < threshold
    return {
        "result": result,
        "reason": f"cosine similarity score is {score} and is below threshold {threshold}",
    }


@magik_eval
def matches_desired_classification(
    classification_labels_and_descriptions: list[dict],
    input_description: str,
    task_description: str,
    desired_classification_label: str,
    output_to_test=None,
):
    label = classify_output(
        classification_labels_and_descriptions=classification_labels_and_descriptions,
        input_description=input_description,
        task_description=task_description,
        output_to_test=output_to_test,
    )
    result = label == desired_classification_label
    return {
        "result": result,
        "reason": f"output is classified as {label} and desired classification is {desired_classification_label}",
    }

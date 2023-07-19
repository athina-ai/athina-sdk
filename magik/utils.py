# Normalize the output to a testable format
def normalize_output_string(str):
    str = str.replace("\n", "")
    str = str.replace("\t", "")
    str = str.replace("'", "")
    str = str.replace('"', "")
    return str


def substitute_vars(string, vars_dict):
    return string.format(**vars_dict)


def standardize_url(url):
    if url.startswith("http://") or url.startswith("https://"):
        return url
    else:
        return "http://" + url


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

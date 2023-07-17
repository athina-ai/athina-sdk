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

# Normalize the output to a testable format
def normalize_output_string(str):
    str = str.replace("\n", "")
    str = str.replace("\t", "")
    str = str.replace("'", "")
    str = str.replace('"', "")
    return str

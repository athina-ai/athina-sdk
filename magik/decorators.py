def magik_eval(func):
    def wrapper(*args):
        return lambda output_to_test: func(*args, output_to_test=output_to_test)

    return wrapper

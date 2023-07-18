def magik_eval(func):
    def wrapper(*args, **kwargs):
        return lambda output_to_test: func(
            *args, **kwargs, output_to_test=output_to_test
        )

    return wrapper

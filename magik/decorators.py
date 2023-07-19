def magik_eval(func):
    def wrapper(*args, **kwargs):
        wrapped_func = lambda output_to_test: func(
            *args, **kwargs, output_to_test=output_to_test
        )

        # Convert each value to a string and join them with commas, with strings wrapped in quotes
        arg_string = ", ".join(
            f"'{value}'"
            if isinstance(value, str)
            else value.__name__
            if callable(value)
            else str(value)
            for value in args
        )

        wrapped_func.__name__ = f"{func.__name__}({arg_string})"
        return wrapped_func

    return wrapper

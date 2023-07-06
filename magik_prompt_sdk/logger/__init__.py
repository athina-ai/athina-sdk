import logging
import colorlog


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CLIAppLogger(logging.Logger, metaclass=Singleton):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

        # Create a console handler with color support
        console_handler = colorlog.StreamHandler()
        console_handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(log_color)s[%(levelname)s]: %(message)s",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            )
        )
        self.addHandler(console_handler)


def setup_logger():
    logger = CLIAppLogger("cli_logger", level=logging.DEBUG)
    return logger


# Create a default logger instance
logger = setup_logger()

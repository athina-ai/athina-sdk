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
                "%(log_color)s%(message)s",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "white",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            )
        )
        self.addHandler(console_handler)

    def success(self, message):
        self.info(f"\033[32m{message}\033[0m")  # Output info log in green

    def error(self, message, *args, **kwargs):
        super().error("ERROR: " + message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        super().warning("WARN: " + message, *args, **kwargs)

    def log_with_color(self, message, color, *args, **kwargs):
        colors = {
            "black": "30",
            "red": "31",
            "green": "32",
            "yellow": "33",
            "blue": "34",
            "magenta": "35",
            "cyan": "36",
            "white": "37",
        }

        color_code = colors.get(color.lower(), "37")
        formatted_message = f"\033[{color_code}m{message}\033[0m"
        print(formatted_message, *args, **kwargs)


def setup_logger():
    logger = CLIAppLogger("cli_logger", level=logging.INFO)
    return logger


# Create a default logger instance
logger = setup_logger()

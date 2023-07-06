#!/usr/bin/env python3

import argparse
from magik_prompt_sdk.generate import generate_test
from magik_prompt_sdk.logger import logger

commands = {
    "generate": generate_test,
    "run": generate_test,
    "deploy": generate_test,
}


def main():
    parser = argparse.ArgumentParser(
        description="Generate, run, and deploy unit tests for your AI app"
    )
    parser.add_argument("cmd", help="Command to execute")
    parser.add_argument("test_name", help="Name of the test")

    args = parser.parse_args()
    cmd = args.cmd
    test_name = args.test_name

    if not cmd or not test_name:
        print("Missing arguments")
        return

    if cmd not in commands:
        print(f"Error: Command {cmd} not found")
        return
    command_function = commands[cmd]

    command_function(test_name)


if __name__ == "__main__":
    main()

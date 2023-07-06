#!/usr/bin/env python3

import argparse
from magik_prompt_sdk.initialize import initialize
from magik_prompt_sdk.generate import generate_test
from magik_prompt_sdk.run import run_tests
from magik_prompt_sdk.deploy import deploy_test
from magik_prompt_sdk.logger import logger

commands = {
    "init": initialize,
    "generate": generate_test,
    "run": run_tests,
    "deploy": deploy_test,
}


def main():
    parser = argparse.ArgumentParser(
        description="Generate, run, and deploy unit tests for your AI app"
    )
    parser.add_argument("cmd", help="Command to execute")
    parser.add_argument("test_name", nargs="?", help="Name of the test (optional)")

    args = parser.parse_args()
    cmd = args.cmd
    test_name = args.test_name

    if not cmd:
        logger.error("Missing command")
        return

    if cmd not in commands:
        logger.error(f"Error: Command {cmd} not found")
        return

    command_function = commands[cmd]
    if (cmd in ["generate", "run", "deploy"]) and not test_name:
        logger.info(
            f"Please provide a test_name argument as well.\n\nUsage: magik {cmd} <test_name>"
        )
        return

    if test_name:
        command_function(test_name)
    else:
        command_function()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
from magik.initialize import initialize
from magik.generate import generate_test
from magik.deploy import deploy_test
from magik.internal_logger import logger
from magik.run import Run

commands = [
    "init",
    "generate",
    "run",
    "deploy",
]


def main():
    parser = argparse.ArgumentParser(
        description="Generate, run, and deploy unit tests for your AI app"
    )
    parser.add_argument("cmd", help="Command to execute")
    parser.add_argument("test_name", nargs="?", help="Name of the test (optional)")
    parser.add_argument(
        "--prod", action="store_true", help="Flag for production environment"
    )
    parser.add_argument("--start_date", help="Start date (optional)")
    parser.add_argument("--end_date", help="End date (optional)")
    parser.add_argument("--prompt_slug", help="Prompt slug (optional)")

    args = parser.parse_args()
    cmd = args.cmd
    test_name = args.test_name
    is_production = args.prod if hasattr(args, "prod") else False
    start_date = args.start_date
    end_date = args.end_date
    prompt_slug = args.prompt_slug

    if not cmd:
        logger.error("Missing command")
        return

    if cmd not in commands:
        logger.error(f"Error: Command '{cmd}' not found")
        return

    if (cmd in ["generate", "deploy"]) and not test_name:
        logger.info(
            f"Please provide a test_name argument as well.\n\nUsage: magik {cmd} <test_name>"
        )
        return

    if cmd == "init":
        initialize()
        return

    if cmd == "generate":
        generate_test(test_name)
        return

    if cmd == "run" and not is_production:
        test_runner = Run()
        test_runner.run_tests(test_name)
        return

    if cmd == "run" and is_production:
        if not start_date or not end_date:
            logger.info(
                f"Please provide a start_date and end_date argument as well.\n\nUsage: magik run <test_name> --prod --start_date <start_date> --end_date <end_date>"
            )
            return

        test_runner = Run()
        test_runner.run_tests_in_prod(
            start_date=start_date,
            end_date=end_date,
            prompt_slug=prompt_slug,
        )
        return

    if cmd == "deploy":
        deploy_test(test_name)
        return


if __name__ == "__main__":
    main()

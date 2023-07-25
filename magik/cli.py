#!/usr/bin/env python3

import argparse
from magik.initialize import initialize
from magik.generate import generate_test
from magik.deploy import deploy_test
from magik.internal_logger import logger
from magik.constants import TEST_DIR, TEST_RUNS_DIR
from magik.run import Run


def main():
    parser = argparse.ArgumentParser(
        prog="magik", description="Magik testing suite CLI tool"
    )

    subparsers = parser.add_subparsers(title="commands", dest="command")

    # magik init
    parser_init = subparsers.add_parser("init", help="Initialize magik testing suite")
    parser_init.set_defaults(func=init)

    # magik generate <test-name>
    parser_generate = subparsers.add_parser("generate", help="Generate a new test")
    parser_generate.add_argument("test_name", help="Name of the test")
    parser_generate.set_defaults(func=generate)

    # magik run <test-name>
    parser_run = subparsers.add_parser("run", help="Run a test")
    parser_run.add_argument("test_name", help="Name of the test")
    parser_run.set_defaults(func=run)

    # magik deploy <test-name>
    parser_deploy = subparsers.add_parser("deploy", help="Deploy a test")
    parser_deploy.add_argument("test_name", help="Name of the test")
    parser_deploy.set_defaults(func=deploy)

    # magik run_prod --prod --test <test-name> --prompt <prompt-slug> --start_date <start-date> --end_date <end_date>
    parser_run_production = subparsers.add_parser(
        "run_prod", help="Run a test in production"
    )
    parser_run_production.add_argument(
        "--test", dest="test_name", help="Name of the test", required=False, default="*"
    )
    parser_run_production.add_argument(
        "--prompt", dest="prompt_slug", help="Slug of the prompt", required=True
    )
    parser_run_production.add_argument("--start_date", help="Start date of the test")
    parser_run_production.add_argument("--end_date", help="End date of the test")
    parser_run_production.set_defaults(func=run_prod)

    args = parser.parse_args()
    args.func(args)


def init(args):
    initialize()


def generate(args):
    generate_test(args.test_name)


def run(args):
    test_runner = Run(test_dir=TEST_DIR, test_runs_dir=TEST_RUNS_DIR)
    test_runner.run_tests(args.test_name)


def deploy(args):
    deploy_test(args.test_name)


def run_prod(args):
    test_runner = Run(test_dir=TEST_DIR, test_runs_dir=TEST_RUNS_DIR)
    test_runner.run_tests_in_prod(
        start_date=args.start_date,
        end_date=args.end_date,
        prompt_slug=args.prompt_slug,
        test_slug=args.test_name,
    )


if __name__ == "__main__":
    main()

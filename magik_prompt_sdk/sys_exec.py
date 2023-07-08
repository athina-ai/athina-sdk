import asyncio
import os
import json
import subprocess
from magik_prompt_sdk.logger import logger


def execute_command(command, confirm=True, log=True):
    if confirm:
        confirmation = input(f"Run '{command}'? (y/n)")
        if confirmation != "y":
            return

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        if log:
            logger.info(command)
        output = result.stdout
        if log:
            logger.info(output)
        return output
    else:
        if log:
            logger.info(command)
        error = result.stderr
        if log:
            logger.error("error:" + error)
        return error


async def execute_command_async(command, confirm=True, log=True):
    logger.info(f"executing command {command}")
    if confirm:
        confirmation = input(f"Run '{command}'? (y/n)")
        if confirmation != "y":
            return

    # Create a new subprocess, redirect the standard output into a pipe
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    # Read output
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        if log:
            logger.info(command)
        output = stdout.decode()
        if log:
            logger.info(output)
        return output
    else:
        if log:
            print(command)
        error = stderr.decode()
        if log:
            logger.error("error:" + error)
        return error


def file_exists(filepath):
    return os.path.isfile(filepath)


def create_file(filepath):
    directory = os.path.dirname(filepath)
    os.makedirs(
        directory, exist_ok=True
    )  # Create parent directories if they don't exist
    open(filepath, "a").close()  # Create an empty file at the specified filepath


def touch(file_path, confirm=False):
    execute_command(f"touch {file_path}", confirm=confirm)


def write_to_file(file_path, content):
    directory = os.path.dirname(file_path)

    try:
        # Check if directory exists, create it if necessary
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, "w") as file:
            file.write(content)
        logger.debug(f"Successfully wrote to file: {file_path}")
    except IOError as e:
        logger.error(f"Error writing to file: {e}")


def append_to_file(file_path, data):
    write_to_file(file_path, data, mode="a")


def read_from_file(file_path):
    if file_exists(file_path) == False:
        raise Exception(f"File does not exist at {file_path}")
    try:
        with open(file_path, "r") as file:
            data = file.read()
        return data
    except IOError:
        raise Exception(f"Error reading from file: {file_path}")


def read_json_file(file_path):
    data = None
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

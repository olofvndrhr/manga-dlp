import os
import subprocess

from loguru import logger as log


def run_hook(command: str, hook_type: str, **kwargs) -> int:
    """
    Args:
        command (str): command to run
        hook_type (str): type of the hook
        kwargs: key value pairs of env vars to set

    Returns:
        exit_code (int): exit code of command
    """

    # check if hook commands are empty
    if not command or command == "None":
        log.debug(f"Hook '{hook_type}' empty. Not running")
        return 2

    command_list = command.split(" ")

    # setting env vars
    for key, value in kwargs.items():
        os.environ[f"MDLP_{key.upper()}"] = str(value)

    # running command
    log.info(f"Hook '{hook_type}' - running command: '{command}'")
    proc = subprocess.run(command_list, check=False, timeout=15, encoding="utf8")
    exit_code = proc.returncode

    if exit_code == 0:
        log.debug("Hook returned status code 0. All good")
    else:
        log.warning(f"Hook returned status code {exit_code}. Possible error")

    # return exit code of command
    return exit_code

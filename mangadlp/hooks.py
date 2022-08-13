import os
import subprocess

from mangadlp.logger import Logger

# prepare logger
log = Logger(__name__)


class Hooks:
    """Pre- and post-hooks for each download.

    Args:
        cmd_manga_pre (str): Commands to execute before the manga download starts
        cmd_manga_post (str): Commands to execute after the manga download finished
        cmd_chapter_pre (str): Commands to execute before the chapter download starts
        cmd_chapter_post (str): Commands to execute after the chapter download finished

    """

    def __init__(
        self,
        cmd_manga_pre: str,
        cmd_manga_post: str,
        cmd_chapter_pre: str,
        cmd_chapter_post: str,
    ) -> None:
        self.cmd_manga_pre = cmd_manga_pre
        self.cmd_manga_post = cmd_manga_post
        self.cmd_chapter_pre = cmd_chapter_pre
        self.cmd_chapter_post = cmd_chapter_post

    def run(self, hook_type: str, hook_status: dict, hook_info: dict) -> int:
        if hook_type == "manga_pre":
            hook_cmd_str = self.cmd_manga_pre
        elif hook_type == "manga_post":
            hook_cmd_str = self.cmd_manga_post
        elif hook_type == "chapter_pre":
            hook_cmd_str = self.cmd_chapter_pre
        elif hook_type == "chapter_post":
            hook_cmd_str = self.cmd_chapter_post
        else:
            log.error(f"Hook type '{hook_type}' is not valid. Not running")
            return 1

        # check if hook commands are empty
        if not hook_cmd_str or hook_cmd_str == "None":
            log.verbose(f"Hook '{hook_type}' empty. Not running")
            return 2

        hook_cmd_list = hook_cmd_str.split(" ")

        # setting env vars
        hook_info["hook_type"] = hook_type
        hook_info["status"] = hook_status.get("status")
        hook_info["reason"] = hook_status.get("reason")

        for key, value in hook_info.items():
            os.environ[f"MDLP_{key.upper()}"] = str(value)

        # running command
        log.info(f"Hook '{hook_type}' - running command: '{hook_cmd_str}'")
        ecode = subprocess.call(hook_cmd_list)

        if ecode == 0:
            log.verbose("Hook returned status code 0. All good")
        else:
            log.warning(f"Hook returned status code {ecode}. Possible error")

        # return exit code of command
        return ecode

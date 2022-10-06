import logging

DATE_FMT = "%Y-%m-%dT%H:%M:%S%z"


# prepare custom levels and default config of logger
def prepare_logger():
    logging.basicConfig(
        format="%(asctime)s | [%(levelname)s] [%(name)s]: %(message)s",
        datefmt=DATE_FMT,
        level=20,
        handlers=[logging.StreamHandler()],
    )
    logging.addLevelName(level=15, levelName="VERBOSE")
    logging.addLevelName(level=25, levelName="LEAN")


# set log message format
def format_logger(verbosity: int):
    logging.getLogger().setLevel(verbosity)

    # dont show log level name on default/lean logging
    if verbosity >= 20:
        logging.basicConfig(
            format="%(asctime)s | %(message)s",
            datefmt=DATE_FMT,
            force=True,
        )
    else:
        logging.basicConfig(
            format="%(asctime)s | [%(levelname)s] [%(name)s]: %(message)s",
            datefmt=DATE_FMT,
            force=True,
        )


class Logger:
    """Default logger for manga-dlp.

    Args:
        name (str): Name of the logger

    """

    def __init__(self, name: str):
        self.name = name
        # create logger
        self.log = logging.getLogger(self.name)

    # custom log levels
    def verbose(self, message: str):
        self.log.log(level=15, msg=message)

    def lean(self, message: str):
        self.log.log(level=25, msg=message)

    # default log levels
    def critical(self, message: str):
        self.log.critical(msg=message)

    def error(self, message: str):
        self.log.error(msg=message)

    def warning(self, message: str):
        self.log.warning(msg=message)

    def info(self, message: str):
        self.log.info(msg=message)

    def debug(self, message: str):
        self.log.debug(msg=message)

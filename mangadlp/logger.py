import logging
import sys

from loguru import logger

LOGGING_FMT: str = (
    "%(asctime)s | (D) [%(levelname)-7s] [%(name)-10s] [%(funcName)-20s]: %(message)s"
)
LOGURU_FMT: str = "{time:%Y-%m-%dT%H:%M:%S%z} | (C) <level>[{level: <7}]</level> [{name: <10}] [{function: <20}]: {message}"


def enable_default_logger(loglevel: int) -> None:
    logging.root.handlers = []

    logging.basicConfig(
        format=LOGGING_FMT,
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        level=loglevel,
        handlers=[logging.StreamHandler()],
    )


# create config for a normal stderr logger
def prepare_logger(loglevel: int) -> None:
    config: dict = {
        "handlers": [
            {
                "sink": sys.stdout,
                "level": loglevel,
                "format": LOGURU_FMT,
            },
        ],
    }
    logger.configure(**config)
    enable_default_logger(loglevel)

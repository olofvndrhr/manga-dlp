import logging
import sys
from typing import Any, Dict

from loguru import logger


LOGURU_FMT = "{time:%Y-%m-%dT%H:%M:%S%z} | <level>[{level: <7}]</level> [{name: <10}] [{function: <20}]: {message}"


# from loguru docs
class InterceptHandler(logging.Handler):
    """Intercept python logging messages and log them via loguru.logger."""

    def emit(self, record: Any) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


# init logger with format and log level
def prepare_logger(loglevel: int = 20) -> None:
    stdout_handler: Dict[str, Any] = {
        "sink": sys.stdout,
        "level": loglevel,
        "format": LOGURU_FMT,
    }

    logging.basicConfig(handlers=[InterceptHandler()], level=loglevel)
    logger.configure(handlers=[stdout_handler])

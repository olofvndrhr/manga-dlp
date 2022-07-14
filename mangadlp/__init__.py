import logging

from mangadlp.logger import logger_lean, logger_verbose

# prepare logger with default level INFO==20
logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=20,
    handlers=[logging.StreamHandler()],
)

# create custom log levels
logging.addLevelName(15, "VERBOSE")
logging.VERBOSE = 15  # type: ignore
logging.verbose = logger_verbose  # type: ignore
logging.Logger.verbose = logger_verbose  # type: ignore

logging.addLevelName(25, "LEAN")
logging.VERBOSE = 25  # type: ignore
logging.lean = logger_lean  # type: ignore
logging.Logger.lean = logger_lean  # type: ignore

import logging

# prepare logger
logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)


def logger_verbose(msg, *args, **kwargs):
    if logging.getLogger().isEnabledFor(15):
        logging.log(15, msg)


def logger_lean(msg, *args, **kwargs):
    if logging.getLogger().isEnabledFor(25):
        logging.log(25, msg)


logging.addLevelName(15, "VERBOSE")
logging.verbose = logger_verbose  # type: ignore
logging.Logger.verbose = logger_verbose  # type: ignore

logging.addLevelName(25, "LEAN")
logging.lean = logger_lean  # type: ignore
logging.Logger.lean = logger_lean  # type: ignore

import logging

# prepare logger with default level INFO==20
logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=20,
    handlers=[logging.StreamHandler()],
)


# create verbose logger with level 15
def logger_verbose(msg, *args, **kwargs):
    if logging.getLogger().isEnabledFor(15):
        logging.log(15, msg)


# create lean logger with level 25
def logger_lean(msg, *args, **kwargs):
    if logging.getLogger().isEnabledFor(25):
        logging.log(25, msg)


logging.addLevelName(15, "VERBOSE")
logging.VERBOSE = 15  # type: ignore
logging.verbose = logger_verbose  # type: ignore
logging.Logger.verbose = logger_verbose  # type: ignore

logging.addLevelName(25, "LEAN")
logging.VERBOSE = 25  # type: ignore
logging.lean = logger_lean  # type: ignore
logging.Logger.lean = logger_lean  # type: ignore

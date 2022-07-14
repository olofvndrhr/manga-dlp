import logging


# set log message format
def format_logger(verbosity: int):
    logging.getLogger().setLevel(verbosity)

    # dont show log level name on default/lean logging
    if verbosity >= 20:
        logging.basicConfig(
            format="%(asctime)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            force=True,
        )
    else:
        logging.basicConfig(
            format="%(asctime)s | %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            force=True,
        )


# create verbose logger with level 15
def logger_verbose(msg, *args, **kwargs):
    if logging.getLogger().isEnabledFor(15):
        logging.log(15, msg)


# create lean logger with level 25
def logger_lean(msg, *args, **kwargs):
    if logging.getLogger().isEnabledFor(25):
        logging.log(25, msg)

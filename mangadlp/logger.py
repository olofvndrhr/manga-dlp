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
            format="%(asctime)s | [%(name)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            force=True,
        )

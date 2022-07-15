import logging

# prepare logger with default level INFO==20
logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=20,
    handlers=[logging.StreamHandler()],
)

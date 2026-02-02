import logging

from genaidrivenetl.config import LOG_FILE, LOG_FORMAT, LOGGING_LEVEL


def setup_logging(level=LOGGING_LEVEL):
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILE),
        ],
    )

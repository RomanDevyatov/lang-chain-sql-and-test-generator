import logging

from genaidrivenetl.config import Config


def setup_logging(level=Config.LOGGING_LEVEL):
    logging.basicConfig(
        level=level,
        format=Config.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(Config.LOG_FILE),
        ],
        force=True,
    )

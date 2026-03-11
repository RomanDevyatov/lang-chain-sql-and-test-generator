import logging
import sys

from genaidrivenetl.config import Config


def setup_logging(level=Config.LOGGING_LEVEL, is_stdout=False):
    logging.basicConfig(
        level=level,
        format=Config.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout) if is_stdout else logging.StreamHandler(),
            logging.FileHandler(Config.LOG_FILE),
        ],
        force=True,
    )

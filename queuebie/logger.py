import logging

from queuebie.settings import QUEUEBIE_LOGGER_NAME


def get_logger() -> logging.Logger:
    """
    Returns an instance of a queuebie Django logger
    """
    return logging.getLogger(QUEUEBIE_LOGGER_NAME)

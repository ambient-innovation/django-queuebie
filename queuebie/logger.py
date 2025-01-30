import logging

from queuebie.settings import get_queuebie_logger_name


def get_logger() -> logging.Logger:
    """
    Returns an instance of a queuebie Django logger
    """
    return logging.getLogger(get_queuebie_logger_name())

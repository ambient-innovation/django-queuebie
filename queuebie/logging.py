import logging

from queuebie.settings import QUEUEBIE_LOGGER_NAME


def get_logger() -> logging.Logger:
    # todo: write test
    # TODO: add docs about how to set up logger
    return logging.getLogger(QUEUEBIE_LOGGER_NAME)

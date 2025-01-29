import logging

from queuebie.logger import get_logger
from queuebie.settings import QUEUEBIE_LOGGER_NAME


def test_get_logger():
    logger = get_logger()

    assert isinstance(logger, logging.Logger)
    assert logger.name == QUEUEBIE_LOGGER_NAME

import logging

from queuebie.logger import get_logger
from queuebie.settings import get_queuebie_logger_name


def test_get_logger():
    logger = get_logger()

    assert isinstance(logger, logging.Logger)
    assert logger.name == get_queuebie_logger_name()

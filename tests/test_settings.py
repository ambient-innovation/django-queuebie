from django.conf import settings
from django.test import override_settings

from queuebie.settings import (
    get_queuebie_app_base_path,
    get_queuebie_cache_key,
    get_queuebie_logger_name,
    get_queuebie_strict_mode,
)


@override_settings(QUEUEBIE_APP_BASE_PATH="/path/to/queuebie")
def test_get_queuebie_app_base_path_is_set():
    assert get_queuebie_app_base_path() == "/path/to/queuebie"


def test_get_queuebie_app_base_path_default_used():
    assert get_queuebie_app_base_path() == settings.BASE_PATH


@override_settings(QUEUEBIE_CACHE_KEY="new_cache_key")
def test_get_queuebie_cache_key_is_set():
    assert get_queuebie_cache_key() == "new_cache_key"


def test_get_queuebie_cache_key_default_used():
    assert get_queuebie_cache_key() == "queuebie"


@override_settings(QUEUEBIE_LOGGER_NAME="my_logger")
def test_get_queuebie_logger_name_is_set():
    assert get_queuebie_logger_name() == "my_logger"


def test_get_queuebie_logger_name_default_used():
    assert get_queuebie_logger_name() == "queuebie"


@override_settings(QUEUEBIE_STRICT_MODE=False)
def test_get_queuebie_strict_mode_is_set():
    assert get_queuebie_strict_mode() is False


def test_get_queuebie_strict_mode_default_used():
    assert get_queuebie_strict_mode() is True

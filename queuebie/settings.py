from pathlib import Path

from django.conf import settings


def get_queuebie_app_base_path() -> Path | str:
    """
    Base path of the application queuebie should look for registered handlers.
    :return:
    """
    return getattr(settings, "QUEUEBIE_APP_BASE_PATH", getattr(settings, "BASE_PATH", None))


def get_queuebie_cache_key() -> str:
    """
    Cache key to store registered handlers in.
    """
    return getattr(settings, "QUEUEBIE_CACHE_KEY", "queuebie")


def get_queuebie_logger_name() -> str:
    """
    Django logger name
    """
    return getattr(settings, "QUEUEBIE_LOGGER_NAME", "queuebie")


def get_queuebie_strict_mode() -> bool:
    """
    Determines if commands are allowed to be handled outside the scope they are defined in.
    """
    return getattr(settings, "QUEUEBIE_STRICT_MODE", True)


def get_queuebie_excluded_directories() -> set[str]:
    """
    Directory names which are skipped when searching for handler modules.
    """
    return set(getattr(settings, "QUEUEBIE_EXCLUDED_DIRECTORIES", {"tests", "migrations", "__pycache__"}))

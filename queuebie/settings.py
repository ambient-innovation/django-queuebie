from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


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
    excluded_directories = getattr(settings, "QUEUEBIE_EXCLUDED_DIRECTORIES", {"tests", "migrations", "__pycache__"})

    # A string would decay into a set of single characters, silently excluding the wrong directories
    if isinstance(excluded_directories, str):
        raise ImproperlyConfigured(  # noqa: TRY003
            "QUEUEBIE_EXCLUDED_DIRECTORIES has to be a collection of directory names, not a string."
        )

    return set(excluded_directories)

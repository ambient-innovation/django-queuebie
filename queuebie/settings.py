from pathlib import Path

from django.conf import settings

from queuebie.exceptions import InvalidExcludedDirectoriesError

DEFAULT_EXCLUDED_DIRECTORIES = {
    "__pycache__",
    "fixtures",
    "locale",
    "media",
    "migrations",
    "node_modules",
    "static",
    "templates",
    "tests",
}


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


def get_queuebie_default_excluded_directories() -> set[str]:
    """
    Directory names which occur inside Django apps but never hold message handlers.
    """
    return _directory_names(setting_name="QUEUEBIE_DEFAULT_EXCLUDED_DIRECTORIES", default=DEFAULT_EXCLUDED_DIRECTORIES)


def get_queuebie_excluded_directories() -> set[str]:
    """
    Directory names which are skipped when searching for handler modules.
    """
    return get_queuebie_default_excluded_directories() | _directory_names(
        setting_name="QUEUEBIE_EXCLUDED_DIRECTORIES", default=set()
    )


def _directory_names(*, setting_name: str, default: set[str]) -> set[str]:
    directory_names = getattr(settings, setting_name, default)

    # A string would decay into a set of single characters, silently excluding the wrong directories
    if isinstance(directory_names, str):
        raise InvalidExcludedDirectoriesError(setting_name=setting_name)

    return set(directory_names)

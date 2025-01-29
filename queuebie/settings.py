from pathlib import Path

from django.conf import settings

QUEUEBIE_APP_BASE_PATH: Path | str = getattr(settings, "QUEUEBIE_APP_BASE_PATH", getattr(settings, "BASE_PATH", None))
QUEUEBIE_CACHE_KEY: str = getattr(settings, "QUEUEBIE_CACHE_KEY", "queuebie")
QUEUEBIE_LOGGER_NAME: str = getattr(settings, "QUEUEBIE_LOGGER_NAME", "queuebie")
QUEUEBIE_STRICT_MODE: bool = getattr(settings, "QUEUEBIE_STRICT_MODE", True)

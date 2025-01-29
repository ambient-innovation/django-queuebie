from pathlib import Path

from django.conf import settings

QUEUEBIE_APP_BASE_PATH: Path | str = getattr(settings, "DJANGO_QUEUEBIE_APP_BASE_PATH", settings.BASE_PATH)
QUEUEBIE_LOGGER_NAME: str = getattr(settings, "DJANGO_QUEUEBIE_LOGGER_NAME", "queuebie")
QUEUEBIE_CACHE_KEY: str = getattr(settings, "DJANGO_QUEUEBIE_CACHE_KEY", "queuebie")

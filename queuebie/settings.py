from pathlib import Path

from django.conf import settings

# TODO: use me
# TODO: write test
QUEUEBIE_APP_BASE_PATH: Path | str = getattr(settings, "QUEUEBIE_APP_BASE_PATH", settings.BASE_PATH)
QUEUEBIE_LOGGER_NAME: str = getattr(settings, "DJANGO_PONY_EXPRESS_LOGGER_NAME", "queuebie")

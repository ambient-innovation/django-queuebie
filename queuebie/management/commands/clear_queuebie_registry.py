from django.core.cache import cache
from django.core.management.base import BaseCommand

from queuebie.logger import get_logger


class Command(BaseCommand):
    def handle(self, *args, **options):
        # TODO: use constants in settings for cache names
        # TODO: document me
        cache.delete("commands")
        cache.delete("events")

        logger = get_logger()
        logger.info("Queuebie registry cleared.")

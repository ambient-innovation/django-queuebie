from django.core.cache import cache
from django.core.management.base import BaseCommand

from queuebie.logger import get_logger
from queuebie.settings import get_queuebie_cache_key


class Command(BaseCommand):
    def handle(self, *args, **options):
        cache.delete(get_queuebie_cache_key())

        logger = get_logger()
        logger.info("Queuebie registry cleared.")

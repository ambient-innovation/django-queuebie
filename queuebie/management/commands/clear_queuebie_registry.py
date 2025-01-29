from django.core.cache import cache
from django.core.management.base import BaseCommand

from queuebie.logger import get_logger
from queuebie.settings import QUEUEBIE_CACHE_KEY


class Command(BaseCommand):
    def handle(self, *args, **options):
        # TODO: document me that this should go in the deployment process in the CI
        cache.delete(QUEUEBIE_CACHE_KEY)

        logger = get_logger()
        logger.info("Queuebie registry cleared.")

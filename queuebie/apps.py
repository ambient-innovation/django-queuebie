from django.apps import AppConfig

from queuebie import message_registry


class QueuebieConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "queuebie"

    def ready(self):
        super().ready()

        # Register all decorated functions before they get imported by something else which will break the
        # registration process since decorators are only executed the first time
        message_registry.autodiscover()

import sys
from pathlib import Path
from unittest import mock

from django.apps import AppConfig, apps

from queuebie import MessageRegistry
from queuebie.apps import QueuebieConfig


def test_app_config():
    app_config = apps.get_app_config("queuebie")

    assert isinstance(app_config, AppConfig)
    assert app_config.default_auto_field == "django.db.models.BigAutoField"
    assert app_config.name == "queuebie"


@mock.patch.object(MessageRegistry, "autodiscover")
def test_app_ready_autodiscover_called(mocked_autodiscover):
    config = QueuebieConfig(app_name="queuebie", app_module=sys.modules[__name__])
    config.path = str(Path(__file__).resolve().parent)
    config.ready()

    assert mocked_autodiscover.call_count == 1

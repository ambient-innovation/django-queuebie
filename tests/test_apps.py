from django.apps import AppConfig, apps


def test_app_config():
    app_config = apps.get_app_config("queuebie")

    assert isinstance(app_config, AppConfig)
    assert app_config.default_auto_field == "django.db.models.BigAutoField"
    assert app_config.name == "queuebie"

from pathlib import Path

BASE_PATH = Path(__file__).resolve(strict=True).parent

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "queuebie",
    "testapp",
)

DEBUG = False

ALLOWED_HOSTS = ["localhost:8000"]

SECRET_KEY = "ASDFjklö123456890"

# Routing
ROOT_URLCONF = "testapp.urls"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite",
    }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template_processors.debug",
                "django.template_processors.request",
                "django.contrib.auth_processors.auth",
                "django.contrib.messages_processors.messages",
            ],
            "debug": True,
        },
    },
]

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

USE_TZ = True
TIME_ZONE = "UTC"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "queuebie": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

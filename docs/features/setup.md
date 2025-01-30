# Setup

## Installation

- Install the package via pip: `pip install django_queuebie`
- Add module to `INSTALLED_APPS` within the main django `settings.py`:

```python
INSTALLED_APPS = (
    # ...
    "queuebie",
)
```

## Caching

Note that this packages uses the default cache defined in your Django application. It will store there the result of the
handler auto-discovery. If no cache is set up, the auto-discovery will run on every request.

To ensure that you don't keep artefacts in your cache once you deploy your code, you have to reset the Django cache. You
can do this via the default way that Django provides or you can use this management command

`python manage.py clear_queuebie_registry`

## Logging

You can set up a logger as you'd expect it from Django. Take care that the key `queuebie` here needs to reflect the
value of `QUEUEBIE_LOGGER_NAME`.

```python
# django settings
LOGGING = {
    "loggers": {
        "queuebie": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
```

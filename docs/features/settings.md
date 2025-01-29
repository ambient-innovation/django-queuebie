# Settings

## QUEUEBIE_APP_BASE_PATH

Queuebie needs to know where your project lives to detect local Django apps. It defaults to `settings.BASE_PATH`
but you can overwrite it with a string or a `Pathlib` object.

```python
from pathlib import Path

QUEUEBIE_APP_BASE_PATH = Path(__file__).resolve(strict=True).parent
```

## QUEUEBIE_CACHE_KEY

Queuebie will cache all detected message handlers in Django's default cache. The default cache key is "queuebie".
You can overwrite it with this variable.

```python
QUEUEBIE_CACHE_KEY = "my_very_special_cache_key"
```

## QUEUEBIE_LOGGER_NAME

Queuebie defines a Django logger with the default name "queuebie". If you want to rename that logger, you can set this
variable.

```python
QUEUEBIE_LOGGER_NAME = "my_very_special_logger"
```

## QUEUEBIE_STRICT_MODE

Queuebie enforces by default that commands are not used outside its domain (aka Django app). If you want to skip that
restriction for whatever reason, you can do so.

```python
QUEUEBIE_STRICT_MODE = False
```

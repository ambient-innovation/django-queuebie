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

Take care to use the same name in the logging configuration in your Django settings.

## QUEUEBIE_EXCLUDED_DIRECTORIES

Queuebie searches the whole subtree of every local Django app for `handlers/commands` and `handlers/events`
directories. Directory names listed here are skipped, which keeps handler-shaped trees that are not meant to be
registered - most notably a test suite mirroring your handler layout - out of the auto-discovery.

The default is `{"tests", "migrations", "__pycache__"}`. A directory is skipped when any part of its path below the
app root matches one of these names.

```python
QUEUEBIE_EXCLUDED_DIRECTORIES = {"tests", "migrations", "__pycache__", "fixtures"}
```

## QUEUEBIE_STRICT_MODE

Queuebie enforces by default that commands are not used outside their scope and event handlers don't talk to the
database. If you want to skip that restriction for whatever reason, you can do so.

```python
QUEUEBIE_STRICT_MODE = False
```

### What a scope is

The scope of a message or a handler is the package which owns the `handlers/` or `messages/` directory the module
lives in - the last such directory in the module path, so a package legitimately called `messages` further up doesn't
truncate the scope.

| Module                                             | Scope                    |
|----------------------------------------------------|--------------------------|
| `apps.shipping.messages.commands.shipment`           | `apps.shipping`          |
| `apps.shipping.handlers.commands.shipment`           | `apps.shipping`          |
| `apps.logistics.billing.handlers.commands.invoice`   | `apps.logistics.billing` |

A module which lives in neither directory has no owning package, so its full module path becomes its scope. Such a
command matches no handler - keep your commands in a `messages/` directory.

A command handler may only handle commands of its own scope. For the common layout - one `handlers/` directory at the
root of a Django app - the scope is that app, so nothing changes. If you organise a Django app into sub-packages, the
boundary follows those sub-packages instead.

Event handlers are deliberately not scope-checked: crossing scopes is what events are for.

[![PyPI release](https://img.shields.io/pypi/v/django-queuebie.svg)](https://pypi.org/project/django-queuebie/)
[![Downloads](https://static.pepy.tech/badge/django-queuebie)](https://pepy.tech/project/django-queuebie)
[![Coverage](https://img.shields.io/badge/Coverage-100.0%25-success)](https://github.com/ambient-innovation/django-queuebie/actions?workflow=CI)
[![Linting](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Coding Style](https://img.shields.io/badge/code%20style-Ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Documentation Status](https://readthedocs.org/projects/django-queuebie/badge/?version=latest)](https://django-queuebie.readthedocs.io/en/latest/?badge=latest)

A simple and synchronous message queue for commands and events for Django.

[PyPI](https://pypi.org/project/django-queuebie/) • [GitHub](https://github.com/ambient-innovation/django-queuebie) • [Full documentation](https://django-queuebie.readthedocs.io/en/latest/index.html)

Creator & Maintainer: [Beyonder Deutschland](https://beyonder.de/)

## Features

* Split up your business logic in commands and events
* Commands are imperatives telling your system what to do, events reflect that something has happened
* Register light-weight functions via a decorator to listen to your commands and events
* Message handlers receive the context of the message (command or event), providing an explicit API
* No magic, no side effects since the queue works synchronously

```python
import dataclasses

from queuebie.runner import handle_message
from queuebie.messages import Command, Event
from queuebie import message_registry

# Example command
@dataclasses.dataclass(kw_only=True)
class BuyProduct(Command):
    product_id: int
    customer_id: int
    price: float
    currency: str

# Example event
@dataclasses.dataclass(kw_only=True)
class ProductBought(Event):
    product_id: int
    customer_id: int

# Example handler
@message_registry.register_command(BuyProduct)
def handle_buy_product(context: BuyProduct) -> Event:
    # Here lives your business logic

    return ProductBought(
        product_id=context.product_id,
        customer_id=context.customer_id,
    )

# Start queue and process messages
handle_message(
    BuyProduct(
        product_id=product.id,
        customer_id=customer.id,
        price=12.99,
        currency="EUR",
    )
)
```

## Installation

- Install the package via pip:

  `pip install django_queuebie`

  or via uv:

  `uv add django_queuebie`

- Add module to `INSTALLED_APPS` within the main django `settings.py`:

```python
INSTALLED_APPS = (
    # ...
    "queuebie",
)
```

## Releasing a new version

Releases are fully automated. Push a version tag and the pipeline will build, sign with
[Sigstore](https://www.sigstore.dev/), publish to PyPI via
[Trusted Publishing](https://docs.pypi.org/trusted-publishers/), and create a GitHub Release —
no API tokens needed.

```bash
git tag v<version>          # e.g. git tag v1.2.3
git push origin v<version>
```

Tags **must** start with `v`. Tags without the prefix won't trigger the pipeline.

### First-time setup

Before the pipeline can run for the first time, an admin must:

1. **Create GitHub Environment `pypi`**
   - Go to *Settings → Environments → New environment*, name it exactly `pypi`
   - Under *Deployment branches and tags*, add a tag rule with pattern `v*`
   - Optionally add required reviewers for a manual approval gate

2. **Configure PyPI Trusted Publisher**
   - Go to *PyPI → Project settings → Publishing → Add a new publisher*
   - Fill in: Owner `ambient-innovation`, Repository `django-queuebie`,
     Workflow `release.yml`, Environment `pypi`

### Publish to ReadTheDocs.io

- Fetch the latest changes in GitHub mirror and push them
- Trigger new build at ReadTheDocs.io (follow instructions in admin panel at RTD) if the GitHub webhook is not yet set
  up.

### Maintenance

Please note that this package supports the [ambient-package-update](https://pypi.org/project/ambient-package-update/).
So you don't have to worry about the maintenance of this package. This updater is rendering all important
configuration and setup files. It works similar to well-known updaters like `pyupgrade` or `django-upgrade`.

To run an update, refer to the [documentation page](https://pypi.org/project/ambient-package-update/)
of the "ambient-package-update".

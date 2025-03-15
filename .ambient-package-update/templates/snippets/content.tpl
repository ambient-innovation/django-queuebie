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

# Getting started

## In a nutshell

* Create commands and events and define their context
* Create handlers which handle (no surprise here) commands and events
* Register each handler via the provided decorators
* Start the message queue by injecting a first command (usually in a view or API endpoint)

## Create commands and events

Here we see two messages. A command is always named in the imperative ("DoSomething"). An event used always past
tense ("SomethingHappened").

The context is a dataclass to create a defined API on what data is actually sent. Note, that you can send Django models
as well but take care when using foreign key relations inside your handlers. You then soften the clear context API by
implicitly fetching data.

```python
# my_app/messages/commands/product.py
from dataclasses import dataclass
from queuebie.messages import Command


# Example command
class BuyProduct(Command):
    @dataclass(kw_only=True)
    class Context:
        product_id: int
        customer_id: int
        price: float
        currency: str
```

```python
# my_app/messages/events/product.py
from dataclasses import dataclass
from queuebie.messages import Event


# Example event
class ProductBought(Event):
    @dataclass(kw_only=True)
    class Context:
        product_id: int
        customer_id: int
```

## Creating handlers

Here's an example of a simple handler function. By design, these are functions and not objects to keep it as simple,
understandable and testable as possible.

They have to live inside your Django app in `my_app/handlers/commands/[your_filename].py` or
respectively `handlers/events/[your_filename].py` for the auto-discovery to find it.

A handler becomes a handler when three conditions are met:

* The function is registered as such via one of the two decorators `register_command` and `register_event`
* The function lives within `my_app/handlers/commands/` or `my_app/handlers/events/`
* The function takes a message (command or event) and returns optionally the other type of message (event or command).

```python
# my_app/handlers/commands/product.py
from queuebie import message_registry
from queuebie.messages import Event


# Example handler
@message_registry.register_command(BuyProduct)
def handle_buy_product(context: BuyProduct.Context) -> Event:
    # Here lives your business logic

    return ProductBought(
        context=ProductBought.Context(
            product_id=context.product_id,
            customer_id=context.customer_id,
        )
    )
```

## Message queue

You can start the message queue from everywhere, but in most cases, the entry points to your application are the best
place. This means Django views or some kind of API views.

```python
# my_app/views.py

# Start queue and process messages
handle_message(
    BuyProduct(
        BuyProduct.Context(
            product_id=product.id,
            customer_id=customer.id,
            price=12.99,
            currency="EUR",
        )
    )
)
```

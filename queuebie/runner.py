from django.db import transaction

from queuebie import message_registry
from queuebie.exceptions import InvalidMessageTypeError
from queuebie.messages import Command, Event, Message


def handle_message(message_list: Message | list[Message]):
    if isinstance(message_list, list):
        queue = message_list
    else:
        queue = [message_list]

    # Run auto-registry
    from queuebie import message_registry

    message_registry.autodiscover()

    while queue:
        message = queue.pop(0)
        if isinstance(message, Event):
            handle_event(message, queue)
        elif isinstance(message, Command):
            handle_command(message, queue)
        else:
            raise InvalidMessageTypeError(class_name=message.__class__.__name__)


def handle_command(command: Command, queue: list[Message]):
    handler_list = message_registry.command_dict.get(command.__class__, [])  # TODO: ive replace "list()" here
    for handler in handler_list:
        try:
            # TODO: warum ist der rückgabewert hier wichtig?
            # TODO: logger bauen, den man über das django logging in den settings konfigurieren kann
            #  context, request-datum, user etc.
            print(f"Handling command '{command.__class__.__name__}' ({command.uuid}) with handler '{handler.__name__}'")
            if handler:
                # TODO: das sollte um das ganze handle_message
                with transaction.atomic():
                    new_messages = handler(context=command.Context) or []
                    new_messages = new_messages if isinstance(new_messages, list) else [new_messages]
                    uuid_list = [f"{m!s}" for m in new_messages]
                    print(f"New messages: {uuid_list!s}")
                    queue.extend(new_messages)
        except Exception as e:
            print(f"Exception handling command {command.__class__.__name__}: {e!s}")
            raise e from e


def handle_event(event: Event, queue: list[Message]):
    handler_list = message_registry.event_dict.get(event.__class__, [])  # TODO: ive replace "list()" here
    for handler in handler_list:
        try:
            print(f"Handling event '{event.__class__.__name__}' ({event.uuid}) with handler '{handler.__name__}'")
            if handler:
                with transaction.atomic():
                    new_messages = handler(context=event.Context) or []
                    new_messages = new_messages if isinstance(new_messages, list) else [new_messages]
                    uuid_list = [f"{m!s}" for m in new_messages]
                    print(f"New messages: {uuid_list!s}")
                    queue.extend(new_messages)
        except Exception as e:
            print(f"Exception handling event {event.__class__.__name__}: {e!s}")
            raise e from e

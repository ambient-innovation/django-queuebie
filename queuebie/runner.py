from django.db import transaction

from queuebie.exceptions import InvalidMessageTypeError
from queuebie.logging import get_logger
from queuebie.messages import Command, Event, Message


def handle_message(messages: Message | list[Message]) -> None:
    queue: list[Message] = messages if isinstance(messages, list) else [messages]

    for message in queue:
        if not isinstance(message, (Command, Event)):
            raise InvalidMessageTypeError(class_name=message.__class__.__name__)

    # Run auto-registry
    # todo: do we need this here?
    from queuebie import message_registry

    message_registry.autodiscover()

    handler_list = []
    while queue:
        message = queue.pop(0)
        if isinstance(message, Command):
            handler_list = message_registry.command_dict.get(message.__class__, [])
        elif isinstance(message, Event):
            handler_list = message_registry.event_dict.get(message.__class__, [])

        new_messages = _process_message(handler_list=handler_list, message=message)
        queue.extend(new_messages)


def _process_message(*, handler_list: list, message: [Command, Event]):
    """
    Handler to process messages of type "Command"
    """
    logger = get_logger()

    for handler in handler_list:
        try:
            # TODO: warum ist der rückgabewert hier wichtig? wäre das was für ein db log?
            # TODO: logger bauen, den man über das django logging in den settings konfigurieren kann
            #  context, request-datum, user etc.
            logger.debug(
                f"Handling command '{message.__class__.__name__}' ({message.uuid}) with handler '{handler.__name__}'"
            )
            if handler:
                # TODO: das sollte um das ganze handle_message - ist das so? test schreiben
                with transaction.atomic():
                    new_messages = handler(context=message.Context) or []
                    new_messages = new_messages if isinstance(new_messages, list) else [new_messages]
                    uuid_list = [f"{m!s}" for m in new_messages]
                    logger.debug(f"New messages: {uuid_list!s}")
        except Exception as e:
            logger.debug(f"Exception handling command {message.__class__.__name__}: {e!s}")
            raise e from e

        return new_messages

import importlib

from django.db import transaction

from queuebie import message_registry
from queuebie.exceptions import InvalidMessageTypeError
from queuebie.logger import get_logger
from queuebie.messages import Command, Event, Message


def handle_message(messages: Message | list[Message]) -> None:
    queue: list[Message] = messages if isinstance(messages, list) else [messages]

    for message in queue:
        if not isinstance(message, (Command, Event)):
            raise InvalidMessageTypeError(class_name=message.__class__.__name__)

    # Run auto-registry
    message_registry.autodiscover()

    handler_list = []
    while queue:
        message = queue.pop(0)
        # TODO: test this with messages with the same name
        if isinstance(message, Command):
            handler_list = message_registry.command_dict.get(message.module_path(), [])
        elif isinstance(message, Event):
            handler_list = message_registry.event_dict.get(message.module_path(), [])

        new_messages = _process_message(handler_list=handler_list, message=message)
        queue.extend(new_messages)


def _process_message(*, handler_list: list, message: [Command, Event]):
    """
    Handler to process messages of type "Command"
    """
    logger = get_logger()
    messages = []

    # TODO: handler: FunctionDefinition
    # TODO: test schreiben für atomic -> error mittendrin werfen
    with transaction.atomic():
        for handler in handler_list:
            try:
                # TODO: warum ist der rückgabewert hier wichtig? wäre das was für ein db log?
                # TODO: logger bauen, den man über das django logging in den settings konfigurieren kann
                #  context, request-datum, user etc.
                logger.debug(
                    f"Handling command '{message.module_path()}' ({message.uuid}) with handler '{handler['name']}'."
                )
                module = importlib.import_module(handler["module"])
                handler_function = getattr(module, handler["name"])
                handler_messages = handler_function(context=message.Context) or []
                handler_messages = handler_messages if isinstance(handler_messages, list) else [handler_messages]
                if len(handler_messages) > 0:
                    messages.append(*handler_messages)
                uuid_list = [f"{m!s}" for m in handler_messages]
                logger.debug(f"New messages: {uuid_list!s}")
            except Exception as e:
                logger.debug(f"Exception handling command {message.module_path()}: {e!s}")
                raise e from e

    return messages

import importlib
from contextlib import nullcontext

from django.db import transaction

from queuebie import message_registry
from queuebie.database_blocker import BlockDatabaseAccess
from queuebie.exceptions import InvalidMessageTypeError
from queuebie.logger import get_logger
from queuebie.messages import Command, Event, Message
from queuebie.settings import get_queuebie_strict_mode


def handle_message(messages: Message | list[Message]) -> list[Message]:
    """
    Process the given message(s) and every message their handlers return, until the queue is drained.

    Returns all handled messages in the order they were processed - the initial message(s) first, followed by
    everything raised along the way. The caller can inspect it to learn what its command led to, e.g. whether a
    handler returned an event or bailed out with `None`.
    """
    # Copy the input, so draining the queue doesn't empty the caller's list
    queue: list[Message] = list(messages) if isinstance(messages, list) else [messages]

    for message in queue:
        if not isinstance(message, (Command, Event)):
            raise InvalidMessageTypeError(class_name=message.__class__.__name__)

    # Run auto-registry
    message_registry.autodiscover()

    handled: list[Message] = []
    with transaction.atomic():
        while queue:
            message = queue.pop(0)
            handled.append(message)
            if isinstance(message, Command):
                handler_list = message_registry.command_dict.get(message.module_path(), [])
                block_db_access = False
            else:
                handler_list = message_registry.event_dict.get(message.module_path(), [])
                block_db_access = True if get_queuebie_strict_mode() else False

            new_messages = _process_message(handler_list=handler_list, message=message, block_db_access=block_db_access)
            queue.extend(new_messages)

    return handled


def _process_message(*, handler_list: list, message: [Command, Event], block_db_access: bool) -> list[Message]:
    """
    Handler to process messages of type "Command"
    """
    logger = get_logger()
    messages = []

    for handler in handler_list:
        try:
            logger.debug(
                f"Handling command '{message.module_path()}' ({message.uuid}) with handler '{handler['name']}'."
            )
            module = importlib.import_module(handler["module"])
            handler_function = getattr(module, handler["name"])
            with BlockDatabaseAccess() if block_db_access else nullcontext():
                handler_messages = handler_function(context=message) or []
            handler_messages = handler_messages if isinstance(handler_messages, list) else [handler_messages]
            if len(handler_messages) > 0:
                messages.extend(handler_messages)
            uuid_list = [f"{m!s}" for m in handler_messages]
            logger.debug(f"New messages: {uuid_list!s}")
        except Exception as e:
            logger.debug(f"Exception handling command {message.module_path()}: {e!s}")
            raise e from e

    return messages

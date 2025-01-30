from queuebie import message_registry
from queuebie.logger import get_logger
from queuebie.messages import Command
from testapp.messages.events.my_events import SomethingHappened


@message_registry.register_event(event=SomethingHappened)
def handle_my_event(*, context: SomethingHappened) -> list[Command] | Command:
    logger = get_logger()
    logger.info(f'Event "SomethingHappened" executed with other_var={context.other_var}.')
    return []

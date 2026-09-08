from queuebie import message_registry
from queuebie.logger import get_logger
from testapp.nested_domain.messages.events.nested_events import SomethingNestedHappened


@message_registry.register_event(event=SomethingNestedHappened)
def handle_nested_event(*, context: SomethingNestedHappened) -> None:
    logger = get_logger()
    logger.info(f'Event "SomethingNestedHappened" executed with other_var={context.other_var}.')

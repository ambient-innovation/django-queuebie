from queuebie import message_registry
from queuebie.logger import get_logger
from queuebie.messages import Event
from testapp.nested_domain.messages.commands.nested_commands import DoSomethingNested
from testapp.nested_domain.messages.events.nested_events import SomethingNestedHappened


@message_registry.register_command(command=DoSomethingNested)
def handle_nested_command(*, context: DoSomethingNested) -> Event:
    logger = get_logger()
    logger.info(f'Command "DoSomethingNested" executed with my_var={context.my_var}.')

    return SomethingNestedHappened(other_var=context.my_var + 1)

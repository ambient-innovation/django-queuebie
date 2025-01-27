from queuebie import message_registry
from queuebie.logger import get_logger
from queuebie.messages import Event
from testapp.messages.commands.my_commands import CriticalCommand, DoSomething
from testapp.messages.events.my_events import SomethingHappened


@message_registry.register_command(command=DoSomething)
def handle_my_command(*, context: DoSomething.Context) -> list[Event] | Event:
    logger = get_logger()
    logger.info(f'Command "DoSomething" executed with my_var={context.my_var}.')
    return SomethingHappened(context=SomethingHappened.Context(other_var=context.my_var + 1))


@message_registry.register_command(command=CriticalCommand)
def handle_critical_command(*, context: CriticalCommand.Context) -> None:
    if context.my_var == 0:
        raise RuntimeError("Handler is broken.")  # noqa: TRY003

from random import randint

from django.contrib.auth.models import User

from queuebie import message_registry
from queuebie.logger import get_logger
from queuebie.messages import Event
from testapp.messages.commands.my_commands import (
    CreateUser,
    CriticalCommand,
    DoSomething,
    PersistSomething,
    RaiseRuntimeError,
)
from testapp.messages.events.my_events import SomethingHappened, SomethingHappenedThatWantsToBePersisted


@message_registry.register_command(command=DoSomething)
def handle_my_command(*, context: DoSomething) -> list[Event] | Event:
    logger = get_logger()
    logger.info(f'Command "DoSomething" executed with my_var={context.my_var}.')
    return SomethingHappened(other_var=context.my_var + 1)


@message_registry.register_command(command=PersistSomething)
def handle_something_that_needs_persistence(*, context: PersistSomething) -> Event:
    User.objects.create(username="testuser" + str(randint(1, 100)))

    return SomethingHappenedThatWantsToBePersisted(any_var=1)


@message_registry.register_command(command=CriticalCommand)
def handle_critical_command(*, context: CriticalCommand) -> None:
    if context.my_var == 0:
        raise RuntimeError("Handler is broken.")  # noqa: TRY003


@message_registry.register_command(command=CreateUser)
def create_user(context: CreateUser):
    User.objects.create_user(username=context.username)


@message_registry.register_command(command=RaiseRuntimeError)
def raise_exception(context: RaiseRuntimeError):
    raise RuntimeError(context.error_msg)


class MyClass:
    """
    This is a test class since we observed the behaviour that in a similar setup, the "forced"
    import was breaking mocking.
    """

    def process(self):
        return 42

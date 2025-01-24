from queuebie import message_registry
from queuebie.messages import Command
from testapp.messages.events.my_events import SomethingHappened


@message_registry.register_event(event=SomethingHappened)
def handle_my_event(*, context: SomethingHappened.Context) -> list[Command] | Command:
    return []

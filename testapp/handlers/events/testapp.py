from queuebie import message_registry
from queuebie.messages import Command
from testapp.messages.events.my_events import MyEvent


@message_registry.register_event(event=MyEvent)
def handle_my_event(*, context: MyEvent.Context) -> list[Command] | Command:
    return []

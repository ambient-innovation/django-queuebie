from queuebie import message_registry
from queuebie.messages import Event
from testapp.messages.commands.my_commands import MyCommand
from testapp.messages.events.my_events import MyEvent


@message_registry.register_command(command=MyCommand)
def handle_my_command(*, context: MyCommand.Context) -> list[Event] | Event:
    return MyEvent(context=MyEvent.Context(other_var=context.my_var + 1))

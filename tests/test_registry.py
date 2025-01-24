from queuebie import MessageRegistry
from testapp.messages.commands.my_commands import MyCommand
from testapp.messages.events.my_events import MyEvent


def test_message_registry_init_regular():
    message_registry = MessageRegistry()

    assert message_registry.command_dict == {}
    assert message_registry.event_dict == {}


def test_message_registry_singleton_works():
    message_registry_1 = MessageRegistry()
    message_registry_2 = MessageRegistry()

    assert message_registry_1 is message_registry_2


def test_message_autodiscover_regular():
    message_registry = MessageRegistry()

    message_registry.autodiscover()

    # Assert one command registered
    assert len(message_registry.command_dict) == 1
    assert MyCommand in message_registry.command_dict.keys()

    # Assert one handler registered
    assert len(message_registry.command_dict[MyCommand]) == 1
    assert "<function handle_my_command at" in str(message_registry.command_dict[MyCommand][0])

    # Assert one event registered
    assert len(message_registry.event_dict) == 1
    assert MyEvent in message_registry.event_dict.keys()

    # Assert one handler registered
    assert len(message_registry.event_dict[MyEvent]) == 1
    assert "<function handle_my_event at" in str(message_registry.event_dict[MyEvent][0])

import pytest

from queuebie import MessageRegistry
from testapp.messages.commands.my_commands import DoSomething
from testapp.messages.events.my_events import SomethingHappened


def test_message_registry_init_regular():
    message_registry = MessageRegistry()

    assert message_registry.command_dict == {}
    assert message_registry.event_dict == {}


def test_message_registry_singleton_works():
    message_registry_1 = MessageRegistry()
    message_registry_2 = MessageRegistry()

    assert message_registry_1 is message_registry_2


def test_message_registry_register_command_regular():
    def dummy_function(*args):
        return None

    message_registry = MessageRegistry()
    decorator = message_registry.register_command(command=DoSomething)
    decorator(dummy_function)

    assert len(message_registry.event_dict) == 0
    assert len(message_registry.command_dict) == 1
    assert "dummy_function" in str(message_registry.command_dict[DoSomething][0])


def test_message_registry_register_command_second_function():
    def dummy_function(*args):
        return None

    def dummy_function_2(*args):
        return None

    message_registry = MessageRegistry()
    decorator = message_registry.register_command(command=DoSomething)
    decorator(dummy_function)
    decorator(dummy_function_2)

    assert len(message_registry.event_dict) == 0
    assert len(message_registry.command_dict) == 1
    assert "dummy_function" in str(message_registry.command_dict[DoSomething][0])
    assert "dummy_function_2" in str(message_registry.command_dict[DoSomething][1])


def test_message_registry_register_command_wrong_type():
    def dummy_function(*args):
        return None

    message_registry = MessageRegistry()
    decorator = message_registry.register_command(command=SomethingHappened)

    with pytest.raises(
        TypeError, match='Trying to register message function of wrong type: "MyEvent" on handler "dummy_function".'
    ):
        decorator(dummy_function)


def test_message_registry_register_event_regular():
    def dummy_function(*args):
        return None

    message_registry = MessageRegistry()
    decorator = message_registry.register_event(event=SomethingHappened)
    decorator(dummy_function)

    assert len(message_registry.command_dict) == 0
    assert len(message_registry.event_dict) == 1
    assert "dummy_function" in str(message_registry.event_dict[SomethingHappened][0])


def test_message_registry_register_event_second_function():
    def dummy_function(*args):
        return None

    def dummy_function_2(*args):
        return None

    message_registry = MessageRegistry()
    decorator = message_registry.register_event(event=SomethingHappened)
    decorator(dummy_function)
    decorator(dummy_function_2)

    assert len(message_registry.command_dict) == 0
    assert len(message_registry.event_dict) == 1
    assert "dummy_function" in str(message_registry.event_dict[SomethingHappened][0])
    assert "dummy_function_2" in str(message_registry.event_dict[SomethingHappened][1])


def test_message_registry_register_event_wrong_type():
    def dummy_function(*args):
        return None

    message_registry = MessageRegistry()
    decorator = message_registry.register_event(event=DoSomething)

    with pytest.raises(
        TypeError, match='Trying to register message function of wrong type: "MyCommand" on handler "dummy_function".'
    ):
        decorator(dummy_function)


def test_message_autodiscover_regular():
    message_registry = MessageRegistry()

    message_registry.autodiscover()

    # Assert one command registered
    assert len(message_registry.command_dict) == 1
    assert DoSomething in message_registry.command_dict.keys()

    # Assert one handler registered
    assert len(message_registry.command_dict[DoSomething]) == 1
    assert "<function handle_my_command at" in str(message_registry.command_dict[DoSomething][0])

    # Assert one event registered
    assert len(message_registry.event_dict) == 1
    assert SomethingHappened in message_registry.event_dict.keys()

    # Assert one handler registered
    assert len(message_registry.event_dict[SomethingHappened]) == 1
    assert "<function handle_my_event at" in str(message_registry.event_dict[SomethingHappened][0])

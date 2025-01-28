from pathlib import Path
from unittest import mock

import pytest
from django.core.cache import cache

from queuebie import MessageRegistry
from queuebie.exceptions import RegisterOutOfScopeCommandError
from testapp.messages.commands.my_commands import CriticalCommand, DoSomething
from testapp.messages.events.my_events import SomethingHappened
from tests.helpers.commands import DoTestThings


def dummy_function(*args):
    return None


def dummy_function_2(*args):
    return None


def test_message_registry_init_regular():
    message_registry = MessageRegistry()

    assert message_registry.command_dict == {}
    assert message_registry.event_dict == {}


def test_message_registry_singleton_works():
    message_registry_1 = MessageRegistry()
    message_registry_1.command_dict[0] = "my_module"
    message_registry_2 = MessageRegistry()

    assert message_registry_1 is message_registry_2
    assert message_registry_1.command_dict == message_registry_2.command_dict


def test_message_registry_register_command_regular():
    message_registry = MessageRegistry()
    decorator = message_registry.register_command(command=DoTestThings)
    decorator(dummy_function)

    assert len(message_registry.event_dict) == 0
    assert len(message_registry.command_dict) == 1
    assert "dummy_function" in str(message_registry.command_dict[DoTestThings.module_path()][0])


def test_message_registry_register_command_second_function():
    message_registry = MessageRegistry()
    decorator = message_registry.register_command(command=DoTestThings)
    decorator(dummy_function)
    decorator(dummy_function_2)

    assert len(message_registry.event_dict) == 0
    assert len(message_registry.command_dict) == 1
    assert "dummy_function" in str(message_registry.command_dict[DoTestThings.module_path()][0])
    assert "dummy_function_2" in str(message_registry.command_dict[DoTestThings.module_path()][1])


def test_message_registry_register_command_wrong_type():
    message_registry = MessageRegistry()
    decorator = message_registry.register_command(command=SomethingHappened)

    with pytest.raises(
        TypeError,
        match='Trying to register message function of wrong type: "SomethingHappened" on handler "dummy_function".',
    ):
        decorator(dummy_function)


def test_message_registry_register_command_wrong_scope():
    message_registry = MessageRegistry()
    decorator = message_registry.register_command(command=DoSomething)

    with pytest.raises(
        RegisterOutOfScopeCommandError,
        match='Trying to register a command from another scope/app: "DoSomething" on handler "dummy_function".',
    ):
        decorator(dummy_function)


def test_message_registry_register_event_regular():
    message_registry = MessageRegistry()
    decorator = message_registry.register_event(event=SomethingHappened)
    decorator(dummy_function)

    assert len(message_registry.command_dict) == 0
    assert len(message_registry.event_dict) == 1
    assert "dummy_function" in str(message_registry.event_dict[SomethingHappened.module_path()][0])


def test_message_registry_register_event_second_function():
    message_registry = MessageRegistry()
    decorator = message_registry.register_event(event=SomethingHappened)
    decorator(dummy_function)
    decorator(dummy_function_2)

    assert len(message_registry.command_dict) == 0
    assert len(message_registry.event_dict) == 1
    assert "dummy_function" in str(message_registry.event_dict[SomethingHappened.module_path()][0])
    assert "dummy_function_2" in str(message_registry.event_dict[SomethingHappened.module_path()][1])


def test_message_registry_register_event_wrong_type():
    message_registry = MessageRegistry()
    decorator = message_registry.register_event(event=DoSomething)

    with pytest.raises(
        TypeError, match='Trying to register message function of wrong type: "DoSomething" on handler "dummy_function".'
    ):
        decorator(dummy_function)


def test_message_autodiscover_regular():
    cache.clear()

    message_registry = MessageRegistry()
    message_registry.autodiscover()

    # Assert one command registered
    assert len(message_registry.command_dict) == 2  # noqa: PLR2004
    assert DoSomething.module_path() in message_registry.command_dict.keys()
    assert CriticalCommand.module_path() in message_registry.command_dict.keys()

    # Assert one handler registered
    assert len(message_registry.command_dict[DoSomething.module_path()]) == 1
    assert {
        "module": "testapp.handlers.commands.testapp",
        "name": "handle_my_command",
    } == message_registry.command_dict[DoSomething.module_path()][0]

    # Assert one event registered
    assert len(message_registry.event_dict) == 1
    assert SomethingHappened.module_path() in message_registry.event_dict.keys()

    # Assert one handler registered
    assert len(message_registry.event_dict[SomethingHappened.module_path()]) == 1
    assert {"module": "testapp.handlers.events.testapp", "name": "handle_my_event"} == message_registry.event_dict[
        SomethingHappened.module_path()
    ][0]


@mock.patch("queuebie.registry.QUEUEBIE_APP_BASE_PATH", return_value=Path("/some/path"))
def test_message_autodiscover_no_local_apps(*args):
    cache.clear()

    message_registry = MessageRegistry()
    message_registry.autodiscover()

    # Assert one command registered
    assert len(message_registry.command_dict) == 0
    assert len(message_registry.event_dict) == 0

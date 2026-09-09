import json
import logging
import sys
from pathlib import Path
from unittest import mock

import pytest
from django.core.cache import cache
from django.test import override_settings

from queuebie import MessageRegistry
from queuebie.exceptions import RegisterOutOfScopeCommandError
from queuebie.settings import get_queuebie_cache_key, get_queuebie_logger_name
from testapp.handlers.commands.testapp import MyClass
from testapp.messages.commands.messages import SendMessage
from testapp.messages.commands.my_commands import (
    CreateUser,
    CriticalCommand,
    DoSomething,
    PersistSomething,
    RaiseRuntimeError,
)
from testapp.messages.events.my_events import (
    SomethingHappened,
    SomethingHappenedThatWantsToBePersistedViaEvent,
)
from testapp.nested_domain.handlers.commands.nested_domain import handle_nested_command
from testapp.nested_domain.messages.commands.nested_commands import DoSomethingNested
from testapp.nested_domain.messages.events.nested_events import SomethingNestedHappened
from tests.helpers.commands import DoTestThings

DECOY_COMMAND_PATH = "testapp.tests.messages.commands.decoy_commands.NeverDiscovered"
DECOY_HANDLER_MODULE = "testapp.tests.handlers.commands.decoy"
ORPHAN_HANDLER_MODULE = "testapp.orphan_domain.handlers.commands.orphan"


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


@override_settings(QUEUEBIE_STRICT_MODE=False)
def test_message_registry_register_command_regular():
    message_registry = MessageRegistry()
    decorator = message_registry.register_command(command=DoTestThings)
    decorator(dummy_function)

    assert len(message_registry.event_dict) == 0
    assert len(message_registry.command_dict) == 1
    assert "dummy_function" in str(message_registry.command_dict[DoTestThings.module_path()][0])


@override_settings(QUEUEBIE_STRICT_MODE=False)
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
        match=r'Trying to register message function of wrong type: "SomethingHappened" on handler "dummy_function".',
    ):
        decorator(dummy_function)


def test_message_registry_register_command_wrong_scope():
    message_registry = MessageRegistry()
    decorator = message_registry.register_command(command=DoSomething)

    with pytest.raises(
        RegisterOutOfScopeCommandError,
        match=r'Command "DoSomething" \(scope "testapp"\) cannot be handled by '
        r'"dummy_function" \(scope "tests.test_registry"\).',
    ):
        decorator(dummy_function)


def test_message_registry_register_command_scope_outside_of_django_app():
    """
    Neither the command nor the handler lives inside an installed Django app, so their scopes are their
    full module paths - which differ.
    """
    message_registry = MessageRegistry()
    decorator = message_registry.register_command(command=DoTestThings)

    with pytest.raises(
        RegisterOutOfScopeCommandError,
        match=r'Command "DoTestThings" \(scope "tests.helpers.commands"\) cannot be handled by '
        r'"dummy_function" \(scope "tests.test_registry"\).',
    ):
        decorator(dummy_function)


def test_message_registry_register_command_nested_scope_matches():
    message_registry = MessageRegistry()
    decorator = message_registry.register_command(command=DoSomethingNested)
    decorator(handle_nested_command)

    assert len(message_registry.command_dict) == 1
    assert {
        "module": "testapp.nested_domain.handlers.commands.nested_domain",
        "name": "handle_nested_command",
    } == message_registry.command_dict[DoSomethingNested.module_path()][0]


def test_message_registry_register_command_nested_scope_differs():
    """
    Handler and command live in the same Django app but in different sub-packages.
    """
    message_registry = MessageRegistry()
    decorator = message_registry.register_command(command=DoSomething)

    with pytest.raises(
        RegisterOutOfScopeCommandError,
        match=r'Command "DoSomething" \(scope "testapp"\) cannot be handled by '
        r'"handle_nested_command" \(scope "testapp.nested_domain"\).',
    ):
        decorator(handle_nested_command)


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
        TypeError,
        match=r'Trying to register message function of wrong type: "DoSomething" on handler "dummy_function".',
    ):
        decorator(dummy_function)


def test_message_autodiscover_regular():
    cache.clear()

    message_registry = MessageRegistry()
    message_registry.autodiscover()

    # Assert every command of the test app registered, and nothing else
    assert set(message_registry.command_dict) == {
        CreateUser.module_path(),
        CriticalCommand.module_path(),
        DoSomething.module_path(),
        DoSomethingNested.module_path(),
        PersistSomething.module_path(),
        RaiseRuntimeError.module_path(),
        # Defined in a module called "messages.py", which must not be mistaken for the scope directory
        SendMessage.module_path(),
    }

    # Assert one handler registered
    assert len(message_registry.command_dict[DoSomething.module_path()]) == 1
    assert {
        "module": "testapp.handlers.commands.testapp",
        "name": "handle_my_command",
    } == message_registry.command_dict[DoSomething.module_path()][0]

    # Assert every event of the test app registered, and nothing else
    assert set(message_registry.event_dict) == {
        SomethingHappened.module_path(),
        SomethingHappenedThatWantsToBePersistedViaEvent.module_path(),
        SomethingNestedHappened.module_path(),
    }

    # Assert one handler registered
    assert len(message_registry.event_dict[SomethingHappened.module_path()]) == 1
    assert {"module": "testapp.handlers.events.testapp", "name": "handle_my_event"} == message_registry.event_dict[
        SomethingHappened.module_path()
    ][0]


def test_message_autodiscover_nested_handlers():
    cache.clear()

    message_registry = MessageRegistry()
    message_registry.autodiscover()

    assert DoSomethingNested.module_path() in message_registry.command_dict.keys()
    assert {
        "module": "testapp.nested_domain.handlers.commands.nested_domain",
        "name": "handle_nested_command",
    } == message_registry.command_dict[DoSomethingNested.module_path()][0]

    assert SomethingNestedHappened.module_path() in message_registry.event_dict.keys()
    assert {
        "module": "testapp.nested_domain.handlers.events.nested_domain",
        "name": "handle_nested_event",
    } == message_registry.event_dict[SomethingNestedHappened.module_path()][0]


def test_message_autodiscover_does_not_duplicate_packages():
    """
    Importing a handler package as "<package>.__init__" would create a second module object next to the package.
    """
    cache.clear()

    message_registry = MessageRegistry()
    message_registry.autodiscover()

    assert "testapp.handlers.commands" in sys.modules
    assert "testapp.handlers.commands.__init__" not in sys.modules


def test_message_autodiscover_excluded_directory_not_imported():
    cache.clear()

    message_registry = MessageRegistry()
    message_registry.autodiscover()

    assert DECOY_COMMAND_PATH not in message_registry.command_dict.keys()
    assert DECOY_HANDLER_MODULE not in sys.modules


def test_message_autodiscover_non_package_handler_directory_skipped(caplog):
    """
    A "handlers/commands" directory which is no Python package cannot be imported, so it is skipped - loudly,
    because handlers nobody registers are worse than a startup warning.
    """
    cache.clear()

    message_registry = MessageRegistry()
    with caplog.at_level(logging.WARNING, logger=get_queuebie_logger_name()):
        message_registry.autodiscover()

    assert ORPHAN_HANDLER_MODULE not in sys.modules
    assert str(Path("testapp") / "orphan_domain" / "handlers") in caplog.text, (
        "The skipped handler directory has to be named in the warning."
    )
    assert "is not a Python package" in caplog.text


@override_settings(QUEUEBIE_EXCLUDED_DIRECTORIES={"migrations", "__pycache__"})
def test_message_autodiscover_excluded_directories_configurable():
    cache.clear()

    message_registry = MessageRegistry()
    try:
        message_registry.autodiscover()

        assert DECOY_COMMAND_PATH in message_registry.command_dict.keys()
    finally:
        # Keep the deliberately discovered decoy out of the interpreter and the cache for the other tests
        sys.modules.pop(DECOY_HANDLER_MODULE, None)
        cache.clear()


@mock.patch("queuebie.registry.get_queuebie_app_base_path", return_value=Path("/some/path"))
def test_message_autodiscover_no_local_apps(*args):
    cache.clear()

    message_registry = MessageRegistry()
    message_registry.autodiscover()

    assert len(message_registry.command_dict) == 0
    assert len(message_registry.event_dict) == 0


@mock.patch("importlib.import_module")
@mock.patch("importlib.reload")
def test_message_autodiscover_caching_avoid_importing_again(mocked_reload_module, mocked_import_module):
    cache.set(
        get_queuebie_cache_key(), json.dumps({"commands": ["my_command_handler"], "events": ["my_event_handler"]})
    )

    message_registry = MessageRegistry()
    message_registry.autodiscover()

    assert mocked_reload_module.call_count == 0
    assert mocked_import_module.call_count == 0


def test_message_autodiscover_load_handlers_from_cache_regular(*args):
    cache.set(
        get_queuebie_cache_key(), json.dumps({"commands": ["my_command_handler"], "events": ["my_event_handler"]})
    )

    message_registry = MessageRegistry()
    commands, events = message_registry._load_handlers_from_cache()

    assert len(commands) == 1
    assert len(events) == 1


@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}})
def test_message_autodiscover_load_handlers_from_cache_dummy_cache(*args):
    message_registry = MessageRegistry()
    commands, events = message_registry._load_handlers_from_cache()

    assert len(commands) == 0
    assert len(events) == 0


@mock.patch.object(MyClass, "process")
def test_registry_forced_import_doesnt_break_mocking(mocked_process):
    """
    This is a test for ensuring that the "forced" import isn't breaking mocking features.
    """

    def my_func():
        return MyClass().process()

    my_func()
    mocked_process.assert_called_once()

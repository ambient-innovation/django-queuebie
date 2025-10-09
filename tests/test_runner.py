from logging import Logger
from unittest import mock

import pytest
from django.contrib.auth.models import User
from django.test import override_settings

from queuebie import MessageRegistry
from queuebie.database_blocker import DatabaseAccessDeniedError
from queuebie.exceptions import InvalidMessageTypeError
from queuebie.runner import handle_message
from testapp.messages.commands.my_commands import (
    CreateUser,
    CriticalCommand,
    DoSomething,
    PersistSomething,
    RaiseRuntimeError,
    SameNameCommand,
)
from testapp.messages.commands.other_commands import SameNameCommand as OtherSameNameCommand
from testapp.messages.events.my_events import (
    SomethingHappened,
    SomethingHappenedThatWantsToBePersistedViaEvent,
)


@pytest.mark.django_db
@mock.patch.object(Logger, "info")
def test_handle_message_queue_enqueues_next_messages(mocked_logger_info):
    handle_message(messages=DoSomething(my_var=1))

    # DoSomething triggers "SomethingHappened", so we assert that the whole queuing works
    assert mocked_logger_info.call_count == 2  # noqa: PLR2004
    assert mocked_logger_info.call_args_list == [
        mock.call('Command "DoSomething" executed with my_var=1.'),
        mock.call('Event "SomethingHappened" executed with other_var=2.'),
    ]


@pytest.mark.django_db
@mock.patch.object(Logger, "debug")
def test_handle_message_error_in_handler(mocked_logger_debug):
    with pytest.raises(RuntimeError, match=r"Handler is broken."):
        handle_message(messages=CriticalCommand(my_var=0))

    assert mocked_logger_debug.call_count > 1
    assert (
        mock.call(
            "Exception handling command testapp.messages.commands.my_commands.CriticalCommand: Handler is broken."
        )
        in mocked_logger_debug.call_args_list
    )


@pytest.mark.django_db
@mock.patch("queuebie.runner._process_message")
def test_handle_message_pass_single_message(mocked_handle_command):
    handle_message(messages=DoSomething(my_var=1))

    assert mocked_handle_command.call_count == 1


@pytest.mark.django_db
@mock.patch("queuebie.runner._process_message")
def test_handle_message_pass_message_list(mocked_handle_command):
    handle_message(
        messages=[
            DoSomething(my_var=1),
            SomethingHappened(other_var=2),
        ]
    )

    assert mocked_handle_command.call_count == 2  # noqa: PLR2004


def test_handle_message_pass_invalid_type():
    with pytest.raises(InvalidMessageTypeError, match='"MessageRegistry" is not an Event or Command'):
        handle_message(messages=MessageRegistry())


@pytest.mark.django_db
def test_handle_message_command_with_db_hit_is_ok():
    handle_message(messages=[PersistSomething(any_var="noodle")])


@pytest.mark.django_db
def test_handle_message_event_with_db_hit_fails():
    with pytest.raises(DatabaseAccessDeniedError, match="Database access is disabled in this context"):
        handle_message(messages=[SomethingHappenedThatWantsToBePersistedViaEvent(any_var=1)])


@pytest.mark.django_db
@override_settings(QUEUEBIE_STRICT_MODE=False)
def test_handle_message_event_with_db_hit_ok_when_not_on_strict_mode(*args):
    handle_message(messages=[SomethingHappenedThatWantsToBePersistedViaEvent(any_var=1)])


@pytest.mark.django_db
@mock.patch("queuebie.registry.get_queuebie_strict_mode", return_value=False)
@mock.patch.object(MessageRegistry, "autodiscover")
@mock.patch("queuebie.runner._process_message")
def test_handle_message_other_command_with_same_name(mocked_handle_command, *args):
    def dummy_func(*args, **kwargs):
        return None

    message_registry = MessageRegistry()
    decorator_1 = message_registry.register_command(command=SameNameCommand)
    decorator_1(dummy_func)

    decorator_2 = message_registry.register_command(command=OtherSameNameCommand)
    decorator_2(dummy_func)

    handle_message(messages=SameNameCommand(name="one"))

    assert mocked_handle_command.call_count == 1
    assert len(mocked_handle_command.call_args_list) == 1
    assert isinstance(mocked_handle_command.call_args_list[0][1]["message"], SameNameCommand)
    assert mocked_handle_command.call_args_list[0][1]["handler_list"] == [
        {"module": "tests.test_runner", "name": "dummy_func"}
    ]

    handle_message(messages=OtherSameNameCommand(name="two"))

    assert mocked_handle_command.call_count == 2  # noqa: PLR2004
    assert len(mocked_handle_command.call_args_list) == 2  # noqa: PLR2004
    assert isinstance(mocked_handle_command.call_args_list[1][1]["message"], OtherSameNameCommand)
    assert mocked_handle_command.call_args_list[1][1]["handler_list"] == [
        {"module": "tests.test_runner", "name": "dummy_func"}
    ]


@pytest.mark.django_db
@mock.patch("queuebie.registry.get_queuebie_strict_mode", return_value=False)
def test_handle_message_atomic_works(*args):
    with pytest.raises(RuntimeError, match=r"Something is broken."):
        handle_message([CreateUser(username="username"), RaiseRuntimeError(error_msg="Something is broken.")])

    assert User.objects.filter(username="username").exists() is False

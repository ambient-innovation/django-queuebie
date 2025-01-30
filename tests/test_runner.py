from logging import Logger
from unittest import mock

import pytest
from django.contrib.auth.models import User

from queuebie import MessageRegistry
from queuebie.exceptions import InvalidMessageTypeError
from queuebie.runner import _process_message, handle_message
from testapp.messages.commands.my_commands import CriticalCommand, DoSomething, SameNameCommand
from testapp.messages.events.my_events import SomethingHappened


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
    with pytest.raises(RuntimeError, match="Handler is broken."):
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
@mock.patch("queuebie.registry.get_queuebie_strict_mode", return_value=False)
@mock.patch.object(MessageRegistry, "autodiscover")
@mock.patch("queuebie.runner._process_message")
def test_handle_message_other_command_with_same_name(mocked_handle_command, *args):
    from testapp.messages.commands.other_commands import SameNameCommand as OtherSameNameCommand

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
def test_process_message_atomic_works(mocked_handle_command, *args):
    handler_list = [
        {"module": "testapp.handlers.commands.testapp", "name": "create_user"},
        {"module": "testapp.handlers.commands.testapp", "name": "raise_exception"},
    ]

    message = DoSomething(my_var=1)

    with pytest.raises(RuntimeError, match="Something is broken."):
        _process_message(handler_list=handler_list, message=message)

    assert User.objects.filter(username="username").exists() is False

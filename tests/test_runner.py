from logging import Logger
from unittest import mock

import pytest

from queuebie import MessageRegistry
from queuebie.exceptions import InvalidMessageTypeError
from queuebie.runner import handle_message
from testapp.messages.commands.my_commands import CriticalCommand, DoSomething


@pytest.mark.django_db
@mock.patch.object(Logger, "info")
def test_handle_message_queue_enqueues_next_messages(mocked_logger_info):
    handle_message(messages=DoSomething(context=DoSomething.Context(my_var=1)))

    # DoSomething triggers "SomethingHappened", so we assert that the whole queuing works
    assert mocked_logger_info.call_count == 2  # noqa: PLR2004
    assert mocked_logger_info.call_args_list == [
        mock.call('Command "DoSomething" executed with my_var=1.'),
        mock.call('Event "SomethingHappened" executed with other_var=2.'),
    ]


@pytest.mark.django_db
@mock.patch.object(Logger, "debug")
def test_handle_message_error_in_handler(logger_debug):
    with pytest.raises(RuntimeError, match="Handler is broken."):
        handle_message(messages=CriticalCommand(context=CriticalCommand.Context(my_var=0)))

    assert logger_debug.call_count > 1
    assert (
        mock.call(
            "Exception handling command testapp.messages.commands.my_commands.CriticalCommand: Handler is broken."
        )
        in logger_debug.call_args_list
    )


@pytest.mark.django_db
@mock.patch("queuebie.runner._process_message")
def test_handle_message_pass_single_message(handle_command):
    handle_message(messages=DoSomething(context=DoSomething.Context(my_var=1)))

    assert handle_command.call_count == 1


@pytest.mark.django_db
@mock.patch("queuebie.runner._process_message")
def test_handle_message_pass_message_list(handle_command):
    handle_message(
        messages=[
            DoSomething(context=DoSomething.Context(my_var=1)),
            DoSomething(context=DoSomething.Context(my_var=2)),
        ]
    )

    assert handle_command.call_count == 2  # noqa: PLR2004


def test_handle_message_pass_invalid_type():
    with pytest.raises(InvalidMessageTypeError, match='"MessageRegistry" is not an Event or Command'):
        handle_message(messages=MessageRegistry())

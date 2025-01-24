from logging import Logger
from unittest import mock

import pytest

from queuebie import MessageRegistry
from queuebie.exceptions import InvalidMessageTypeError
from queuebie.messages import Message
from queuebie.runner import handle_message
from testapp.messages.commands.my_commands import DoSomething


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
    def dummy_function(context):
        raise RuntimeError("Handler is broken.")

    message_registry = MessageRegistry()
    decorator = message_registry.register_command(command=DoSomething)
    decorator(dummy_function)

    with pytest.raises(RuntimeError, match="Handler is broken."):
        handle_message(messages=DoSomething(context=DoSomething.Context(my_var=1)))

    assert logger_debug.call_count == 2
    assert mock.call('Exception handling command DoSomething: Handler is broken.') in logger_debug.call_args_list


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

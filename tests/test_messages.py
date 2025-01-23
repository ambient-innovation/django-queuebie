import dataclasses

import pytest

from queuebie.exceptions import MessageContextWrongTypeError
from queuebie.messages import Message


def test_message_init_uuid_set():
    class MyMessage(Message):
        @dataclasses.dataclass
        class Context:
            my_var: int

    message = MyMessage(context=MyMessage.Context(my_var=1))

    assert message.uuid is not None


def test_message_str_regular():
    class MyMessage(Message):
        @dataclasses.dataclass
        class Context:
            my_var: int

    message = MyMessage(context=MyMessage.Context(my_var=1))

    assert str(message) == f"<class 'tests.test_messages.test_message_str_regular.<locals>.MyMessage'> ({message.uuid})"


def test_message_init_context_of_wrong_type():
    @dataclasses.dataclass
    class MyContext:
        my_var = 1

    with pytest.raises(MessageContextWrongTypeError, match=r"Context must be of type \"Message.Context\""):
        Message(context=MyContext)

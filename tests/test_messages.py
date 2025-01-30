import dataclasses

from queuebie.messages import Message


def test_message_init_uuid_set():
    @dataclasses.dataclass(kw_only=True)
    class MyMessage(Message):
        my_var: int

    message = MyMessage(my_var=1)

    assert message.uuid is not None


def test_message_str_regular():
    @dataclasses.dataclass(kw_only=True)
    class MyMessage(Message):
        my_var: int

    message = MyMessage(my_var=1)

    assert str(message) == f"<class 'tests.test_messages.test_message_str_regular.<locals>.MyMessage'> ({message.uuid})"

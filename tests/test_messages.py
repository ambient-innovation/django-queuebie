from unittest import mock

from testapp.messages.commands.my_commands import DoSomething


@mock.patch("uuid.uuid4", return_value="1234-abcd")
def test_message_init_uuid_set(*args):
    message = DoSomething(my_var=1)

    assert message.uuid == "1234-abcd"


def test_message_str_regular():
    message = DoSomething(my_var=1)

    assert str(message) == f"<class 'testapp.messages.commands.my_commands.DoSomething'> ({message.uuid})"

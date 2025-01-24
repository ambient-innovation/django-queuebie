from queuebie.runner import handle_message
from testapp.messages.commands.my_commands import DoSomething


def test_handle_message_pass_single_message():
    # TODO: finish me
    handle_message(message_list=DoSomething(context=DoSomething.Context(my_var=1)))
    assert 1 == 0  # noqa: PLR0133

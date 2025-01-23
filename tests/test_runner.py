import dataclasses

from queuebie.messages import Command, Event
from queuebie.runner import handle_message


class TestCommand(Command):
    @dataclasses.dataclass
    class Context:
        my_var: int


class CommandTested(Event):
    @dataclasses.dataclass
    class Context:
        my_var: int


def test_handle_message_pass_single_message():
    # TODO: finish me
    handle_message(message_list=TestCommand(context=TestCommand.Context(my_var=1)))
    assert 1 == 0  # noqa: PLR0133

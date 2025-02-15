from queuebie.utils import is_part_of_app
from testapp.handlers.commands.testapp import handle_my_command
from testapp.messages.commands.my_commands import DoSomething


def test_is_part_of_app_is_part():
    assert is_part_of_app(function=handle_my_command, class_type=DoSomething) is True


def test_is_part_of_app_is_not_part():
    assert is_part_of_app(function=test_is_part_of_app_is_part, class_type=DoSomething) is False


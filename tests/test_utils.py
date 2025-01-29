from queuebie.utils import is_part_of_app, unique_append_to_inner_list
from testapp.handlers.commands.testapp import handle_my_command
from testapp.messages.commands.my_commands import DoSomething


def test_is_part_of_app_is_part():
    assert is_part_of_app(function=handle_my_command, class_type=DoSomething) is True


def test_is_part_of_app_is_not_part():
    assert is_part_of_app(function=test_is_part_of_app_is_part, class_type=DoSomething) is False


def test_unique_append_to_inner_list_key_doesnt_exist():
    data = {}
    data = unique_append_to_inner_list(data=data, key="new_key", value=1)

    assert len(data) == 1
    assert "new_key" in data
    assert data["new_key"] == [1]


def test_unique_append_to_inner_list_key_exists():
    data = {"my_key": [1]}
    data = unique_append_to_inner_list(data=data, key="my_key", value=2)

    assert len(data) == 1
    assert "my_key" in data
    assert data["my_key"] == [1, 2]


def test_unique_append_to_inner_list_value_exists():
    data = {"my_key": [1]}
    data = unique_append_to_inner_list(data=data, key="my_key", value=1)

    assert len(data) == 1
    assert "my_key" in data
    assert data["my_key"] == [1]

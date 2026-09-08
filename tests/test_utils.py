from queuebie.utils import is_same_scope, message_scope, unique_append_to_inner_list
from testapp.handlers.commands.testapp import handle_my_command
from testapp.messages.commands.my_commands import DoSomething
from testapp.nested_domain.handlers.commands.nested_domain import handle_nested_command
from testapp.nested_domain.messages.commands.nested_commands import DoSomethingNested


def test_message_scope_flat_layout():
    assert message_scope(module_path="apps.shipping.handlers.commands.shipment") == "apps.shipping"
    assert message_scope(module_path="apps.shipping.messages.commands.shipment") == "apps.shipping"


def test_message_scope_nested_layout():
    assert message_scope(module_path="apps.logistics.shipping.handlers.commands.invoice") == "apps.logistics.shipping"


def test_message_scope_last_marker_wins():
    assert message_scope(module_path="apps.messages.shipping.handlers.commands.invoice") == "apps.messages.shipping"


def test_message_scope_module_named_like_marker():
    """
    The trailing segment is the module itself and must not be mistaken for the owning directory.
    """
    assert message_scope(module_path="apps.shipping.handlers.commands.messages") == "apps.shipping"
    assert message_scope(module_path="apps.shipping.messages.commands.handlers") == "apps.shipping"


def test_message_scope_without_marker():
    assert message_scope(module_path="tests.helpers.commands") == "tests.helpers.commands"


def test_is_same_scope_same_flat_scope():
    assert is_same_scope(function=handle_my_command, class_type=DoSomething) is True


def test_is_same_scope_same_nested_scope():
    assert is_same_scope(function=handle_nested_command, class_type=DoSomethingNested) is True


def test_is_same_scope_nested_handler_foreign_command():
    assert is_same_scope(function=handle_nested_command, class_type=DoSomething) is False


def test_is_same_scope_different_scope():
    assert is_same_scope(function=test_is_same_scope_same_flat_scope, class_type=DoSomething) is False


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

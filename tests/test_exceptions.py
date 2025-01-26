from queuebie.exceptions import (
    InvalidMessageTypeError,
    MessageContextWrongTypeError,
    RegisterOutOfScopeCommandError,
    RegisterWrongMessageTypeError,
)


def test_message_context_wrong_type_error():
    exception = MessageContextWrongTypeError(class_name="MyClass")

    assert str(exception) == 'Context must be of type "MyClass.Context"'


def test_register_wrong_message_type_error():
    exception = RegisterWrongMessageTypeError(message_name="Message", decoratee_name="Decoratee")

    assert str(exception) == 'Trying to register message function of wrong type: "Message" on handler "Decoratee".'


def test_register_command_out_of_scope_error():
    exception = RegisterOutOfScopeCommandError(message_name="Message", decoratee_name="Decoratee")

    assert str(exception) == 'Trying to register a command from another scope/app: "Message" on handler "Decoratee".'


def test_invalid_message_type_error():
    exception = InvalidMessageTypeError(class_name="MyClass")

    assert str(exception) == '"MyClass" is not an Event or Command'

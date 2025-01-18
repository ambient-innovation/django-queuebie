from queuebie.exceptions import InvalidMessageTypeError, MessageContextWrongTypeError, RegisterWrongMessageTypeError


def test_message_context_wrong_type_error():
    exception = MessageContextWrongTypeError(class_name="MyClass")

    assert str(exception) == 'Context must be of type "MyClass.Context"'


def test_register_wrong_message_type_error():
    exception = RegisterWrongMessageTypeError(message_name="Message", decoratee_name="Decoratee")

    assert str(exception) == 'Trying to register message function of wrong type: "Message" on handler "Decoratee".'


def test_invalid_message_type_error():
    exception = InvalidMessageTypeError(class_name="MyClass")

    assert str(exception) == '"MyClass" was not an Event or Command'

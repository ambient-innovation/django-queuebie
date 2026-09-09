from queuebie.exceptions import (
    InvalidExcludedDirectoriesError,
    InvalidMessageTypeError,
    RegisterOutOfScopeCommandError,
    RegisterWrongMessageTypeError,
)


def test_register_wrong_message_type_error():
    exception = RegisterWrongMessageTypeError(message_name="Message", decoratee_name="Decoratee")

    assert str(exception) == 'Trying to register message function of wrong type: "Message" on handler "Decoratee".'


def test_register_command_out_of_scope_error():
    exception = RegisterOutOfScopeCommandError(message_name="Message", decoratee_name="Decoratee")

    assert str(exception) == 'Trying to register a command from another scope/app: "Message" on handler "Decoratee".'


def test_invalid_message_type_error():
    exception = InvalidMessageTypeError(class_name="MyClass")

    assert str(exception) == '"MyClass" is not an Event or Command'


def test_invalid_excluded_directories_error():
    exception = InvalidExcludedDirectoriesError()

    assert str(exception) == "QUEUEBIE_EXCLUDED_DIRECTORIES has to be a collection of directory names, not a string."

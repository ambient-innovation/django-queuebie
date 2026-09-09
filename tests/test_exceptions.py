import pickle

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
    exception = RegisterOutOfScopeCommandError(
        message_name="Message",
        message_scope="apps.warband.faction",
        decoratee_name="Decoratee",
        decoratee_scope="apps.warband.skirmish",
    )

    assert str(exception) == (
        'Command "Message" (scope "apps.warband.faction") cannot be handled by '
        '"Decoratee" (scope "apps.warband.skirmish").'
    )


def test_invalid_message_type_error():
    exception = InvalidMessageTypeError(class_name="MyClass")

    assert str(exception) == '"MyClass" is not an Event or Command'


def test_invalid_excluded_directories_error():
    exception = InvalidExcludedDirectoriesError(setting_name="MY_SETTING")

    assert str(exception) == "MY_SETTING has to be a collection of directory names, not a string."


def test_exceptions_survive_pickling():
    """
    Unpickling replays "args" through __init__, so every exception has to accept its own rendered message.
    Frameworks which ship exceptions between processes rely on that.
    """
    exceptions = (
        RegisterWrongMessageTypeError(message_name="Message", decoratee_name="Decoratee"),
        RegisterOutOfScopeCommandError(
            message_name="Message",
            message_scope="apps.warband.faction",
            decoratee_name="Decoratee",
            decoratee_scope="apps.warband.skirmish",
        ),
        InvalidMessageTypeError(class_name="MyClass"),
        InvalidExcludedDirectoriesError(setting_name="MY_SETTING"),
    )

    for exception in exceptions:
        assert str(pickle.loads(pickle.dumps(exception))) == str(exception)


def test_invalid_excluded_directories_error_names_the_main_setting_by_default():
    assert str(InvalidExcludedDirectoriesError()) == (
        "QUEUEBIE_EXCLUDED_DIRECTORIES has to be a collection of directory names, not a string."
    )

from django.core.exceptions import ImproperlyConfigured


class RegisterWrongMessageTypeError(TypeError):
    def __init__(self, *, message_name: str, decoratee_name: str):
        super().__init__(
            f'Trying to register message function of wrong type: "{message_name}" on handler "{decoratee_name}".'
        )


class RegisterOutOfScopeCommandError(TypeError):
    def __init__(self, *, message_name: str, message_scope: str, decoratee_name: str, decoratee_scope: str):
        super().__init__(
            f'Command "{message_name}" (scope "{message_scope}") cannot be handled by '
            f'"{decoratee_name}" (scope "{decoratee_scope}").'
        )


class InvalidMessageTypeError(TypeError):
    def __init__(self, *, class_name: str):
        super().__init__(f'"{class_name}" is not an Event or Command')


class InvalidExcludedDirectoriesError(ImproperlyConfigured):
    # "args" is swallowed so that unpickling, which replays them through __init__, keeps working
    def __init__(self, *args):
        super().__init__("QUEUEBIE_EXCLUDED_DIRECTORIES has to be a collection of directory names, not a string.")

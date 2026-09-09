from django.core.exceptions import ImproperlyConfigured

# Unpickling replays an exception's rendered message through "args", so every exception below accepts it
# positionally and renders a new one only when constructed without. Frameworks which ship exceptions
# between processes - Celery, a multiprocessing test runner - rely on that.


class RegisterWrongMessageTypeError(TypeError):
    def __init__(self, *args, message_name: str = "", decoratee_name: str = ""):
        if not args:
            args = (
                f'Trying to register message function of wrong type: "{message_name}" on handler "{decoratee_name}".',
            )

        super().__init__(*args)


class RegisterOutOfScopeCommandError(TypeError):
    def __init__(
        self,
        *args,
        message_name: str = "",
        message_scope: str = "",
        decoratee_name: str = "",
        decoratee_scope: str = "",
    ):
        if not args:
            args = (
                f'Command "{message_name}" (scope "{message_scope}") cannot be handled by '
                f'"{decoratee_name}" (scope "{decoratee_scope}").',
            )

        super().__init__(*args)


class InvalidMessageTypeError(TypeError):
    def __init__(self, *args, class_name: str = ""):
        if not args:
            args = (f'"{class_name}" is not an Event or Command',)

        super().__init__(*args)


class InvalidExcludedDirectoriesError(ImproperlyConfigured):
    def __init__(self, *args, setting_name: str = "QUEUEBIE_EXCLUDED_DIRECTORIES"):
        if not args:
            args = (f"{setting_name} has to be a collection of directory names, not a string.",)

        super().__init__(*args)

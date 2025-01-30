class RegisterWrongMessageTypeError(TypeError):
    def __init__(self, *, message_name: str, decoratee_name: str):
        super().__init__(
            f'Trying to register message function of wrong type: "{message_name}" on handler "{decoratee_name}".'
        )


class RegisterOutOfScopeCommandError(TypeError):
    def __init__(self, *, message_name: str, decoratee_name: str):
        super().__init__(
            f'Trying to register a command from another scope/app: "{message_name}" on handler "{decoratee_name}".'
        )


class InvalidMessageTypeError(TypeError):
    def __init__(self, *, class_name: str):
        super().__init__(f'"{class_name}" is not an Event or Command')

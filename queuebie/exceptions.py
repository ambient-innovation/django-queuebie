class MessageContextWrongTypeError(RuntimeError):
    def __init__(self, *, class_name: str):
        super().__init__(f'Context must be of type "{class_name}.Context"')


class RegisterWrongMessageTypeError(TypeError):
    def __init__(self, *, message_name: str, decoratee_name: str):
        super().__init__(
            f'Trying to register message function of wrong type: "{message_name}" ' f'on handler "{decoratee_name}".'
        )


class InvalidMessageTypeError(TypeError):
    def __init__(self, *, class_name: str):
        super().__init__(f'"{class_name}" was not an Event or Command')

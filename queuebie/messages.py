import abc
import uuid


class Message(abc.ABC):
    """
    Base class for all commands and events.
    """

    uuid: str

    def __post_init__(self):
        super().__init__()
        # Hier kannst du zusätzliche Initialisierungslogik hinzufügen, falls nötig
        self.uuid = str(uuid.uuid4())

    def __str__(self) -> str:
        return f"{self.__class__} ({self.uuid})"

    @classmethod
    def module_path(cls) -> str:
        return f"{cls.__module__}.{cls.__qualname__}"


class Command(Message):
    """
    Commands are messages which prompt the system to do something.
    Are always written in present tense: "CreateInvoice".
    Every instance has to be decorated as "@dataclass(kw_only=True)".
    # todo: check that messages are dataclasses?
    """


class Event(Message):
    """
    Events are the results of a command.
    Are always written in past tense: "InvoiceCreated".
    Every instance has to be decorated as "@dataclass(kw_only=True)".
    """

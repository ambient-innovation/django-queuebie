import abc
import uuid
from dataclasses import dataclass

from queuebie.exceptions import MessageContextWrongTypeError


# TODO: commands dürfen nicht in anderen apps importiert werden, nur events
class Message(abc.ABC):
    """
    Base class for all commands and events.
    """

    uuid = str
    Context: dataclass

    @dataclass(kw_only=True)
    class Context:
        def __init__(self, **kwargs):
            raise NotImplementedError

    def __init__(self, context: "Message.Context") -> None:
        super().__init__()

        self.uuid = str(uuid.uuid4())

        if type(context) is not self.Context:
            raise MessageContextWrongTypeError(class_name=self.__class__.__name__)
        self.Context = context

    def __str__(self) -> str:
        return f"{self.__class__} ({self.uuid})"

    @classmethod
    def module_path(cls) -> str:
        return f"{cls.__module__}.{cls.__qualname__}"


class Command(Message):
    """
    Commands are messages which prompt the system to do something.
    Are always written in present tense: "CreateInvoice".
    """


class Event(Message):
    """
    Events are the results of a command.
    Are always written in past tense: "InvoiceCreated".
    """

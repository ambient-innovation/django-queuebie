import inspect
import uuid
from dataclasses import dataclass


class Message:
    uuid = str
    Context: dataclass

    @dataclass(kw_only=True)
    class Context:
        def __init__(self):
            raise NotImplementedError

    @classmethod
    def _from_dict_to_dataclass(cls, *, context_data: dict) -> "Message.Context":
        return cls.Context(
            **{
                key: (context_data[key] if val.default == val.empty else context_data.get(key, val.default))
                for key, val in inspect.signature(cls.Context).parameters.items()
            }
        )

    def __init__(self, context: "Message.Context"):  # noqa: PBR001
        self.uuid = str(uuid.uuid4())
        if type(context) is not self.Context:
            raise RuntimeError(f"Context must be of type {self.__class__.__name__}.Context")
        self.Context = context

    def __str__(self) -> str:
        return f"{self.__class__} ({self.uuid})"


class Command(Message):
    pass


class Event(Message):
    pass

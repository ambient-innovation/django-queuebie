import dataclasses

from queuebie.messages import Command


@dataclasses.dataclass(kw_only=True)
class SameNameCommand(Command):
    name: str

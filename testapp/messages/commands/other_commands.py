from dataclasses import dataclass

from queuebie.messages import Command


class SameNameCommand(Command):
    @dataclass(kw_only=True)
    class Context:
        name: str

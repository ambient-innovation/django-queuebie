from dataclasses import dataclass

from queuebie.messages import Command


@dataclass(kw_only=True)
class DoSomething(Command):
    my_var: int


@dataclass(kw_only=True)
class CriticalCommand(Command):
    my_var: int


@dataclass(kw_only=True)
class SameNameCommand(Command):
    name: str

from dataclasses import dataclass

from queuebie.messages import Command


class DoSomething(Command):
    @dataclass(kw_only=True)
    class Context:
        my_var: int


class CriticalCommand(Command):
    @dataclass(kw_only=True)
    class Context:
        my_var: int

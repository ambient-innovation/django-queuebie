from dataclasses import dataclass

from queuebie.messages import Command


class MyCommand(Command):
    @dataclass(kw_only=True)
    class Context:
        my_var: int

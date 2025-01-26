import dataclasses

from queuebie.messages import Command


class TestCommand(Command):
    @dataclasses.dataclass(kw_only=True)
    class Context:
        my_var: int

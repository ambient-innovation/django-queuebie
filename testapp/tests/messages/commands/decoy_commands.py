import dataclasses

from queuebie.messages import Command


@dataclasses.dataclass(kw_only=True)
class NeverDiscovered(Command):
    my_var: int

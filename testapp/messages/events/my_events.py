import dataclasses

from queuebie.messages import Event


@dataclasses.dataclass(kw_only=True)
class SomethingHappened(Event):
    other_var: int

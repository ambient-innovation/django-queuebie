import dataclasses

from queuebie.messages import Event


@dataclasses.dataclass(kw_only=True)
class SomethingNestedHappened(Event):
    other_var: int

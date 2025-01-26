import dataclasses

from queuebie.messages import Event


class SomethingWasTested(Event):
    @dataclasses.dataclass(kw_only=True)
    class Context:
        other_var: int

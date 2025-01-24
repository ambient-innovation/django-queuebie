from dataclasses import dataclass

from queuebie.messages import Event


class MyEvent(Event):
    @dataclass(kw_only=True)
    class Context:
        other_var: int

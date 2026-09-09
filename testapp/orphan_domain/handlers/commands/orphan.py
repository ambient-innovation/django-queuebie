# The missing "__init__.py" files are the point of this fixture, so INP001 does not apply here.
# ruff: noqa: INP001
"""
Sits in a "handlers/commands" directory whose parents are no Python packages. Auto-discovery must skip it
and say so, instead of dropping it silently.
"""

import dataclasses

from queuebie import message_registry
from queuebie.messages import Command


@dataclasses.dataclass(kw_only=True)
class NeverImported(Command):
    my_var: int


@message_registry.register_command(command=NeverImported)
def handle_never_imported(*, context: NeverImported) -> None:
    pass

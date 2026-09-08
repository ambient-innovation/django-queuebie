"""
Mirrors the handler layout inside an excluded directory. Autodiscovery must never import this module,
so the command below stays unregistered.
"""

from queuebie import message_registry
from testapp.tests.messages.commands.decoy_commands import NeverDiscovered


@message_registry.register_command(command=NeverDiscovered)
def handle_never_discovered(*, context: NeverDiscovered) -> None:
    pass

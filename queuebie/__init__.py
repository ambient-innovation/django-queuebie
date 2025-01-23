"""Simple event queue for commands and events (CQRS)"""

__version__ = "1.0.0"

from queuebie.registry import MessageRegistry

# Create global message registry
# TODO: is this thread-safe? does it matter? -> prove with unit-tests
message_registry = MessageRegistry()

# TODO: tasks for v1.0
#  -> docs with examples
#  -> tests
#  -> fix all code todos

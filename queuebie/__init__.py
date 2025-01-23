"""Simple event queue for commands and events (CQRS)"""

__version__ = "1.0.0"

from queuebie.registry import MessageRegistry

# Create global message registry
# TODO: is this thread-safe? doesn't matter, contains just the methods
#  -> if this is a proper singleton, we could call it when we need it instead of hiding it here
message_registry = MessageRegistry()

# TODO: tasks for v1.0
#  -> docs with examples
#  -> tests
#  -> fix all code todos

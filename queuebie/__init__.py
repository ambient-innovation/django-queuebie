"""Simple message queue for commands and events (CQRS)"""

__version__ = "0.1.0"

from queuebie.registry import MessageRegistry

# Create global message registry
# todo: hab ich hier n konflikt mit toolbox?
message_registry = MessageRegistry()

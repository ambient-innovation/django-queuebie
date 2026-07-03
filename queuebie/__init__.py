"""A simple and synchronous message queue for commands and events for Django"""

__version__ = "0.4.0"

from queuebie.registry import MessageRegistry

# Initialise global message registry
message_registry = MessageRegistry()

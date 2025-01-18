from queuebie.registry import MessageRegistry

# Create global message registry
# TODO: is this thread-safe?
message_registry = MessageRegistry()

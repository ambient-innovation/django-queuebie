"""Simple event queue for commands and events (CQRS)"""

__version__ = "0.1.0"

from queuebie.registry import MessageRegistry

# Create global message registry
message_registry = MessageRegistry()

# TODO: docs with examples
# TODO: add docs about how to set up logger
# TODO: docs about default timeout could be > 300?
# TODO: do we want a separate cache for queuebie?
# TODO: message handling optional in db oder im log ausgeben: context, request-datum, user etc.
# TODO: document settings
# TODO: document management command that this should go in the deployment process in the CI

import dataclasses

from queuebie.messages import Command


@dataclasses.dataclass(kw_only=True)
class SendMessage(Command):
    """
    Lives in a module called "messages" on purpose: the module name must not be mistaken for the
    directory determining the scope.
    """

    text: str

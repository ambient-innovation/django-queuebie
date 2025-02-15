import dataclasses

from ambient_toolbox.autodiscover import DecoratorBasedRegistry
from ambient_toolbox.autodiscover.utils import unique_append_to_inner_list

from queuebie.exceptions import RegisterOutOfScopeCommandError, RegisterWrongMessageTypeError
from queuebie.messages import Command, Event
from queuebie.settings import get_queuebie_strict_mode
from queuebie.utils import is_part_of_app


@dataclasses.dataclass(kw_only=True)
class FunctionDefinition:
    module: str
    name: str


class MessageRegistry(DecoratorBasedRegistry):
    """
    Singleton for registering messages classes in.
    """

    REGISTRY_GROUP_COMMANDS = "handlers.commands"
    REGISTRY_GROUP_EVENTS = "handlers.events"

    def register_command(self, *, command: type[Command]):
        def decorator(decoratee):
            # Ensure that registered message is of correct type
            if not (issubclass(command, Command)):
                raise RegisterWrongMessageTypeError(message_name=command.__name__, decoratee_name=decoratee.__name__)

            # Strict mode means, commands can only be registered for callables in the same Django app
            if get_queuebie_strict_mode() and not is_part_of_app(function=decoratee, class_type=command):
                raise RegisterOutOfScopeCommandError(message_name=command.__name__, decoratee_name=decoratee.__name__)

            # Add decoratee to dependency list
            function_definition = dataclasses.asdict(
                FunctionDefinition(module=decoratee.__module__, name=decoratee.__name__)
            )
            self.registry = unique_append_to_inner_list(
                data=self.registry[self.REGISTRY_GROUP_COMMANDS], key=command.module_path(), value=function_definition
            )

            super().register(registry_group="handlers.commands")(decoratee)

            # Return decoratee
            return decoratee

        return decorator

    def register_event(self, *, event: type[Event]):
        def decorator(decoratee):
            # Ensure that registered message is of correct type
            if not (issubclass(event, Event)):
                raise RegisterWrongMessageTypeError(message_name=event.__name__, decoratee_name=decoratee.__name__)

            super().register(registry_group="handlers.events")(decoratee)

            # Return decoratee
            return decoratee

        return decorator

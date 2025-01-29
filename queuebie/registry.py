import dataclasses
import importlib
import json
import os
import sys
from pathlib import Path

from django.apps import apps
from django.core.cache import cache

from queuebie.exceptions import RegisterOutOfScopeCommandError, RegisterWrongMessageTypeError
from queuebie.logger import get_logger
from queuebie.messages import Command, Event
from queuebie.settings import QUEUEBIE_APP_BASE_PATH, QUEUEBIE_CACHE_KEY
from queuebie.utils import is_part_of_app, unique_append_to_inner_list


@dataclasses.dataclass(kw_only=True)
class FunctionDefinition:
    module: str
    name: str


class MessageRegistry:
    """
    Singleton for registering messages classes in.
    """

    # TODO: make message registry generic and put in toolbox

    # TODO: build a system check that validates that in handlers registered message (command/event) match the context
    #  -> maybe we already have this in the autodiscover
    # TODO: Command-Handler have to create Event - as a check?
    _instance: "MessageRegistry" = None

    def __init__(self):
        self.command_dict: dict = {}
        self.event_dict: dict = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register_command(self, *, command: type[Command]):
        def decorator(decoratee):
            # Ensure that registered message is of correct type
            if not (issubclass(command, Command)):
                raise RegisterWrongMessageTypeError(message_name=command.__name__, decoratee_name=decoratee.__name__)

            if not is_part_of_app(function=decoratee, class_type=command):
                raise RegisterOutOfScopeCommandError(message_name=command.__name__, decoratee_name=decoratee.__name__)

            # Add decoratee to dependency list
            function_definition = dataclasses.asdict(
                FunctionDefinition(module=decoratee.__module__, name=decoratee.__name__)
            )
            self.command_dict = unique_append_to_inner_list(
                data=self.command_dict, key=command.module_path(), value=function_definition
            )

            logger = get_logger()
            logger.debug("Registered command '%s'", decoratee.__name__)

            # Return decoratee
            return decoratee

        return decorator

    def register_event(self, *, event: type[Event]):
        # TODO: create a generic registry function and "inherit" here from it
        def decorator(decoratee):
            # Ensure that registered message is of correct type
            if not (issubclass(event, Event)):
                raise RegisterWrongMessageTypeError(message_name=event.__name__, decoratee_name=decoratee.__name__)

            # Add decoratee to dependency list
            function_definition = dataclasses.asdict(
                FunctionDefinition(module=decoratee.__module__, name=decoratee.__name__)
            )
            self.event_dict = unique_append_to_inner_list(
                data=self.event_dict, key=event.module_path(), value=function_definition
            )

            logger = get_logger()
            logger.debug("Registered event '%s'", decoratee.__name__)

            # Return decoratee
            return decoratee

        return decorator

    def autodiscover(self) -> None:
        """
        Detects message registries which have been registered via the "register_*" decorator.
        """
        # Fetch registered handlers from cache if possible
        self.command_dict, self.event_dict = self._load_handlers_from_cache()

        # If the handlers were cached, we don't have to go through the file system
        if len(self.command_dict) > 0 and len(self.event_dict) > 0:
            return

        # Project directory
        project_path = QUEUEBIE_APP_BASE_PATH
        logger = get_logger()

        for app_config in apps.get_app_configs():
            app_path = Path(app_config.path).resolve()

            # If it's not a local app, we don't care
            if project_path not in app_path.parents:
                continue

            # TODO: registering only via one file might be a plus
            for message_type in ("commands", "events"):
                try:
                    for module in os.listdir(app_path / "handlers" / message_type):
                        if module[-3:] != ".py":
                            continue
                        module_name = module.replace(".py", "")
                        module_path = f"{app_config.label}.handlers.{message_type}.{module_name}"
                        sys_module = sys.modules.get(module_path)
                        if sys_module:
                            importlib.reload(sys_module)
                        else:
                            importlib.import_module(module_path)
                        logger.debug(f'"{module_path}" imported.')
                except FileNotFoundError:
                    pass

        # Log to shell which functions have been detected
        logger.debug("Message autodiscovery running for commands...")
        for command in self.command_dict:
            handler_list = ", ".join(str(x) for x in self.command_dict[command])
            logger.debug(f"* {command}: [{handler_list}]")
        logger.debug("Message autodiscovery running for events...")
        for event in self.event_dict:
            handler_list = ", ".join(str(x) for x in self.event_dict[event])
            logger.debug(f"* {event}: [{handler_list}]")

        logger.debug(f"{len(self.command_dict) + len(self.event_dict)} message handlers detected.\n")

        # Update cache
        cache.set(QUEUEBIE_CACHE_KEY, json.dumps({"commands": self.command_dict, "events": self.event_dict}))

    def _load_handlers_from_cache(self) -> tuple[dict, dict]:
        """
        Get registered handler definitions from Django cache
        """
        cached_data = cache.get(QUEUEBIE_CACHE_KEY)
        if cached_data is None:
            return {}, {}
        json_data = json.loads(cached_data)
        # TODO: casting to dataclass is missing
        cached_commands = json_data.get("commands", None)
        cached_events = json_data.get("events", None)

        return cached_commands, cached_events

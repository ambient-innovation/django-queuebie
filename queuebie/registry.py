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
from queuebie.settings import (
    get_queuebie_app_base_path,
    get_queuebie_cache_key,
    get_queuebie_excluded_directories,
    get_queuebie_strict_mode,
)
from queuebie.utils import is_same_scope, unique_append_to_inner_list


@dataclasses.dataclass(kw_only=True)
class FunctionDefinition:
    module: str
    name: str


class MessageRegistry:
    """
    Singleton for registering messages classes in.
    """

    # TODO: make message registry generic and put in toolbox
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

            if get_queuebie_strict_mode() and not is_same_scope(function=decoratee, class_type=command):
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
        project_path = get_queuebie_app_base_path()
        logger = get_logger()

        excluded_directories = get_queuebie_excluded_directories()

        for app_config in apps.get_app_configs():
            app_path = Path(app_config.path).resolve()

            # If it's not a local app, we don't care
            if project_path not in app_path.parents:
                continue

            for directory, directory_names, file_names in os.walk(app_path):
                # Excluded directories are pruned from the walk so their subtrees are never visited
                directory_names[:] = sorted(name for name in directory_names if name not in excluded_directories)

                current_path = Path(directory)
                if current_path.name not in ("commands", "events") or current_path.parent.name != "handlers":
                    continue

                package_path = f"{app_config.name}.{'.'.join(current_path.relative_to(app_path).parts)}"

                # Importing the package covers handlers registered in its "__init__.py"
                self._import_handler_module(module_path=package_path)
                for file_name in sorted(file_names):
                    if not file_name.endswith(".py") or file_name == "__init__.py":
                        continue
                    self._import_handler_module(module_path=f"{package_path}.{file_name[:-3]}")

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
        cache.set(get_queuebie_cache_key(), json.dumps({"commands": self.command_dict, "events": self.event_dict}))

    def _import_handler_module(self, *, module_path: str) -> None:
        """
        Imports a module containing message handlers, reloading it if it was imported before.
        """
        sys_module = sys.modules.get(module_path)
        if sys_module:
            importlib.reload(sys_module)
        else:
            importlib.import_module(module_path)

        get_logger().debug(f'"{module_path}" imported.')

    def _load_handlers_from_cache(self) -> tuple[dict, dict]:
        """
        Get registered handler definitions from Django cache
        """
        cached_data = cache.get(get_queuebie_cache_key())
        if cached_data is None:
            return {}, {}
        json_data = json.loads(cached_data)
        cached_commands = json_data.get("commands", None)
        cached_events = json_data.get("events", None)

        return cached_commands, cached_events

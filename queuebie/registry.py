import importlib
import os
import sys
from pathlib import Path

from django.apps import apps

from queuebie.exceptions import RegisterOutOfScopeCommandError, RegisterWrongMessageTypeError
from queuebie.logger import get_logger
from queuebie.messages import Command, Event
from queuebie.settings import QUEUEBIE_APP_BASE_PATH
from queuebie.utils import is_part_of_app


class MessageRegistry:
    """
    Singleton for registering messages classes in.
    """

    # TODO: maybe use a generic solution in the toolbox, where you have namespaces what you want to register so I
    #  can remove the notification registry, too

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
            if command not in self.command_dict:
                self.command_dict[command] = [decoratee]
            else:
                self.command_dict[command].append(decoratee)

            logger = get_logger()
            logger.debug("Registered command '%s'", decoratee.__name__)

            # Return decoratee
            return decoratee

        return decorator

    def register_event(self, *, event: type[Event]):
        def decorator(decoratee):
            # Ensure that registered message is of correct type
            if not (issubclass(event, Event)):
                raise RegisterWrongMessageTypeError(message_name=event.__name__, decoratee_name=decoratee.__name__)

            # Add decoratee to dependency list
            if event not in self.event_dict:
                self.event_dict[event] = [decoratee]
            else:
                self.event_dict[event].append(decoratee)

            logger = get_logger()
            logger.debug("Registered event '%s'", decoratee.__name__)

            # Return decoratee
            return decoratee

        return decorator

    def autodiscover(self) -> None:
        """
        Detects message registries which have been registered via the "register_*" decorator.
        """
        if len(self.command_dict) + len(self.event_dict) > 0:
            return

        # Import all messages in all installed apps to trigger notification class registration via decorator
        # TODO: can we not do this on every request?
        #  -> use the django cache -> do i have to handle if there is none?
        #  -> need to be able to kill the cache when the files change -> python file metadata?
        #  --> but then i have to go over all files, too
        #  dont overengineer. ich mach n MC, welches das putzt. wenn du n deployment unabhängigen cache verwendest,
        #  baust du das in die CI ein. fertig

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
                        if module[-3:] == ".py":
                            module_name = module.replace(".py", "")
                            try:
                                module_path = f"{app_config.label}.handlers.{message_type}.{module_name}"
                                sys_module = sys.modules.get(module_path)
                                if sys_module:
                                    importlib.reload(sys_module)
                                else:
                                    importlib.import_module(module_path)
                                logger.debug(f'"{module_path}" imported.')
                            except ModuleNotFoundError:
                                pass
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

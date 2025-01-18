import contextlib
import importlib
import os
from functools import wraps

from django.conf import settings

from apps.core.event_loop.messages import Command, Event


class MessageRegistry:
    """
    Singleton for registering messages classes in.
    """

    # TODO: build a system check that validates that in handlers registered message (command/event) match the context

    def __init__(self):
        self.command_dict: dict = {}
        self.event_dict: dict = {}

    def register_command(self, command: Command):  # noqa: PBR001, PBR002
        def decorator(decoratee):  # noqa: PBR001, PBR002
            # Ensure that registered message is of correct type
            if not (issubclass(command, Command)):
                raise TypeError(
                    f'Trying to register message function of wrong type: "{command.__name__}" '
                    f'on handler "{decoratee.__name__}".'
                )

            # Add decoratee to dependency list
            if command not in self.command_dict:
                self.command_dict[command] = [decoratee]
            else:
                self.command_dict[command].append(decoratee)

            # Return decoratee
            return decoratee

        return decorator

    def register_event(self, event: Event):  # noqa: PBR001, PBR002
        def decorator(decoratee):  # noqa: PBR001, PBR002
            # Ensure that registered message is of correct type
            if not (issubclass(event, Event)):
                raise TypeError(
                    f'Trying to register message function of wrong type: "{event.__name__}" '
                    f'on handler "{decoratee.__name__}".'
                )

            # Add decoratee to dependency list
            if event not in self.event_dict:
                self.event_dict[event] = [decoratee]
            else:
                self.event_dict[event].append(decoratee)

            # Return decoratee
            return decoratee

        return decorator

    def inject(self, func):  # noqa: PBR001, PBR002
        @wraps(func)
        def decorated(*args, **kwargs):  # noqa: PBR002
            new_args = (*args, self.event_dict)
            return func(*new_args, **kwargs)

        return decorated

    def autodiscover(self) -> None:
        """
        Detects message registries which have been registered via the "register_*" decorator.
        """
        if len(self.command_dict) + len(self.event_dict) > 0:
            return

        # Import all notification.pys in all installed apps to trigger notification class registration via decorator
        for app in settings.INSTALLED_APPS:
            if app[:5] != "apps.":
                continue
            custom_package = app.replace("apps.", "")
            for message_type in ["commands", "events"]:
                try:
                    for module in os.listdir(settings.APPS_DIR / custom_package / "handlers" / message_type):
                        if module[-3:] == ".py":
                            module_name = module.replace(".py", "")
                            with contextlib.suppress(ModuleNotFoundError):
                                importlib.import_module(f"{app}.handlers.{message_type}.{module_name}")
                except FileNotFoundError:
                    pass

        # Log to shell which functions have been detected
        print("Message autodiscovery running for commands...")
        for command in self.command_dict:
            handler_list = ", ".join(str(x) for x in self.command_dict[command])
            print(f"* {command}: [{handler_list}]")
        print("Message autodiscovery running for events...")
        for event in self.event_dict:
            handler_list = ", ".join(str(x) for x in self.event_dict[event])
            print(f"* {event}: [{handler_list}]")

        print(f"{len(self.command_dict) + len(self.event_dict)} message functions detected.\n")

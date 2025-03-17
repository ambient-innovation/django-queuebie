import random

from django.contrib.auth.models import User

from queuebie import message_registry
from queuebie.logger import get_logger
from queuebie.messages import Command
from testapp.messages.events.my_events import SomethingHappened, SomethingHappenedThatWantsToBePersistedViaEvent


@message_registry.register_event(event=SomethingHappened)
def handle_my_event(*, context: SomethingHappened) -> list[Command] | Command:
    logger = get_logger()
    logger.info(f'Event "SomethingHappened" executed with other_var={context.other_var}.')
    return []


@message_registry.register_event(event=SomethingHappenedThatWantsToBePersistedViaEvent)
def handle_event_and_try_to_persist_something(*, context: SomethingHappenedThatWantsToBePersistedViaEvent):
    User.objects.create(username="testuser" + str(random.randint(1, 100)))

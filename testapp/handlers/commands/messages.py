from queuebie import message_registry
from queuebie.logger import get_logger
from testapp.messages.commands.messages import SendMessage


@message_registry.register_command(command=SendMessage)
def handle_send_message(*, context: SendMessage) -> None:
    logger = get_logger()
    logger.info(f'Command "SendMessage" executed with text={context.text}.')

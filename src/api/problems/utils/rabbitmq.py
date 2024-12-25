import json
from datetime import datetime

from config.settings import RabbitMQ


async def push_message(message: dict) -> dict:
    message.update({"iot": datetime.now()})
    _to_str = json.dumps(message, default=str)
    await RabbitMQ().get_broker().publish(_to_str)
    return message

import json
from datetime import datetime

from config.settings import RabbitMQ


async def push_message(message: dict, queue_name: str = "Testing", rk: str = "push", exchange_name:str = "push") -> dict:
    message.update({"iot": datetime.now()})
    _to_str = json.dumps(message, default=str)
    await RabbitMQ().get_broker().publish(message=_to_str, queue=queue_name, routing_key=rk, exchange=exchange_name)
    return message

import asyncio
import json

from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue

from control import ControllerTest

broker = RabbitBroker(url="amqp://admin:admin@rabbitmq:5672")
app = FastStream(broker)
test_controller = ControllerTest()

@broker.subscriber(RabbitQueue("Testing", auto_delete=True), exchange="testing_system")
async def process_message(msg: str):
    decode = json.loads(msg)
    test_name = f"task_{decode.get('task_id')}"
    result = test_controller.check_solution(decode.get("solution"), test_name)
    print(result)

async def main():
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())

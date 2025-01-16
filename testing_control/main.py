import asyncio
import json
import logging
import time
from os import getenv

from dotenv import load_dotenv
from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue
from redis.asyncio import Redis

from control import ControllerTest

load_dotenv()

broker = RabbitBroker(url=getenv("RABBITMQ_URL"))
app = FastStream(broker)
test_controller = ControllerTest()

redis_client = Redis(host=getenv("REDIS_HOST"), port=getenv("REDIS_PORT"), db=getenv("TESTING_DB"))

logging.basicConfig(
    level=getenv("LOG_LEVEL", logging.INFO),
    format='[%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)d:%(funcName)s %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()

@broker.subscriber(RabbitQueue("Testing", auto_delete=True, routing_key="push"), exchange="push")
async def process_message(msg: str):
    logger.info("New message %s", msg)
    decode = json.loads(msg)
    test_name = f"task_{decode.get('task_id')}"

    current_time = time.perf_counter()
    try:
        test_result = test_controller.check_solution(decode.get("solution"), test_name)
    except ModuleNotFoundError:
        test_result = {"status": "Error", "message": "Test module not found"}
    end_time = time.perf_counter()
    test_result["time"] = round((end_time - current_time) * 1000)

    await redis_client.hset("tests_results", decode.get("user_id"), json.dumps(test_result))
    logger.info("push result %s", test_result)

async def main():
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())

from config.settings import Redis, settings


async def push_to_waiting(id: int, *args):
    await settings.REDIS.in_waiting.sadd("in_wait", id, *args)

async def check_in_waiting(id: int):
    return await settings.REDIS.in_waiting.sismember("in_wait", id)
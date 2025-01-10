from config.settings import Redis, settings


async def push_to_waiting(id: int, *args):
    return await settings.REDIS.testing_system.sadd(Redis.problems_namespace.IN_SUBMIT_WAITING_NAME, id, *args)

async def check_in_waiting(id: int):
    return await settings.REDIS.testing_system.sismember(Redis.problems_namespace.IN_SUBMIT_WAITING_NAME, id)

async def get_test_result(result_key: int|str):
    return await settings.REDIS.testing_system.hget(settings.REDIS.problems_namespace.TESTING_RESULTS_NAME, result_key)

async def remove_from_waiting(instance_name: str):
    return await settings.REDIS.testing_system.srem(settings.REDIS.problems_namespace.IN_SUBMIT_WAITING_NAME, instance_name)

async def remove_from_results(key: str|int):
    return await settings.REDIS.testing_system.hdel(settings.REDIS.problems_namespace.TESTING_RESULTS_NAME, key)

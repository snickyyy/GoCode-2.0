import pytest
import pytest_asyncio

print("blabla")

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup():
    print("wrerre")
    yield
    print('srefefre')


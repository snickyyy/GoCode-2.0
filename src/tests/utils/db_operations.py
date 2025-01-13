from faker import Faker
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.problems.models import Test, Task, Category
from api.users.auth.models import Session


async def get_last_session(session):
    stmt = select(Session.id).where(Session.created_at == select(func.max(Session.created_at))).limit(1)
    result = await session.execute(stmt)
    return result.scalar()

async def create_tests(count, session: AsyncSession):
    f = Faker("EN")
    test_for_task = [Test(path=f.file_path()) for i in range(count)]
    session.add_all(test_for_task)
    await session.commit()
    return test_for_task

async def create_tasks(count, session: AsyncSession):
    f = Faker("EN")
    stmt = select(Test.id).limit(1)
    execute = await session.execute(stmt)
    test_id = execute.scalar()
    tasks = [Task(title=f.name_male(), description=f.text(10), difficulty=1, category_id=1, test_id=test_id, constraints=f.text(10), image=f.image_url()) for i in range(count)]
    session.add_all(tasks)
    await session.commit()
    return tasks

async def create_category(count, session: AsyncSession):
    f = Faker("EN")
    categories = [Category(name=f.catch_phrase()) for i in range(count)]
    session.add_all(categories)
    await session.commit()
    return categories

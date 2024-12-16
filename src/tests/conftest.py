from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session

from main import app
from config.db import db_handler


engine = create_async_engine("sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False})


TestingSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

async def get_db():
    local_session = async_scoped_session(
        session_factory=TestingSessionLocal,
        scopefunc=current_task,
    )
    async with local_session() as session:
        yield session
        await local_session.remove()


app.dependency_overrides[db_handler.get_session] = get_db

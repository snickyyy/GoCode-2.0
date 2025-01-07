from asyncio import current_task
from contextlib import asynccontextmanager

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session

from main import app
from config.db import db_handler

from core.models import BaseModel

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

@asynccontextmanager
async def get_session_context():
    local_session = async_scoped_session(
        session_factory=TestingSessionLocal,
        scopefunc=current_task,
    )

    async with local_session() as session:
        yield session
        await local_session.remove()

app.dependency_overrides[db_handler.get_session] = get_db

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    from api.users.models import User
    from api.users.auth.models import Session
    from api.problems.models import Task, Test, Language, Category
    from api.forum.models import Post, Comment
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

@pytest_asyncio.fixture
async def session():
    async with get_session_context() as session:
        yield session

@pytest_asyncio.fixture(scope="session", autouse=True)
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

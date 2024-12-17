from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from config.settings import settings


class DbSettings:
    engine = create_async_engine(
        url=settings.DB.DB_URL,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False},
    )

    session_maker = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    async def get_session(self):
        local_session = async_scoped_session(
            session_factory=self.session_maker,
            scopefunc=current_task,
        )

        async with local_session() as session:
            yield session
            await local_session.remove()


db_handler = DbSettings()

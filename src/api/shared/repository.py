import logging
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, or_, and_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from logs.config import configure_logs

configure_logs()
logger = logging.getLogger(__name__)

class BaseRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_by_id(self, id: int|str):
        query = await self.db.get(self.model, id)
        if not query:
            logger.debug("ERROR: Instance does not exist ()", str(self.model))
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} does not exist")
        logger.debug("Get query %s from model %s", query.id, str(self.model))
        return query

    async def list(self, skip: int = 0, limit: int = 100):
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        logger.debug("Get all from model %s", str(self.model))
        return result.scalars().all()

    async def create(self, schema):
        logger.debug("%s",schema)
        obj = self.model(**schema.model_dump())
        try:
            self.db.add(obj)
            await self.db.commit()
        except IntegrityError:
            raise HTTPException(status_code=409, detail=f"{self.model.__name__} must be unique")
        logger.debug("Create %s object", str(self.model))
        return obj


    async def update(self, id, schema: BaseModel):
        obj = await self.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        for key, value in schema.model_dump().items():
            setattr(obj, key, value)
        await self.db.commit()
        logger.debug("Update %s object <%s>", obj.id,str(self.model))
        return obj

    async def delete(self, id: int):
        obj = await self.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        await self.db.delete(obj)
        await self.db.commit()
        logger.debug("Update %s object <%s>", obj.id, str(self.model))
        return obj

    async def strict_filter(self, schema, skip: int = 0, limit: int = 100):
        stmt = select(self.model).filter(
            and_(
                *[getattr(self.model, key) == value for key, value in schema.model_dump(exclude_unset=True).items()]
            )
        ).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def non_strict_filter(self, schema,  skip: int = 0, limit: int = 100):
        stmt = select(self.model).filter(
            or_(
                *[getattr(self.model, key) == value for key, value in schema.model_dump(exclude_unset=True).items()]
            )
        ).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def count_all(self, filters: list=None):
        stmt = select(func.count(self.model.id))
        if filters:
            stmt = stmt.filter(*filters)
        result = await self.db.scalar(stmt)
        return result

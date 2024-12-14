from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import db_handler


class BaseRepository:
    model = None

    def __init__(self, session: AsyncSession = Depends(db_handler.get_session)):
        self.db = session

    async def get_by_id(self, id):
        query = await self.db.get(self.model, id)
        if not query:
            raise HTTPException(status_code=404, detail="Object not found")
        return query

    async def list(self, skip: int = 0, limit: int = 100):
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, schema):
        obj = self.model(**schema.model_dump())
        self.db.add(obj)
        await self.db.commit()
        return obj


    async def update(self, id, schema: BaseModel):
        obj = await self.get_by_id(id)
        for key, value in schema.model_dump():
            setattr(obj, key, value)
        await self.db.commit()
        return obj

    async def delete(self, id: int):
        obj = await self.get_by_id(id)
        await self.db.delete(obj)
        await self.db.commit()

    async def strict_filter(self, schema, skip: int = 0, limit: int = 100):
        stmt = select(self.model).filter(
            and_(
                *[getattr(self.model, key) == value for key, value in schema.model_dump(exclude_unset=True).items()]
            )
        ).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def non_strict_filter(self, schema, skip: int = 0, limit: int = 100):
        stmt = select(self.model).filter(
            or_(
                *[getattr(self.model, key) == value for key, value in schema.model_dump(exclude_unset=True).items()]
            )
        ).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

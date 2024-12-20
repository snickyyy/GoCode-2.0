from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, or_, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import db_handler


class BaseRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_by_id(self, id: int|str):
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
        try:
            self.db.add(obj)
            await self.db.commit()
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Data must be unique")
        return obj


    async def update(self, id, schema: BaseModel):
        obj = await self.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        for key, value in schema.model_dump():
            setattr(obj, key, value)
        await self.db.commit()
        return obj

    async def delete(self, id: int):
        obj = await self.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        await self.db.delete(obj)
        await self.db.commit()
        return obj

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

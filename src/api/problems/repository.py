from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import case
from api.problems.models import Task, Solution, Category, Language, TASK_STATUS_CHOICES
from api.problems.schemas import SolutionFilter
from api.shared.repository import BaseRepository
from api.users.models import User


class ProblemsRepository(BaseRepository):
    model = Task

    async def get_all(self, user_id, limit: int=50, skip: int=0, **kwargs):
        difficulty_label = case(
            {
                self.model.difficulty == 1: "easy",
                self.model.difficulty == 2: "medium",
                self.model.difficulty == 3: "hard"
            },
            else_="unknown"
        ).label("difficulty_label")

        status_label = case(
            {
                Solution.status == 0: "in-development",
                Solution.status == 1: "decided",
            },
            else_=None
        ).label("status_label")

        stmt = select(
            self.model.id,
            self.model.title,
            Category.name,
            difficulty_label,
            status_label,
        ).join(Category)

        category = kwargs.get('category')
        diff = kwargs.get('difficulty')
        name = kwargs.get('name')
        if category:
            stmt = stmt.filter(Category.name == category)
        if diff:
            stmt = stmt.filter(difficulty_label == diff)
        if name:
            stmt = stmt.filter(self.model.title.ilike(f'%{name}%'))
        stmt = stmt.outerjoin(
            Solution,
            and_(Solution.task_id == Task.id, Solution.user_id == user_id)
        ).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.mappings().all()

class CategoryRepository(BaseRepository):
    model = Category

    async def get_all(self, sort=True):
        if sort:
            stmt = select(self.model.name).order_by(self.model.name)
        else:
            stmt = select(self.model.name)
        result = await self.db.execute(stmt)
        return result.scalars().all()

class LanguageRepository(BaseRepository):
    model = Language

class SolutionRepository(BaseRepository):
    model = Solution

    async def get_one_info(self, solution_id: int):
        stmt = (
            select(
                self.model.id,
                self.model.solution,
                User.username,
                self.model.time,
                self.model.memory,
                Language.name
            )
            .join(self.model.user)
            .join(self.model.language)
            .filter(and_(self.model.id == solution_id, self.model.status == TASK_STATUS_CHOICES.ACCEPTED))
        )
        result = await self.db.execute(stmt)
        res = result.first()
        if not res:
            return False
        return res

    async def get_solutions(self, schema: SolutionFilter, limit: int=10, skip: int=0):
        stmt = select(
            self.model.id,
            Language.name,
            self.model.status,
            self.model.time,
            self.model.memory,
        ).join(Language)
        stmt = stmt.filter(
            and_(
                *[getattr(self.model, key) == value for key, value in schema.model_dump(exclude_unset=True).items()]
            )
        ).limit(limit).offset(skip)
        result = await self.db.execute(stmt)
        return result.mappings().all()

from sqlalchemy import select, and_
from sqlalchemy.sql import case
from api.problems.models import Task, Solution, Category, Language
from api.shared.repository import BaseRepository


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
        if category:
            stmt = stmt.filter(Category.name == category)
        if diff:
            stmt = stmt.filter(difficulty_label == diff)
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

from typing import Any

from sqlalchemy import select, and_, func
from sqlalchemy.sql import case
from api.problems.models import Task, DIFFICULTLY_CHOICES, Solution, Category
from api.problems.schemas import TaskDetail
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

        stmt = stmt.outerjoin(
            Solution,
            and_(Solution.task_id == Task.id, Solution.user_id == user_id)
        ).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.mappings().all()

    async def get_task_details(self, id):
        task = await self.get_by_id(id)
        return TaskDetail.model_validate(task)

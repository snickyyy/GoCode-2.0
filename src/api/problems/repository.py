from sqlalchemy import select, and_, func
from sqlalchemy.sql import case
from api.problems.models import Task, DIFFICULTLY_CHOICES, Solution
from api.shared.repository import BaseRepository


class ProblemsRepository(BaseRepository):
    model = Task

    async def get_all(self, user_id):
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
            difficulty_label,
            status_label,
        ).outerjoin(
            Solution,
            and_(Solution.task_id == Task.id, Solution.user_id == user_id)
        )
        result = await self.db.execute(stmt)
        return result.mappings().all()

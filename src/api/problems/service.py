import asyncio
import json
import time

from asyncpg.exceptions import StringDataRightTruncationError
from fastapi import HTTPException
from sqlalchemy.exc import DBAPIError

from api.problems.models import DIFFICULTLY_CHOICES, TASK_STATUS_CHOICES
from api.problems.repository import ProblemsRepository, CategoryRepository, LanguageRepository, SolutionRepository
from api.problems.schemas import TaskDetail, SolutionFilter, UpdateSolution, CreateSolution
from api.problems.utils.rabbitmq import push_message
from api.problems.utils.redis_ import push_to_waiting, get_test_result, remove_from_waiting, remove_from_results
from config.settings import settings


class ProblemsService:
    def __init__(self,
                 problems_repository: ProblemsRepository,
                 category_repository: CategoryRepository=None,
                 language_repository: LanguageRepository=None,
                 solution_repository: SolutionRepository=None
                 ):

        self.problems_repository = problems_repository
        self.category_repository = category_repository
        self.language_repository = language_repository
        self.solution_repository = solution_repository

    async def get_list_tasks(self, user_id: int, skip: int, limit: int = settings.PAGE_SIZE, **sort):
        tasks = await self.problems_repository.get_all(user_id, skip=skip, limit=limit, **sort)
        return tasks

    async def get_task_details(self, id):
        task = await self.problems_repository.get_by_id(id)
        return TaskDetail.model_validate(task)

    async def get_total_tasks(self):
        tasks = await self.problems_repository.count_all()
        return tasks

    async def get_all_categories(self):
        return await self.category_repository.get_all()

    async def write_solution(self, user_id: int, task_id: int, language_id: int, test_result: dict):
        filter_schema = SolutionFilter(task_id=task_id, user_id=user_id, language_id=language_id)
        solution = await self.solution_repository.strict_filter(filter_schema)
        if solution:
            update_schema = UpdateSolution(
                solution=test_result.get("solution"),
                status=TASK_STATUS_CHOICES(int(test_result.get("status"))),
                time=test_result.get("time"),
                memory=16,
                test_passed=test_result.get("test_passed"),
            )
            try:
                obj = await self.solution_repository.update(solution[0].id, update_schema)
            except DBAPIError:
                raise HTTPException(status_code=409, detail="Maximum length of solution - 1445")
        else:
            create_schema = CreateSolution(
                solution=test_result.get("solution"),
                status=TASK_STATUS_CHOICES(int(test_result.get("status"))),
                time=test_result.get("time"),
                memory=16,
                test_passed=test_result.get("test_passed"),
                user_id=user_id,
                language_id=language_id,
                task_id=task_id
            )
            try:
                obj = await self.solution_repository.create(create_schema)
            except DBAPIError:
                raise HTTPException(status_code=409, detail="Maximum length of solution - 1445")
        return obj

    @staticmethod
    async def get_test_result(result_key: str|int, polling_rate_sec: int = 0.05, connection_attempts: int = 10000) -> dict:
        count_attempts = 0

        while count_attempts != connection_attempts:
            try_result = await get_test_result(result_key)
            if not try_result:
                await asyncio.sleep(polling_rate_sec)
                count_attempts += 1
                continue
            await remove_from_waiting(result_key)
            await remove_from_results(result_key)
            result = json.loads(try_result)
            if isinstance(result.get("status"), str) and  result.get("status").lower() == "error":
                raise HTTPException(status_code=409, detail="Task not found")
            return result
        raise HTTPException(status_code=409, detail="Failed to get test result, try again")

    @staticmethod
    async def push_to_test(user_id: int, solution: str, task_id: int):
        await push_message({"task_id": task_id, "solution": solution, "user_id": user_id})
        await push_to_waiting(user_id)

    @staticmethod
    def get_all_difficulty():
        return [DIFFICULTLY_CHOICES.EASY.label(), DIFFICULTLY_CHOICES.MEDIUM.label(), DIFFICULTLY_CHOICES.HARD.label()]

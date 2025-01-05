from api.problems.models import DIFFICULTLY_CHOICES
from api.problems.repository import ProblemsRepository, CategoryRepository, LanguageRepository, SolutionRepository
from api.problems.schemas import TaskDetail
from api.problems.utils.rabbitmq import push_message
from api.problems.utils.redis_ import push_to_waiting
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

    @staticmethod
    async def push_to_test(user_id: int, solution: str, task_id: int):
        await push_message({"task_id": task_id, "solution": solution, "user_id": user_id})
        await push_to_waiting(user_id)

    @staticmethod
    def get_all_difficulty():
        return [DIFFICULTLY_CHOICES.EASY.label(), DIFFICULTLY_CHOICES.MEDIUM.label(), DIFFICULTLY_CHOICES.HARD.label()]

import time

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.problems.models import TASK_STATUS_CHOICES
from api.problems.repository import ProblemsRepository, CategoryRepository, LanguageRepository, SolutionRepository
from api.problems.schemas import SubmitTask, LanguageFilter
from api.problems.service import ProblemsService
from api.problems.utils.redis_ import check_in_waiting
from api.shared.utils.pagination import Pagination
from config.db import db_handler
from config.settings import settings

router = APIRouter(prefix="/problems", tags=["problems"])

@router.get("/")
async def problems_list(request: Request,page: int|None = 1, category: str|None=None, difficulty: str|None = None, session: AsyncSession = Depends(db_handler.get_session)):
    service = ProblemsService(
        ProblemsRepository(session),
        CategoryRepository(session),
        LanguageRepository(session),
        SolutionRepository(session)
    )
    total_tasks = await service.get_total_tasks()
    pagination = Pagination(total_tasks, settings.PAGE_SIZE)
    offset, limit = pagination.get_offset_and_limit(page)
    tasks = await service.get_list_tasks(
        request.state.user.id,
        skip=offset,
        limit=limit,
        category=category,
        difficulty=difficulty
    )
    return {"detail":
                {
                    "tasks": {
                        "data": tasks,
                        "total": total_tasks
                    },
                    "filters": {
                        "categories": await service.get_all_categories(),
                        "difficulties": service.get_all_difficulty()
                    },
                    "pagination": {
                        "current_page": page,
                        "total_pages": pagination.total_pages,
                        "has_next": pagination.has_next(page),
                        "has_previous": pagination.has_previous(page),
                        "next_page": pagination.next_page(page),
                        "previous_page": pagination.previous_page(page)
                    }
                }
            }

@router.get("/{id}")
async def problem_detail(id: int, session: AsyncSession = Depends(db_handler.get_session)):
    data = await ProblemsService(ProblemsRepository(session)).get_task_details(id)
    return data

@router.post("/{task_id}/solution")
async def problem_solution(request: Request, task_id: int, solution: SubmitTask, session: AsyncSession = Depends(db_handler.get_session)):
    if not request.state.user.check_authenticated():
        raise HTTPException(status_code=401, detail="You need to be authenticated to solve problems")
    if await check_in_waiting(request.state.user.id):
        raise HTTPException(status_code=403, detail="You are already in queue")
    if len(solution.code) > 1445:
        raise HTTPException(status_code=409, detail="Maximum length of solution - 1445")
    service = ProblemsService(
        ProblemsRepository(session),
        solution_repository=SolutionRepository(session),
        language_repository=LanguageRepository(session)
    )
    language_filter_schema = LanguageFilter(name=solution.language)
    language_id = await service.language_repository.strict_filter(language_filter_schema, limit=1)
    if not language_id:
        raise HTTPException(status_code=404, detail="Language not found")

    start = time.perf_counter()
    await ProblemsService.push_to_test(user_id=request.state.user.id, solution=solution.code, task_id=task_id)
    test_result = await ProblemsService.get_test_result(result_key=request.state.user.id)
    testing_time = time.perf_counter() - start

    await service.write_solution(user_id=request.state.user.id, task_id=task_id, language_id=language_id[0].id, test_result=test_result)

    return {"detail": test_result, "testing_time": testing_time}

@router.get("/{task_id}/solutions")
async def problem_solutions(task_id: int, page: int|None=1, language:str|None=None, session: AsyncSession = Depends(db_handler.get_session)):
    service = ProblemsService(
        problems_repository=ProblemsRepository(session),
        solution_repository=SolutionRepository(session),
        language_repository=LanguageRepository(session)
    )
    total = await service.get_total_solutions(task_id)
    paginator = Pagination(total, 10)
    offset, limit = paginator.get_offset_and_limit(page)
    data = await service.get_solutions(task_id=task_id, language=language, limit=limit, skip=offset)
    return {"detail":
                {
                    "solutions": data,
                    "language": language,
                    "total_solutions": total,
                    "pagination": {
                        "current_page": page,
                        "total_pages": paginator.total_pages,
                        "has_next": paginator.has_next(page),
                        "has_previous": paginator.has_previous(page),
                        "next_page": paginator.next_page(page),
                        "previous_page": paginator.previous_page(page)
                    }
                }
            }

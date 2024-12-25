from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.problems.repository import ProblemsRepository
from api.problems.schemas import SubmitTask
from api.problems.utils.rabbitmq import push_message
from api.problems.utils.redis_ import check_in_waiting, push_to_waiting
from api.users.models import ROLES
from config.db import db_handler
from api.problems.generate_test_data import router as generate_date_api

router = APIRouter(prefix="/problems", tags=["problems"])
router.include_router(generate_date_api)

@router.get("/")
async def problems_list(request: Request, session: AsyncSession = Depends(db_handler.get_session)):
    data = await ProblemsRepository(session).get_all(request.state.user.id)
    return {"detail": data}

@router.get("/{id}")
async def problem_detail(id: int, session: AsyncSession = Depends(db_handler.get_session)):
    data = await ProblemsRepository(session).get_task_details(id)
    return data

@router.post("/{task_id}/solution")
async def problem_solution(request: Request, task_id: int, solution: SubmitTask, session: AsyncSession = Depends(db_handler.get_session)):
    if not request.state.user.check_authenticated():
        raise HTTPException(status_code=403, detail="You need to be authenticated to solve problems")
    if check_in_waiting(request.state.user.id):
        raise HTTPException(status_code=403, detail="You are already in queue")
    result = await push_message({"message": "hallo"})
    await push_to_waiting(request.state.user.id)
    return result

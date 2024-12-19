from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.problems.models import Language, Category, Test, Task, Solution
from api.problems.repository import ProblemsRepository
from api.users.auth.utils.sessions import get_user_by_session
from config.db import db_handler
from api.problems.generate_test_data import router as generate_date_api

router = APIRouter(prefix="/problems", tags=["problems"])
router.include_router(generate_date_api)

@router.get("/")
async def problems_list(user=Depends(get_user_by_session), session: AsyncSession = Depends(db_handler.get_session)):
    data = await ProblemsRepository(session).get_all(user.id)
    return {"detail": data}

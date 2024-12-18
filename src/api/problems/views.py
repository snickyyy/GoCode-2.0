from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.problems.models import Language, Category, Test, Task, Solution
from config.db import db_handler

router = APIRouter(prefix="/problems", tags=["problems"])


@router.get("/generate-languages")
async def generate_language(session: AsyncSession = Depends(db_handler.get_session)):
    res = await Language().generate_languages(session)
    return {"detail": res}

@router.get("/generate-categories")
async def generate_languages(session: AsyncSession = Depends(db_handler.get_session)):
    res = await Category().generate_categories(session)
    return {"detail": res}

@router.get("/generate-tests/{count}")
async def generate_tests(count: int, session: AsyncSession = Depends(db_handler.get_session)):
    res = await Test().generate_tests(count, session)
    return {"detail": res}

@router.get("/generate-tasks/{count}")
async def generate_tests(count: int, session: AsyncSession = Depends(db_handler.get_session)):
    res = await Task().generate_tasks(count, session)
    return {"detail": res}

@router.get("/generate-solutions/{count}")
async def generate_solutions(count: int, session: AsyncSession = Depends(db_handler.get_session)):
    res = await Solution().generate_solutions(count, session)
    return {"detail": res}

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from api.problems.models import Language, Category, Test, Task, Solution
from config.db import db_handler

router = APIRouter(prefix="/generate_data")

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

@router.get("/generate_all_relationships")
async def generate_all_relationships(tests_count: int|None=100, tasks_count: int|None=100, solutions_count:int|None=40,session: AsyncSession = Depends(db_handler.get_session)):
    await Solution().generate_all_relations(session=session,
                                            tests_count=tests_count,
                                            tasks_count=tasks_count,
                                            solutions_count=solutions_count)

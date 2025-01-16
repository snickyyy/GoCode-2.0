from time import perf_counter

from fastapi import APIRouter

from api.problems.models import Language, Category, Test, Task, Solution
from api.users.models import User

router = APIRouter(prefix="/generate_test_data", tags=["dev-tests"])


############## USERS #############

@router.get("/generate-users")
async def generate_users(count: int|None=10):
    res = await User.generate_users(count)
    return {"detail": res[-1]}

############## USERS #############

#---------------------------------

############## PROBLEMS #############

@router.get("/generate-languages")
async def generate_language():
    res = await Language.generate_languages()
    return {"detail": res[-1]}
#
@router.get("/generate-categories")
async def generate_languages():
    res = await Category.generate_categories()
    return {"detail": res[-1]}

@router.get("/generate-tests/{count}")
async def generate_tests(count: int):
    res = await Test.generate_tests(count)
    return {"detail": res[-1]}

@router.get("/generate-tasks/{count}")
async def generate_tests(count: int):
    res = await Task.generate_tasks(count)
    return {"detail": res[-1]}

@router.get("/generate-solutions/{count}")
async def generate_solutions(count: int, task_id: int|None=None):
    res = await Solution().generate_solutions(count, task_id)
    return {"detail": res[-1]}

############## PROBLEMS #############

#---------------------------------

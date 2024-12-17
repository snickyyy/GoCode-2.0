from fastapi import APIRouter
from api.users.auth.views import router as auth_api

router = APIRouter(prefix="/accounts", tags=["account"])

router.include_router(auth_api)

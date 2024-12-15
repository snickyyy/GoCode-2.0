from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException

from api.users.auth.schemas import RegisterUser
from api.users.auth.services.email import send_email
from api.users.auth.utils.sessions import create_session, SessionsTypes, check_email_session
from api.users.models import User, ROLES
from api.users.repository import UserRepository
from six import text_type

from api.users.schemas import UserInfo
from config.settings import settings

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(schema: RegisterUser):
    user = await UserRepository().create(schema=schema)
    token = await create_session(user_obj=user, sess_type=SessionsTypes.AUTHENTICATION, exp=datetime.now() + timedelta(seconds=settings.AUTH.EMEIL_CONFIRM_TIME_SEC))
    await send_email(email=schema.email, username=schema.username, token=token)
    return {"success": "an email has been sent"}

@router.get("/activate-account/{token}", response_model=UserInfo)
async def activate_account(token):
    user: User = await check_email_session(token)
    if not user or user.role.label != ROLES.ANONYMOUS.label:
        raise HTTPException(status_code=400, detail="Invalid token")
    user.role = ROLES.USER
    return UserInfo(username=user.username, email=user.email, description=user.description)

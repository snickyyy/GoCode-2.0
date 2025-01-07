from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.auth.repository import SessionRepository
from api.users.auth.schemas import RegisterUser, LoginUser
from api.users.auth.services.email import send_email

from api.users.auth.service import AuthService
from api.users.auth.utils.sessions import SessionsTypes, check_email_session
from api.users.models import User, ROLES
from api.users.repository import UserRepository

from config.db import db_handler
from config.settings import settings

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(request: Request, schema: RegisterUser, session: AsyncSession = Depends(db_handler.get_session)):
    if request.state.user.check_authenticated():
        raise HTTPException(status_code=403, detail="You are already authenticated")
    service = AuthService(UserRepository(session), SessionRepository(session))

    user = await service.create_user(schema)
    token = await service.create_session(
        user_obj=user,
        sess_type=SessionsTypes.AUTHENTICATION,
        exp=datetime.now() + timedelta(seconds=settings.AUTH.EMEIL_CONFIRM_TIME_SEC)
    )
    await send_email(email=schema.email, username=schema.username, token=token)
    return {"detail": "an email has been sent"}

@router.get("/activate-account/{token}")
async def activate_account(request: Request, token, session: AsyncSession = Depends(db_handler.get_session)):
    service = AuthService(UserRepository(session), SessionRepository(session))
    if request.state.user.is_authenticated:
        raise HTTPException(status_code=403, detail="You are already authenticated")
    user: User = await service.check_email_session(token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    service.authorize()
    return {"detail": "your account has been activated, now you need to log in"}

@router.post("/login")
async def login(request: Request, response: Response, schema: LoginUser, session: AsyncSession = Depends(db_handler.get_session)):
    if request.state.user.is_authenticated:
        raise HTTPException(status_code=403, detail="You are already authenticated")
    service = AuthService(UserRepository(session), SessionRepository(session))
    user = await service.authorize(schema.username_or_email, schema.password)

    cookies = await service.create_session(
        user_obj=user,
        sess_type=SessionsTypes.AUTHORIZATION,
        exp=datetime.now() + timedelta(seconds=settings.AUTH.SESSION_DURATION_SEC)
    )
    response.set_cookie(
        key=settings.AUTH.SESSION_AUTH_KEY,
        value=cookies,
        httponly=True,
        max_age=settings.AUTH.SESSION_EXPIRE_SEC,
        secure=True,
        samesite="lax"
    )

    return {"detail": "Logged in successfully"}

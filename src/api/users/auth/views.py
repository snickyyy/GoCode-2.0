from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.auth.schemas import RegisterUser, LoginUser
from api.users.auth.services.email import send_email
from api.users.auth.utils.sessions import create_session, SessionsTypes, check_email_session
from api.users.models import User, ROLES
from api.users.repository import UserRepository

from api.users.schemas import UserInfo
from config.db import db_handler
from config.settings import settings

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(schema: RegisterUser, session: AsyncSession = Depends(db_handler.get_session)):
    user = await UserRepository(session).create(schema=schema)
    token = await create_session(user_obj=user,
                                 sess_type=SessionsTypes.AUTHENTICATION,
                                 exp=datetime.now() + timedelta(seconds=settings.AUTH.EMEIL_CONFIRM_TIME_SEC),
                                 session=session)
    await send_email(email=schema.email, username=schema.username, token=token)
    return {"detail": "an email has been sent"}

@router.get("/activate-account/{token}")
async def activate_account(token, session: AsyncSession = Depends(db_handler.get_session)):
    user: User = await check_email_session(token, session=session)
    if not user or user.role.label != ROLES.ANONYMOUS.label:
        raise HTTPException(status_code=400, detail="Invalid token")
    user.role = ROLES.USER
    session.add(user)
    await session.commit()
    return {"detail": "your account has been activated, now you need to log in"}

@router.post("/login")
async def login(response: Response, schema: LoginUser, session: AsyncSession = Depends(db_handler.get_session)):
    user = await UserRepository(session).get_by_username_or_email(schema.username_or_email)
    if not user or not user.check_password(schema.password) or user.role == ROLES.ANONYMOUS.value:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    cookies = await create_session(user_obj=user,
                                 sess_type=SessionsTypes.AUTHORIZATION,
                                 exp=datetime.now() + timedelta(seconds=settings.AUTH.SESSION_DURATION_SEC),
                                 session=session)
    response.set_cookie(
        key=settings.AUTH.SESSION_AUTH_KEY,
        value=cookies,
        httponly=True,
        max_age=settings.AUTH.SESSION_EXPIRE_SEC,
        secure=True,
        samesite="lax"
    )

    return {"detail": "Logged in successfully"}

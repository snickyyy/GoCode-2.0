from fastapi import Request, Depends
from datetime import datetime
from enum import Enum

from cryptography.fernet import InvalidToken
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.auth.models import Session
from api.users.auth.repository import SessionRepository
from api.users.auth.utils.utils import decrypt_data
from api.users.models import User, ROLES
from api.users.repository import UserRepository
from config.db import db_handler
from config.settings import settings


class SessionsTypes(Enum):
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"


async def create_session(user_obj: User, sess_type: SessionsTypes, exp: datetime, session: AsyncSession):
    payload = {"session_type": sess_type.value,
                "user_id": user_obj.id,
                "username": user_obj.username,
                "email": user_obj.email,
                "role": user_obj.role,
                "iat": datetime.now().isoformat()
               }
    sess_id = await SessionRepository(session).create(payload=payload, exp=exp)
    return sess_id


async def check_email_session(sessions_id, session: AsyncSession)-> User | bool:
    session_obj: Session = await SessionRepository(session).get_by_id(id=sessions_id)
    if session_obj.expires_at <= datetime.now():
        return False

    _decrypt_session: dict = decrypt_data(session_obj.data)
    if not _decrypt_session.get("session_type") or _decrypt_session.get("session_type") != SessionsTypes.AUTHENTICATION.value:
        return False

    user = await UserRepository(session).get_by_id(_decrypt_session.get("user_id"))
    return user

async def check_user_session(sessions_id, session: AsyncSession):
    get_session = await SessionRepository(session).get_by_id(sessions_id)
    if get_session.expires_at <= datetime.now():
        return False

    try:
        decrypt_sess = decrypt_data(get_session.data)
    except InvalidToken:
        return False

    if decrypt_sess.get("role") == ROLES.ANONYMOUS.label():
        return False
    user_by_session = await UserRepository(session).get_by_id(decrypt_sess.get("user_id"))
    return user_by_session

async def get_user_by_session(request: Request, session: AsyncSession = Depends(db_handler.get_session)):
    cookie = request.cookies.get(settings.AUTH.SESSION_AUTH_KEY)
    if not cookie:
        return None
    user_by_session = await check_user_session(cookie, session)
    return user_by_session

async def check_anonymous_session(sessions_id, session: AsyncSession):
    get_session = await SessionRepository(session).get_by_id(sessions_id)
    if get_session.expires_at <= datetime.now():
        return False

    try:
        decrypt_sess = decrypt_data(session.data)
    except InvalidToken:
        return False

    if decrypt_sess.get("role") != ROLES.ANONYMOUS.label():
        return False
    user_by_session = await UserRepository(session).get_by_id(decrypt_sess.get("user_id"))
    return user_by_session

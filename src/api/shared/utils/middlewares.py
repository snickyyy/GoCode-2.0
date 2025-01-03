from fastapi import Request, HTTPException

from api.users.auth.repository import SessionRepository
from api.users.models import ROLES, User
from api.users.repository import UserRepository
from config.db import db_handler


async def set_anonymous_user(request: Request):
    request.state.user = User(id=0, role=ROLES.ANONYMOUS, username="unknown")
    request.state.user.is_authenticated = False

async def get_session_from_cookie(cookie_key: str):
    async with db_handler.get_session_context() as sess:
        try:
            session = await SessionRepository(sess).get_by_id(cookie_key)
            return session
        except HTTPException:
            return None


async def get_user(user_id: int):
    async with db_handler.get_session_context() as sess:
        try:
            user = await UserRepository(sess).get_by_id(user_id)
            return user
        except HTTPException:
            return None
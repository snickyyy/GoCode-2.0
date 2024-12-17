from fastapi import Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.auth.utils.sessions import check_user_session
from config.db import db_handler
from config.settings import settings


async def check_auth_user(request: Request, session: AsyncSession = Depends(db_handler.get_session)):
    cookie = request.cookies.get(settings.AUTH.SESSION_AUTH_KEY)
    if not cookie:
        raise HTTPException(status_code=401, detail="Unauthorized")
    check_cookie = await check_user_session(cookie, session)
    if not check_cookie:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return check_cookie

async def check_auth_anonymous(request: Request, session: AsyncSession = Depends(db_handler.get_session)):
    cookie = request.cookies.get(settings.AUTH.SESSION_AUTH_KEY)
    if cookie:
        raise HTTPException(status_code=403, detail="User is authorized")
    return True

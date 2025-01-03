import logging
from datetime import datetime

from fastapi import Request

from api.shared.utils.middlewares import set_anonymous_user, get_session_from_cookie, get_user
from api.users.auth.utils.utils import decrypt_data
from api.users.models import ROLES
from config.settings import settings
from logs.config import configure_logs

configure_logs()
logger = logging.getLogger()


async def auth_session(request: Request, call_next):
    auth_cookie = request.cookies.get(settings.AUTH.SESSION_AUTH_KEY)
    if not auth_cookie:
        logger.warning("The user does not have a session")
        await set_anonymous_user(request)
        response = await call_next(request)
        return response

    session = await get_session_from_cookie(auth_cookie)
    if not session:
        logger.warning("User session is not valid")
        await set_anonymous_user(request)
        response = await call_next(request)
        response.delete_cookie(settings.AUTH.SESSION_AUTH_KEY)
        return response

    if session.expires_at <= datetime.now():
        logger.warning("User session has expired")
        await set_anonymous_user(request)
        response = await call_next(request)
        response.delete_cookie(settings.AUTH.SESSION_AUTH_KEY)
        return response

    _decrypt_sess = decrypt_data(session.data)
    if _decrypt_sess.get("role") == ROLES.ANONYMOUS.label():
        logger.warning("User is not authorized")
        await set_anonymous_user(request)
        response = await call_next(request)
        response.delete_cookie(settings.AUTH.SESSION_AUTH_KEY)
        return response
    request.state.user = await get_user(_decrypt_sess.get("user_id"))
    response = await call_next(request)
    logger.info("[(%s):%s:%s] user visited %s ----> %s",request.state.user.id, request.state.user.username, request.state.user.role, request.url, request.method)
    return response
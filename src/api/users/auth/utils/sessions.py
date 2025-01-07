from datetime import datetime
from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession

from api.users.auth.models import Session
from api.users.auth.repository import SessionRepository
from api.users.auth.utils.utils import decrypt_data
from api.users.models import User
from api.users.repository import UserRepository


class SessionsTypes(Enum):
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"


async def check_email_session(sessions_id, session: AsyncSession)-> User | bool:
    session_obj: Session = await SessionRepository(session).get_by_id(id=sessions_id)
    if session_obj.expires_at <= datetime.now():
        return False

    _decrypt_session: dict = decrypt_data(session_obj.data)
    if not _decrypt_session.get("session_type") or _decrypt_session.get("session_type") != SessionsTypes.AUTHENTICATION.value:
        return False

    user = await UserRepository(session).get_by_id(_decrypt_session.get("user_id"))
    return user

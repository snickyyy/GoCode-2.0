from datetime import datetime

from fastapi import HTTPException
from pydantic import EmailStr
from pydantic_core import PydanticCustomError

from api.shared.repository import BaseRepository
from api.users.auth.schemas import RegisterUser, UserFilter, CreateSession
from api.users.auth.utils.sessions import SessionsTypes
from api.users.auth.utils.utils import encrypt_data, decrypt_data
from api.users.models import ROLES, User
from api.users.schemas import CreateUser, UpdateUser


class AuthService:
    def __init__(self, user_repository: BaseRepository, session_repository: BaseRepository):
        self.user_repository = user_repository
        self.session_repository = session_repository

    async def create_user(self, schema: RegisterUser):
        user_schema = CreateUser(**schema.model_dump())
        user = await self.user_repository.create(schema=user_schema)
        return user

    async def get_by_username_or_email(self, username_or_email: str):
        try:
            EmailStr._validate(username_or_email)
        except PydanticCustomError:
            schema = UserFilter(username=username_or_email)
        else:
            schema = UserFilter(email=username_or_email)
        result = await self.user_repository.strict_filter(schema, limit=1)
        if not result:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return result[0]

    async def authorize(self, username, password):
        user = await self.get_by_username_or_email(username)
        if user.check_password(password) and user.role != ROLES.ANONYMOUS:
            user.role = ROLES.USER
            user_schema = UpdateUser.from_orm(user)
            await self.user_repository.update(user.id, user_schema)
            return user
        raise HTTPException(status_code=401, detail="Invalid credentials")

    async def create_session(self, user_obj: User, sess_type: SessionsTypes, exp: datetime):
        payload = {
            "session_type": sess_type.value,
            "user_id": user_obj.id,
            "username": user_obj.username,
            "email": user_obj.email,
            "role": user_obj.role,
            "iat": datetime.now().isoformat()
            }
        _encrypt_payload = encrypt_data(payload)
        schema = CreateSession(data=_encrypt_payload, expires_at=exp)
        sess_id = await self.session_repository.create(schema)
        return sess_id

    async def check_email_session(self, sessions_id) -> User | bool:
        session_obj = await self.session_repository.get_by_id(id=sessions_id)
        if session_obj.expires_at <= datetime.now():
            return False

        _decrypt_session: dict = decrypt_data(session_obj.data)
        if not _decrypt_session.get("session_type") or _decrypt_session.get(
                "session_type") != SessionsTypes.AUTHENTICATION.value:
            return False

        user = await self.user_repository.get_by_id(_decrypt_session.get("user_id"))
        return user

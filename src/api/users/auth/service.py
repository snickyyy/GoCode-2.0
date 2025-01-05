from fastapi import HTTPException
from pydantic import EmailStr
from pydantic_core import PydanticCustomError

from api.shared.repository import BaseRepository
from api.users.auth.schemas import RegisterUser, UserFilter
from api.users.models import ROLES
from api.users.schemas import CreateUser, UpdateUser


class AuthService:
    def __init__(self, user_repository: BaseRepository):
        self.user_repository = user_repository

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

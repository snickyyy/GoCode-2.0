from fastapi import HTTPException
from pydantic import EmailStr
from pydantic_core import PydanticCustomError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.shared.repository import BaseRepository
from api.users.auth.schemas import RegisterUser
from api.users.auth.utils.utils import make_hash
from api.users.models import User, ROLES


class UserRepository(BaseRepository):
    model = User

    async def create(self, schema: RegisterUser, user_type: str | ROLES = ROLES.ANONYMOUS):
        user = self.model(
            username=schema.username,
            email=schema.email,
            role=user_type
            )
        user.set_password(schema.password)
        self.db.add(user)
        try:
            await self.db.commit()
        except IntegrityError:
            raise HTTPException(status_code=409, detail="This username or email already exists")
        return user

    async def get_by_username_or_email(self, username_or_email: str):
        try:
            EmailStr._validate(username_or_email)
        except PydanticCustomError:
            stmt = select(self.model).filter(self.model.username == username_or_email)
        else:
            stmt = select(self.model).filter(self.model.email == username_or_email)
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()
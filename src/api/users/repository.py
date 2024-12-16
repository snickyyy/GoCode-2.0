from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.shared.repository import BaseRepository
from api.users.auth.schemas import RegisterUser
from api.users.auth.utils.utils import make_hash
from api.users.models import User, ROLES


class UserRepository(BaseRepository):
    model = User

    async def create(self, schema: RegisterUser, user_type: str | ROLES = ROLES.ANONYMOUS):
        user = self.model(username=schema.username,
                          email=schema.email,
                          role=user_type
                          )
        user.set_password(schema.password)
        self.db.add(user)
        await self.db.commit()
        return user
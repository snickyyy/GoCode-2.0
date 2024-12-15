from datetime import datetime

from api.shared.repository import BaseRepository
from api.users.auth.models import Session
from api.users.auth.utils.utils import encrypt_data


class SessionRepository(BaseRepository):
    model = Session

    async def create(self, payload: dict, exp: datetime):
        _encrypt_payload = encrypt_data(payload)
        session = self.model(payload=_encrypt_payload, expired_at=exp)
        self.db.add(session)
        await self.db.commit()
        return session.id

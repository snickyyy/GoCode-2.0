import logging
from datetime import datetime

from api.shared.repository import BaseRepository
from api.users.auth.models import Session
from api.users.auth.utils.utils import encrypt_data
from logs.config import configure_logs

configure_logs()
logger = logging.getLogger(__name__)

class SessionRepository(BaseRepository):
    model = Session

    async def create(self, payload: dict, exp: datetime):
        _encrypt_payload = encrypt_data(payload)
        session = self.model(data=_encrypt_payload, expires_at=exp)
        self.db.add(session)
        await self.db.commit()
        logger.debug("Created session <%s>", session.id)
        return session.id

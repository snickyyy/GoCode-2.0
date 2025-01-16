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

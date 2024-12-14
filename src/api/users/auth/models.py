from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from core.models import BaseModel


class Session(BaseModel):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    data: Mapped[str]
    expires_at: Mapped[datetime] = mapped_column(DateTime)

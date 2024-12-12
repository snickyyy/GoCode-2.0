from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

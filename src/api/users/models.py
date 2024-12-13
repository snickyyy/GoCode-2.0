from enum import Enum

from sqlalchemy import String, Enum as SQLAlchemyEnum, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy_utils import ChoiceType

from core.models import BaseModel

# ROLE_CHOICES = {
#     "anonymous": 0,
#     "user": 1,
#     "admin": 2,
# }


class ROLES(Enum):
    ANONYMOUS = 0, "anonymous"
    USER = 1, "user"
    ADMIN = 2, "admin"

    def __str__(self):
        return self.name


class User(BaseModel):
    username: Mapped[str] = mapped_column(String(25))
    password: Mapped[str]
    email: Mapped[str] = mapped_column(String(180))
    description: Mapped[str] = mapped_column(String(120), nullable=True)
    role: Mapped[ROLES] = mapped_column(ChoiceType(ROLES, impl=Integer()))
    image: Mapped[str] = mapped_column(nullable=True)


us1 = User(
    username="snicky",
    password="qwerty",
    email="qwerty@gmail.com",
    description="good",
    role="admin",
)
print(us1)

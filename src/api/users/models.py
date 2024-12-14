from enum import Enum
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Enum as SQLAlchemyEnum, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from sqlalchemy_utils import ChoiceType

from core.models import BaseModel

if TYPE_CHECKING:
    from api.problems.models import Solution
    from api.forum.models import Post


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

    solutions: Mapped[List["Solution"]] = relationship(
        "Solution", backref="user", passive_deletes=True
    )
    posts: Mapped[List["Post"]] = relationship(
        "Post", backref="user", passive_deletes=True
    )

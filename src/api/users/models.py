from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ChoiceType
from api.users.auth.utils.utils import make_hash, check_hash
from core.models import BaseModel
from enum import Enum
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:

    from api.forum.models import Post, Comment


class ROLES(Enum):
    ANONYMOUS = 0, "anonymous"
    USER = 1, "user"
    ADMIN = 2, "admin"

    def __new__(cls, value, label):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj

    def __str__(self):
        return self.label

    @classmethod
    def get_value_by_label(cls, label: str):
        for role in cls:
            if role.label == label.lower():
                return role.value
        raise ValueError(f"No matching role found for label: {label}")


class User(BaseModel):
    username: Mapped[str] = mapped_column(String(25))
    password: Mapped[str]
    email: Mapped[str] = mapped_column(String(180))
    description: Mapped[str] = mapped_column(String(120), nullable=True)
    role: Mapped[ROLES] = mapped_column(ChoiceType(ROLES, impl=Integer()))
    image: Mapped[str] = mapped_column(nullable=True)

    from api.problems.models import Solution
    solutions = relationship("Solution", back_populates="user", cascade="all, delete-orphan", lazy="selectin")
    posts: Mapped[List["Post"]] = relationship(
        "Post", backref="user", passive_deletes=True
    )
    comments: Mapped[List["Comment"]] = relationship("Comment", backref="user")

    def set_password(self, password):
        self.password = make_hash(password).decode()

    def check_password(self, password):
        return check_hash(password, self.password)

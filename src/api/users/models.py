from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ChoiceType
from api.users.auth.utils.utils import make_hash, check_hash
from core.models import BaseModel
from enum import Enum


class ROLES(Enum):
    ANONYMOUS = 0
    USER = 1
    ADMIN = 2

    def label(self):
        return self.name.lower()

    @classmethod
    def get_value_by_label(cls, label: str):
        for role in cls:
            if role.label() == label.lower():
                return role.value
        raise ValueError(f"No matching role found for label: {label}")


class User(BaseModel):
    username: Mapped[str] = mapped_column(String(25), unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(String(180), unique=True)
    description: Mapped[str] = mapped_column(String(120), nullable=True)
    role: Mapped[ROLES] = mapped_column(ChoiceType(ROLES, impl=Integer()))
    image: Mapped[str] = mapped_column(nullable=True)

    from api.problems.models import Solution
    solutions = relationship("Solution", back_populates="user", cascade="all, delete-orphan", lazy="selectin")
    from api.forum.models import Post, Comment
    posts = relationship("Post", back_populates="user", passive_deletes=True)
    comments = relationship("Comment", back_populates="user", passive_deletes=True)

    def set_password(self, password):
        self.password = make_hash(password).decode()

    def check_password(self, password):
        return check_hash(password, self.password)

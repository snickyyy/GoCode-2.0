import asyncio
from random import choices
from string import ascii_letters, digits

from faker import Faker
from fastapi import HTTPException
from sqlalchemy import String, Integer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ChoiceType
from api.users.auth.utils.utils import make_hash, check_hash
from config.db import db_handler
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_authenticated = self.role != ROLES.ANONYMOUS

    def authenticate(self):
        if self.role != ROLES.ANONYMOUS:
            self.is_authenticated = True

    def set_password(self, password):
        self.password = make_hash(password).decode()

    def check_authenticated(self):
        return self.role != ROLES.ANONYMOUS

    def check_password(self, password):
        return check_hash(password, self.password)

    @classmethod
    async def generate_users(cls, count):
        f = Faker("en")
        users = []
        for i in range(count):
            users.append(cls(
                username="".join(choices(ascii_letters + digits, k=20)),
                password=f.password(length=12),
                email="".join(choices(ascii_letters + digits, k=40)) + "@example.com",
                role=ROLES.USER)
            )

        async with db_handler.get_session_context() as session:
            session.add_all(users)
            await session.commit()
        return users

    @classmethod
    async def create_admin_user(cls, username: str, password: str, email: str):
        user = cls(username=username, email=email, role=ROLES.ADMIN)
        user.set_password(password)
        async with db_handler.get_session_context() as session:
            session.add(user)
            await session.commit()
        return user

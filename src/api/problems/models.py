from enum import Enum
from typing import List

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ChoiceType

from core.models import BaseModel

class DIFFICULTLY_CHOICES(Enum):
    EASY = 1, 'easy'
    MEDIUM = 2,'medium'
    HARD = 3, 'hard'

class TASK_STATUS_CHOICES(Enum):
    IN_DEVELOPMENT = 0, "In-Development"
    ACCEPTED = 1, "Accepted"

class Category(BaseModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(50))

    tasks: Mapped[List["Task"]] = relationship("Task", backref="category",passive_deletes=True)


class Language(BaseModel):
    name: Mapped[str] = mapped_column(String(28))


class Test(BaseModel):
    path: Mapped[str] = mapped_column(String(280))

    task: Mapped["Task"] = relationship("Task", backref="test", passive_deletes=True)


class Task(BaseModel):
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    difficulty: Mapped[int] = mapped_column(ChoiceType(DIFFICULTLY_CHOICES, impl=Integer()))
    category: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    tests: Mapped[int] = mapped_column(ForeignKey("tests.id", ondelete="CASCADE"))
    constraints: Mapped[str] = mapped_column(String(100))
    image: Mapped[str]


# class Solution(BaseModel):
#     user: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
#     solution: Mapped[str] = mapped_column(String(1445))
#     task: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))


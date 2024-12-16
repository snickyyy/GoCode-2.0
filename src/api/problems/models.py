from enum import Enum
from typing import List, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, Mapper
from sqlalchemy_utils import ChoiceType

from core.models import BaseModel

if TYPE_CHECKING:
    from api.users.models import User

class DIFFICULTLY_CHOICES(Enum):
    EASY = 1, "easy"
    MEDIUM = 2, "medium"
    HARD = 3, "hard"


class TASK_STATUS_CHOICES(Enum):
    IN_DEVELOPMENT = 0, "In-Development"
    ACCEPTED = 1, "Accepted"


class Category(BaseModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(50), unique=True)

    tasks = relationship("Task", back_populates="category", passive_deletes=True)


class Language(BaseModel):
    name: Mapped[str] = mapped_column(String(28), unique=True)

    solutions = relationship("Solution", back_populates="language", passive_deletes=True)


class Test(BaseModel):
    path: Mapped[str] = mapped_column(String(280))

    task: Mapped["Task"] = relationship("Task", back_populates="test", passive_deletes=True)


class Task(BaseModel):
    title: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(255))
    difficulty: Mapped[int] = mapped_column(
        ChoiceType(DIFFICULTLY_CHOICES, impl=Integer())
    )
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id", ondelete="CASCADE"))
    constraints: Mapped[str] = mapped_column(String(100))
    image: Mapped[str]

    solutions = relationship("Solution", back_populates="task", passive_deletes=True)
    category = relationship("Category", back_populates="tasks", passive_deletes=True, uselist=True)
    test = relationship("Test", back_populates="task", passive_deletes=True)


class Solution(BaseModel):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    solution: Mapped[str] = mapped_column(String(1445))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id", ondelete="CASCADE"))
    status: Mapped[int] = mapped_column(ChoiceType(TASK_STATUS_CHOICES, impl=Integer()))
    time: Mapped[int]
    memory: Mapped[int]
    test_passed: Mapped[int]

    user = relationship("User", back_populates="solutions", passive_deletes=True, uselist=True)
    task = relationship("Task", back_populates="solutions", passive_deletes=True, uselist=True)
    language  = relationship("Language", back_populates="solutions", passive_deletes=True, uselist=True)
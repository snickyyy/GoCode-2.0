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

    name: Mapped[str] = mapped_column(String(50))

    tasks: Mapped[List["Task"]] = relationship(
        "Task", backref="category", passive_deletes=True
    )


class Language(BaseModel):
    name: Mapped[str] = mapped_column(String(28))

    solutions: Mapped[List["Solution"]] = relationship(
        "Solution", backref="language", passive_deletes=True
    )


class Test(BaseModel):
    path: Mapped[str] = mapped_column(String(280))

    task: Mapped["Task"] = relationship("Task", backref="test", passive_deletes=True)


class Task(BaseModel):
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    difficulty: Mapped[int] = mapped_column(
        ChoiceType(DIFFICULTLY_CHOICES, impl=Integer())
    )
    category: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE")
    )
    tests: Mapped[int] = mapped_column(ForeignKey("tests.id", ondelete="CASCADE"))
    constraints: Mapped[str] = mapped_column(String(100))
    image: Mapped[str]

    solutions: Mapped[List["Solution"]] = relationship(
        "Solution", backref="tasks", passive_deletes=True
    )


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
    task: Mapped["Task"] = relationship("Task", backref="solutions", passive_deletes=True)
    language: Mapped["Language"] = relationship("Language", backref="solutions", passive_deletes=True)
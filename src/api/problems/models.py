from enum import Enum
import random
from typing import List, TYPE_CHECKING

from faker import Faker
from sqlalchemy import String, ForeignKey, Integer, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, Mapper
from sqlalchemy_utils import ChoiceType

from core.models import BaseModel

if TYPE_CHECKING:
    from api.users.models import User

class DIFFICULTLY_CHOICES(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

    def label(self):
        return self.name.lower()

    @classmethod
    def get_value_by_label(cls, label: str):
        for role in cls:
            if role.label() == label.lower():
                return role.value
        raise ValueError(f"No matching role found for label: {label}")


class TASK_STATUS_CHOICES(Enum):
    IN_DEVELOPMENT = 0
    ACCEPTED = 1

    def label(self):
        return self.name.lower()

    @classmethod
    def get_value_by_label(cls, label: str):
        for role in cls:
            if role.label() == label.lower():
                return role.value
        raise ValueError(f"No matching role found for label: {label}")



class Category(BaseModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(50), unique=True)

    tasks = relationship("Task", back_populates="category", passive_deletes=True)

    @classmethod
    async def generate_categories(cls, session):
        choices = ["Math", "DataBase", "Algorithms"]
        categories = [cls(name=name) for name in choices]
        session.add_all(categories)
        await session.commit()

        return categories


class Language(BaseModel):
    name: Mapped[str] = mapped_column(String(28), unique=True)

    solutions = relationship("Solution", back_populates="language", passive_deletes=True)

    @classmethod
    async def generate_languages(cls, session):
        choices = ["Python", "Java", "JavaScript", "C++", "C#", "C", "PHP", "Rust"]
        languages = [cls(name=name) for name in choices]
        session.add_all(languages)
        await session.commit()

        return languages


class Test(BaseModel):
    path: Mapped[str] = mapped_column(String(280))

    task: Mapped["Task"] = relationship("Task", back_populates="test", passive_deletes=True)

    @classmethod
    async def generate_tests(cls, count, session):
        f = Faker("EN")
        all_tests = []
        for i in range(count):
            test = cls(path=f.file_path(5))
            session.add(test)
            all_tests.append(test)
        session.add_all(all_tests)
        await session.commit()
        return all_tests


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
    category = relationship("Category", back_populates="tasks", passive_deletes=True, lazy="joined")
    test = relationship("Test", back_populates="task", passive_deletes=True)

    @classmethod
    async def generate_tasks(cls, count, session: AsyncSession):
        f = Faker("EN")
        all_tasks = []
        for i in range(count):

            task = cls(
                title=f.sentence(nb_words=5),
                description=f.text(max_nb_chars=255),
                difficulty=random.choice([DIFFICULTLY_CHOICES.MEDIUM, DIFFICULTLY_CHOICES.EASY, DIFFICULTLY_CHOICES.HARD]),
                category_id=random.randint(1, 3),
                test_id=random.randint(1, 10),
                constraints=f.text(max_nb_chars=100),
                image=f.image_url(),
            )
            all_tasks.append(task)
        session.add_all(all_tasks)
        await session.commit()
        return all_tasks


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

    @classmethod
    async def generate_solutions(cls, count, session: AsyncSession):
        f = Faker("EN")
        all_solutions = []
        for i in range(count):
            task = cls(
                user_id=2,
                solution=f.text(max_nb_chars=555),
                task_id=random.randint(1, count),
                language_id=random.randint(1, 8),
                status=random.choice([TASK_STATUS_CHOICES.ACCEPTED, TASK_STATUS_CHOICES.IN_DEVELOPMENT]),
                time=random.randint(10,1000),
                memory=random.randint(1,25),
                test_passed=random.randint(10,100)
            )
            all_solutions.append(task)
        session.add_all(all_solutions)
        await session.commit()
        return all_solutions

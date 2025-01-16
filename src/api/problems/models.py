from enum import Enum
import random
from random import choice

from faker import Faker
from sqlalchemy import String, ForeignKey, Integer, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ChoiceType

from config.db import db_handler
from core.models import BaseModel

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
    async def generate_categories(cls):
        choices = ["Math", "DataBase", "Algorithms"]
        categories = [cls(name=name) for name in choices]
        async with db_handler.get_session_context() as session:
            session.add_all(categories)
            await session.commit()
        return categories


class Language(BaseModel):
    name: Mapped[str] = mapped_column(String(28), unique=True)

    solutions = relationship("Solution", back_populates="language", passive_deletes=True)

    @classmethod
    async def generate_languages(cls):
        choices = ["Python", "Java", "JavaScript", "C++", "C#", "C", "PHP", "Rust"]
        languages = [cls(name=name) for name in choices]
        async with db_handler.get_session_context() as session:
            session.add_all(languages)
            await session.commit()

        return languages


class Test(BaseModel):
    path: Mapped[str] = mapped_column(String(280))

    task: Mapped["Task"] = relationship("Task", back_populates="test", passive_deletes=True)

    @classmethod
    async def generate_tests(cls, count):
        f = Faker("EN")
        all_tests = []
        for i in range(count):
            test = cls(path=f.file_path(5))
            all_tests.append(test)

        async with db_handler.get_session_context() as session:
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
    async def generate_tasks(cls, count):
        f = Faker("EN")
        all_tasks = []
        async with db_handler.get_session_context() as session:
            categories = await session.execute(select(Category.id))
            tests = await session.execute(select(Test.id))
            result_category = categories.scalars().all()
            result_test = tests.scalars().all()
            for i in range(count):
                task = cls(
                    title=f.sentence(nb_words=5),
                    description=f.text(max_nb_chars=255),
                    difficulty=random.choice([DIFFICULTLY_CHOICES.MEDIUM, DIFFICULTLY_CHOICES.EASY, DIFFICULTLY_CHOICES.HARD]),
                    category_id=random.choice(result_category),
                    test_id=random.choice(result_test),
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
    async def generate_solutions(cls, count, task_id=None):
        f = Faker("EN")
        all_solutions = []
        async with db_handler.get_session_context() as session:
            from api.users.models import User
            users = await session.execute(select(User.id))
            tasks = await session.execute(select(Task.id))
            languages = await session.execute(select(Language.id))
            result_users = users.scalars().all()
            result_tasks = tasks.scalars().all()
            result_languages = languages.scalars().all()

            for i in range(count):
                task = cls(
                    user_id=random.choice(result_users),
                    solution=f.text(max_nb_chars=555),
                    task_id=task_id if task_id else choice(result_tasks),
                    language_id=random.choice(result_languages),
                    status=random.choice([TASK_STATUS_CHOICES.ACCEPTED, TASK_STATUS_CHOICES.IN_DEVELOPMENT]),
                    time=random.randint(10,1000),
                    memory=random.randint(1,25),
                    test_passed=random.randint(10,100)
                )
                all_solutions.append(task)
            session.add_all(all_solutions)
            await session.commit()
        return all_solutions

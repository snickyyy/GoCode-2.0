from pydantic import BaseModel, model_validator, root_validator, ConfigDict, validator, field_validator

from api.problems.models import DIFFICULTLY_CHOICES, TASK_STATUS_CHOICES


class TaskList(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    category: str

class TaskDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    category: str
    difficulty: str
    image: str | None = None

    @field_validator("difficulty", mode="before")
    @classmethod
    def clean_difficulty(cls, value):
        shielding_value = value.label()
        return shielding_value

    @field_validator("category", mode="before")
    @classmethod
    def clean_category(cls, value):
        return value.name

class SubmitTask(BaseModel):
    code: str
    language: str

    @field_validator("language", mode="after")
    @classmethod
    def clean_language(cls, value: str):
        return value.capitalize()

class SolutionFilter(BaseModel):
    task_id: int|None = None
    user_id: int|None = None
    language_id: int|None = None
    status: TASK_STATUS_CHOICES|None = None

class UpdateSolution(BaseModel):
    solution: str
    status: TASK_STATUS_CHOICES
    time: int
    memory: int
    test_passed: int

class CreateSolution(UpdateSolution):
    user_id: int
    task_id: int
    language_id: int

class LanguageFilter(BaseModel):
    name: str

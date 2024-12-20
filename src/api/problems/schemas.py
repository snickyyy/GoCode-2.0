from pydantic import BaseModel, model_validator, root_validator, ConfigDict, validator, field_validator

from api.problems.models import DIFFICULTLY_CHOICES


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

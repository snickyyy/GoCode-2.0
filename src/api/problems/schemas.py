from pydantic import BaseModel, model_validator, root_validator


class TaskList(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    category: str

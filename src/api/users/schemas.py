from pydantic import BaseModel, EmailStr

from api.users.models import ROLES


class UserProfile(BaseModel):
    username: str
    email: EmailStr
    description: str|None = None
    image: str|None = None
    total_posts: int = 0
    total_solutions: int = 0


class CreateUser(BaseModel):
    username: str
    password: str
    email: EmailStr
    description: str|None = None
    role: ROLES = ROLES.ANONYMOUS
    image: str|None = None

class UpdateUser(CreateUser):
    ...

    class Config:
        from_attributes=True

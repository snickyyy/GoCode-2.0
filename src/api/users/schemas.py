from pydantic import BaseModel, EmailStr


class UserProfile(BaseModel):
    username: str
    email: EmailStr
    description: str|None = None
    image: str|None = None
    total_posts: int = 0
    total_solutions: int = 0

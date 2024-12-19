from pydantic import BaseModel, EmailStr


class UserInfo(BaseModel):
    username: str
    email: EmailStr
    description: str|None = None


from pydantic import BaseModel, EmailStr, Field


class RegisterUser(BaseModel):
    username: str
    password: str
    email: EmailStr



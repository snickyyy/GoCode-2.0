from pydantic import BaseModel, EmailStr, Field


class RegisterUser(BaseModel):
    username: str
    password: str
    email: EmailStr

class LoginUser(BaseModel):
    username_or_email: str
    password: str



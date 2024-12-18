import re

from pydantic import BaseModel, EmailStr, field_validator


class RegisterUser(BaseModel):
    username: str
    password: str
    email: EmailStr

    # @field_validator("password")
    # def validate_password(cls, value):
    #     pattern = '^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'
    #     if not re.match(pattern, value):
    #         raise ValueError(
    #             "Password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, one digit, and one special character."
    #         )
    #     return value
    #
    # @field_validator("username")
    # def validate_username(cls, value):
    #     pattern = r'^[a-zA-Z0-9_.]+$'
    #     if not re.match(pattern, value):
    #         raise ValueError("Username can only contain English letters, digits, underscores (_), and dots (.)")
    #     return value

class LoginUser(BaseModel):
    username_or_email: str
    password: str



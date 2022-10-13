import string
from typing import Optional

from pydantic import BaseModel, EmailStr, validator

from tortoise.contrib.pydantic import pydantic_model_creator

from .models import User


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserAuth):
    first_name: str
    username: str

    @validator("password")
    def password_length(cls, instance):
        if len(instance) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")

    @validator("password")
    def password_complexity(cls, instance):
        if not any(sym for sym in instance if sym in string.ascii_letters):
            raise ValueError("Пароль должен содержать минимум 1 символ" "(a-z, A-Z)")
        return instance


class ProfileSchema(BaseModel):
    id: str
    first_name: Optional[str]
    username: Optional[str]
    email: Optional[str]


user_pydantic_model = pydantic_model_creator(User, name="user")

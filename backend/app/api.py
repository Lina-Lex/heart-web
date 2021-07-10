from typing import Optional

from pydantic import BaseModel
from stringcase import camelcase


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    username: str
    email: Optional[str]
    full_name: str

    class Config:
        alias_generator = camelcase
        allow_population_by_field_name = True


class UserCreate(User):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str

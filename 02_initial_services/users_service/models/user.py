import typing as tp
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    name: str
    surname: str
    age: tp.Optional[int] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

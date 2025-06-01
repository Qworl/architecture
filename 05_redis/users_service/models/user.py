from pydantic import BaseModel, EmailStr
import typing as tp

class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: str
    surname: str
    age: tp.Optional[int] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

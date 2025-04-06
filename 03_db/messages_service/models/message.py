from pydantic import BaseModel


class MessageBase(BaseModel):
    """Базовая модель сообщения"""
    value: str
    author: int  # user_id


class MessageCreate(MessageBase):
    """Модель для создания сообщения"""
    pass


class Message(MessageBase):
    """Полная модель сообщения"""
    id: int

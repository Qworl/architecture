from datetime import datetime
from pydantic import BaseModel


class MessageBase(BaseModel):
    """Базовая модель сообщения"""    
    content: str
    author: int  # user_id


class MessageCreate(MessageBase):
    """Модель для создания сообщения"""
    pass


class Message(MessageBase):
    """Полная модель сообщения"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

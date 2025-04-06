import typing as tp

from models.message import Message


messages_db: tp.List[Message] = [
    Message(
        id=1,
        value="Hello, world!",
        author=1,
    )
]
import typing as tp

import fastapi
from fastapi import security
from fastapi import HTTPException
import jose
from jose import jwt

from models import message as message_model
from db.db import messages_db
from constants import auth as auth_constants

oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = fastapi.Depends(oauth2_scheme)):
    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, auth_constants.SECRET_KEY, algorithms=[auth_constants.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except jose.JWTError:
        raise credentials_exception


router = fastapi.APIRouter(
    prefix="/messages",
    tags=["messages"],
    dependencies=[fastapi.Depends(get_current_user)],
)


# GET /messages - Получить все сообщения
@router.get("/list", response_model=list[message_model.Message])
def get_messages(
    author_id: tp.Optional[int] = fastapi.Query(None, description="ID автора сообщения"),
    current_user: dict = fastapi.Depends(get_current_user),
):
    """Получить список всех сообщений с возможностью фильтрации по автору"""
    if author_id is not None:
        filtered_messages = [msg for msg in messages_db if msg.author == author_id]
        if not filtered_messages:
            raise HTTPException(
                status_code=404, detail=f"Messages from author with id {author_id} not found"
            )
        return filtered_messages

    return messages_db


# GET /messages/{message_id} - Получить сообщение по ID
@router.get("/details", response_model=message_model.Message)
def get_message(
    message_id: int,
    current_user: dict = fastapi.Depends(get_current_user),
):
    """Получить сообщение по ID"""
    for message in messages_db:
        if message.id == message_id:
            return message
    raise HTTPException(status_code=404, detail="Message not found")


# POST /messages - Создать новое сообщение
@router.post("/create", response_model=message_model.Message, status_code=201)
def create_message(
    message: message_model.MessageCreate,
    current_user: dict = fastapi.Depends(get_current_user),
):
    """Создать новое сообщение"""
    message_id = 1 if not messages_db else max(msg.id for msg in messages_db) + 1

    new_message = message_model.Message(
        id=message_id,
        value=message.value,
        author=message.author,
    )

    messages_db.append(new_message)
    return new_message


# PUT /messages/{message_id} - Обновить сообщение по ID
@router.put("/update", response_model=message_model.Message)
def update_message(
    message_id: int,
    message_update: message_model.MessageBase,
    current_user: dict = fastapi.Depends(get_current_user),
):
    """Обновить существующее сообщение"""
    for index, message in enumerate(messages_db):
        if message.id == message_id:
            if message_update.author != message.author:
                raise HTTPException(status_code=403, detail="You are not allowed to update this message")
            updated_message = message_model.Message(
                id=message_id,
                value=message_update.value,
                author=message_update.author,
            )
            messages_db[index] = updated_message
            return updated_message
    raise HTTPException(status_code=404, detail="Message not found")


# DELETE /messages/{message_id} - Удалить сообщение по ID
@router.delete("/delete", response_model=message_model.Message)
def delete_message(
    message_id: int,
    current_user: dict = fastapi.Depends(get_current_user),
):
    """Удалить сообщение по ID"""
    for index, message in enumerate(messages_db):
        if message.id == message_id:
            if message.author != current_user:
                raise HTTPException(status_code=403, detail="You are not allowed to delete this message")
            deleted_message = messages_db.pop(index)
            return deleted_message
    raise HTTPException(status_code=404, detail="Message not found") 
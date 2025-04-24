import typing as tp
from typing import List
import json

import fastapi
from fastapi import security, APIRouter, Query
from fastapi import HTTPException
import jose
from jose import jwt
from bson import ObjectId
from pymongo.asynchronous import collection
from datetime import datetime

from models import message as message_model
from db import db as messages_db
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


router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    dependencies=[fastapi.Depends(get_current_user)],
)


def convert_mongodb_to_message(message: dict) -> message_model.Message:
    """Преобразует документ MongoDB в модель Message."""
    if isinstance(message, str):
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            raise ValueError("Invalid message format: expected JSON string")
    
    if not isinstance(message, dict):
        raise ValueError("Invalid message format: expected dictionary")
    
    message_data = {
        "id": str(message["_id"]),
        "content": message["value"],
        "author": int(message["author"]),
        "created_at": message.get("created_at", datetime.utcnow()),
        "updated_at": message.get("updated_at", datetime.utcnow())
    }
    return message_model.Message(**message_data)


# GET /messages - Получить все сообщения
@router.get("/list", response_model=list[message_model.Message])
async def get_messages(
    author_id: tp.Optional[int] = fastapi.Query(None, description="ID автора сообщения"),
    limit: int = 50,
    offset: int = 0,
    collection: collection.AsyncCollection = fastapi.Depends(messages_db.get_collection),
):
    """Получить список сообщений с пагинацией."""
    filter_query = {}
    if author_id is not None:
        filter_query["author"] = author_id
    
    cursor = collection.find(filter_query).skip(offset).limit(limit)
    messages = []
    async for message in cursor:
        print(f"Raw message from MongoDB: {message}")  # Добавляем логирование
        messages.append(convert_mongodb_to_message(message))
    return messages


# GET /messages/search - Поиск сообщений по тексту
@router.get("/search", response_model=List[message_model.Message])
async def search_messages(
    query: str = Query(..., description="Текст для поиска"),
    collection: collection.AsyncCollection = fastapi.Depends(messages_db.get_collection),
):
    """Поиск сообщений по тексту."""
    messages = []
    cursor = collection.find(
        {"$text": {"$search": query}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})])
    
    async for message in cursor:
        messages.append(convert_mongodb_to_message(message))
    
    if not messages:
        raise HTTPException(
            status_code=404,
            detail=f"Сообщения по запросу '{query}' не найдены"
        )
    
    return messages


# GET /messages/{message_id} - Получить сообщение по ID
@router.get("/details", response_model=message_model.Message)
async def get_message(
    message_id: str,
    collection: collection.AsyncCollection = fastapi.Depends(messages_db.get_collection),
):
    """Получить сообщение по ID."""
    if (message := await collection.find_one({"_id": ObjectId(message_id)})) is not None:
        return convert_mongodb_to_message(message)
    raise HTTPException(status_code=404, detail=f"Сообщение {message_id} не найдено")


# POST /messages - Создать новое сообщение
@router.post("/create", response_model=message_model.Message, status_code=201)
async def create_message(
    message: message_model.MessageCreate,
    collection: collection.AsyncCollection = fastapi.Depends(messages_db.get_collection),
):
    """Создать новое сообщение."""
    message_dict = {
        "value": message.content,
        "author": message.author,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await collection.insert_one(message_dict)
    created_message = await collection.find_one({"_id": result.inserted_id})
    return convert_mongodb_to_message(created_message)


# PUT /messages/{message_id} - Обновить сообщение по ID
@router.put("/update", response_model=message_model.Message)
async def update_message(
    message_id: str,
    message: message_model.Message,
    collection: collection.AsyncCollection = fastapi.Depends(messages_db.get_collection),
):
    """Обновить сообщение."""
    current_message = await collection.find_one({"_id": ObjectId(message_id)})
    if not current_message:
        raise HTTPException(status_code=404, detail=f"Сообщение {message_id} не найдено")
    
    message_dict = {
        "value": message.content,
        "author": message.author,
        "created_at": current_message["created_at"],
        "updated_at": datetime.utcnow()
    }
    
    update_result = await collection.update_one(
        {"_id": ObjectId(message_id)},
        {"$set": message_dict}
    )
    
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail=f"Сообщение {message_id} не найдено")
    
    updated_message = await collection.find_one({"_id": ObjectId(message_id)})
    return convert_mongodb_to_message(updated_message)


# DELETE /messages/{message_id} - Удалить сообщение по ID
@router.delete("/delete", status_code=204)
async def delete_message(
    message_id: str,
    collection: collection.AsyncCollection = fastapi.Depends(messages_db.get_collection),
):
    """Удалить сообщение."""
    delete_result = await collection.delete_one({"_id": ObjectId(message_id)})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Сообщение {message_id} не найдено") 
import json
import typing as tp
import os

import redis.asyncio as redis
import fastapi

from models.user import User

# Константы
REDIS_HOST = os.getenv("REDIS_HOST", "redis-db")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
USER_DETAILS_TTL = 60 * 10  # 10 минут
USERS_LIST_TTL = 60 * 5  # 5 минут

# Глобальное состояние
redis_client: tp.Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    return redis_client


async def close_redis_connection() -> None:
    global redis_client
    if redis_client is not None:
        await redis_client.aclose()
        redis_client = None


def user_details_key(user_id: int) -> str:
    return f"user:details:{user_id}"


def users_list_key(
    login: tp.Optional[str] = None,
    name: tp.Optional[str] = None,
    surname: tp.Optional[str] = None,
) -> str:
    params = f"login:{login or 'None'}:name:{name or 'None'}:surname:{surname or 'None'}"
    return f"users:list:{params}"


def serialize_user(user: User) -> str:
    return json.dumps(user.model_dump())


def deserialize_user(user_data: str) -> User:
    data = json.loads(user_data)
    return User(**data)


def serialize_user_list(users: tp.List[User]) -> str:
    return json.dumps([user.model_dump() for user in users])


def deserialize_user_list(users_data: str) -> tp.List[User]:
    data = json.loads(users_data)
    return [User(**user_data) for user_data in data]


async def get_cached_user(
    user_id: int,
    redis: redis.Redis = fastapi.Depends(get_redis),
) -> tp.Optional[User]:
    key = user_details_key(user_id)
    data = await redis.get(key)
    if data:
        return deserialize_user(data)
    return None


async def cache_user(
    user: User,
    redis: redis.Redis = fastapi.Depends(get_redis),
) -> None:
    key = user_details_key(user.id)
    await redis.set(key, serialize_user(user), ex=USER_DETAILS_TTL)


async def get_cached_users(
    login: tp.Optional[str] = None,
    name: tp.Optional[str] = None,
    surname: tp.Optional[str] = None,
    redis: redis.Redis = fastapi.Depends(get_redis),
) -> tp.Optional[tp.List[User]]:
    key = users_list_key(login, name, surname)
    data = await redis.get(key)
    if data:
        return deserialize_user_list(data)
    return None


async def cache_users(
    users: tp.List[User],
    login: tp.Optional[str] = None,
    name: tp.Optional[str] = None,
    surname: tp.Optional[str] = None,
    redis: redis.Redis = fastapi.Depends(get_redis),
) -> None:
    key = users_list_key(login, name, surname)
    await redis.set(key, serialize_user_list(users), ex=USERS_LIST_TTL)


async def invalidate_user_cache(
    user_id: int,
    redis: redis.Redis = fastapi.Depends(get_redis),
) -> None:
    key = user_details_key(user_id)
    await redis.delete(key)
    await invalidate_users_list_cache(redis)


async def invalidate_users_list_cache(
    redis: redis.Redis = fastapi.Depends(get_redis),
) -> None:
    pattern = "users:list:*"
    cursor = 0
    while True:
        cursor, keys = await redis.scan(cursor, pattern, 100)
        if keys:
            await redis.delete(*keys)
        if cursor == 0:
            break
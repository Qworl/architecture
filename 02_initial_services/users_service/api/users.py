import typing as tp

import fastapi
from fastapi import security

from models import user as user_model
from models import token as token_model
import jose
from jose import jwt

import constants.auth as auth_constants
import auth.auth as auth
from db.db import users_db

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
        token_data = token_model.TokenData(username=username)
    except jose.JWTError:
        raise credentials_exception

    if token_data.username not in auth_constants.AUTH_USERS_DB:
        raise credentials_exception

    user = auth_constants.AUTH_USERS_DB[token_data.username]
    if not user:
        raise credentials_exception
    return user


router = fastapi.APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[fastapi.Depends(get_current_user)],
)


# GET /users/validate-token - Проверить токен на корректность
@router.get("/validate-token")
def validate_token(current_user: dict = fastapi.Depends(get_current_user)):
    return {"message": "OK"}


# GET /users - Получить всех пользователей
@router.get("/list", response_model=tp.List[user_model.User])
def get_users(
    login: tp.Optional[str] = fastapi.Query(
        None, description="Логин пользователя для поиска"
    ),
    name: tp.Optional[str] = fastapi.Query(
        None, description="Имя пользователя для поиска"
    ),
    surname: tp.Optional[str] = fastapi.Query(
        None, description="Фамилия пользователя для поиска"
    ),
    current_user: dict = fastapi.Depends(get_current_user),
):
    # Поиск по логину (имеет приоритет)
    if login is not None:
        user_by_login = find_user_by_login(login)
        if not user_by_login:
            raise fastapi.HTTPException(
                status_code=404, detail=f"Пользователь с логином {login} не найден"
            )
        return user_by_login

    # Поиск по имени и/или фамилии
    if name is not None or surname is not None:
        return find_users_by_name_and_surname(name, surname)
        
    # Возвращает всех пользователей
    return users_db


def find_user_by_login(login: str) -> tp.List[user_model.User]:
    """Находит пользователей по логину"""
    return [user for user in users_db if user.username == login]


def find_users_by_name_and_surname(
    name: tp.Optional[str], 
    surname: tp.Optional[str]
) -> tp.List[user_model.User]:
    """Находит пользователей по имени и/или фамилии"""
    filtered_users = users_db.copy()
    
    if name is not None:
        filtered_users = [
            user for user in filtered_users if name.lower() in user.name.lower()
        ]
    
    if surname is not None:
        filtered_users = [
            user for user in filtered_users 
            if surname.lower() in user.surname.lower()
        ]
    
    if not filtered_users:
        filter_description = []
        if name:
            filter_description.append(f"имя содержит '{name}'")
        if surname:
            filter_description.append(f"фамилия содержит '{surname}'")
        
        filter_str = " и ".join(filter_description)
        raise fastapi.HTTPException(
            status_code=404, detail=f"Пользователи с параметрами: {filter_str} не найдены"
        )
    
    return filtered_users


# GET /users/details - Получить пользователя по ID
@router.get("/details", response_model=user_model.User)
def get_user(user_id: int, current_user: dict = fastapi.Depends(get_current_user)):
    for user in users_db:
        if user.id == user_id:
            return user
    raise fastapi.HTTPException(status_code=404, detail="User not found")


# POST /users/create - Создать нового пользователя
@router.post("/create", response_model=user_model.User, status_code=201)
def create_user(
    user: user_model.UserCreate,
    current_user: dict = fastapi.Depends(get_current_user),
):
    for u in users_db:
        if u.username == user.username:
            raise fastapi.HTTPException(
                status_code=400, detail="Username already taken"
            )
        if u.email == user.email:
            raise fastapi.HTTPException(
                status_code=400, detail="Email already registered"
            )

    user_id = 1 if not users_db else max(u.id for u in users_db) + 1

    new_user = user_model.User(
        id=user_id,
        username=user.username,
        email=user.email,
        age=user.age,
        name=user.name,
        surname=user.surname,
    )

    hashed_password = auth.get_password_hash(user.password)

    auth.add_user_to_auth_db(
        username=user.username, email=user.email, hashed_password=hashed_password
    )

    users_db.append(new_user)

    return new_user


# PUT /users/update- Обновить пользователя по ID
@router.put("/update", response_model=user_model.User)
def update_user(
    user_id: int,
    user_update: user_model.UserBase,
    current_user: dict = fastapi.Depends(get_current_user),
):
    for index, user in enumerate(users_db):
        if user.id == user_id:
            updated_user = user_model.User(
                id=user_id,
                username=user_update.username,
                email=user_update.email,
                age=user_update.age,
            )
            users_db[index] = updated_user
            return updated_user
    raise fastapi.HTTPException(status_code=404, detail="User not found")


# DELETE /users/delete - Удалить пользователя по ID
@router.delete("/delete", response_model=user_model.User)
def delete_user(
    user_id: int, current_user: dict = fastapi.Depends(get_current_user)
):
    for index, user in enumerate(users_db):
        if user.id == user_id:
            deleted_user = users_db.pop(index)
            return deleted_user
    raise fastapi.HTTPException(status_code=404, detail="User not found")

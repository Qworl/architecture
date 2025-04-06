import typing as tp

import fastapi
from fastapi import security, Depends, APIRouter
from sqlalchemy.orm import Session

from models import user as user_model
from models import token as token_model
import jose
from jose import jwt

import constants.auth as auth_constants
from db.database import get_db
from db import crud

oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = fastapi.Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
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

    user = crud.get_user_by_username(db, username=token_data.username)
    if not user:
        raise credentials_exception
    return user


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[fastapi.Depends(get_current_user)],
)


# GET /users/validate-token - Проверить токен на корректность
@router.get("/validate-token")
def validate_token(current_user: user_model.User = fastapi.Depends(get_current_user)):
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
    db: Session = Depends(get_db),
    current_user: user_model.User = fastapi.Depends(get_current_user),
):
    users = crud.get_user_by_username_or_name_or_surname(db, username=login, name=name, surname=surname)

    if not users:
        filter_str = []
        if login:
            filter_str.append(f"логин содержит '{login}'")
        if name:
            filter_str.append(f"имя содержит '{name}'")
        if surname:
            filter_str.append(f"фамилия содержит '{surname}'")
        filter_str = " и ".join(filter_str)
        raise fastapi.HTTPException(
            status_code=404, 
            detail=f"Пользователи с параметрами: {filter_str} не найдены"
        )        
    return users


# GET /users/details - Получить пользователя по ID
@router.get("/details", response_model=user_model.User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = fastapi.Depends(get_current_user)
):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return user


# POST /users/create - Создать нового пользователя
@router.post("/create", response_model=user_model.User, status_code=201)
def create_user(
    user: user_model.UserCreate,
    db: Session = Depends(get_db),
    current_user: user_model.User = fastapi.Depends(get_current_user),
):
    # Проверяем существование пользователя с таким же username
    if crud.get_user_by_username(db, username=user.username):
        raise fastapi.HTTPException(
            status_code=400, detail="Username already taken"
        )
    # Проверяем существование пользователя с таким же email
    if crud.get_user_by_email(db, email=user.email):
        raise fastapi.HTTPException(
            status_code=400, detail="Email already registered"
        )

    return crud.create_user(db=db, user=user)


# PUT /users/update - Обновить пользователя по ID
@router.put("/update", response_model=user_model.User)
def update_user(
    user_id: int,
    user_update: user_model.UserCreate,
    db: Session = Depends(get_db),
    current_user: user_model.User = fastapi.Depends(get_current_user),
):
    updated_user = crud.update_user(db, user_id=user_id, user=user_update)
    if updated_user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return updated_user


# DELETE /users/delete - Удалить пользователя по ID
@router.delete("/delete", response_model=user_model.User)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = fastapi.Depends(get_current_user)
):
    return crud.delete_user(db, user_id=user_id)

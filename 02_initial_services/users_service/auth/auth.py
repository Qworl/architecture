import typing as tp
import datetime as dt

import passlib.context as passlib_context
from jose import jwt

import constants.auth as auth_constants


pwd_context = passlib_context.CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    if username not in auth_constants.AUTH_USERS_DB:
        return False
    user = auth_constants.AUTH_USERS_DB[username]
    if not verify_password(password, user["hashed_password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: tp.Optional[dt.timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = dt.datetime.now(dt.timezone.utc) + expires_delta
    else:
        expire = dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, auth_constants.SECRET_KEY, algorithm=auth_constants.ALGORITHM)

    return encoded_jwt


def add_user_to_auth_db(username: str, email: str, hashed_password: str):
    auth_constants.AUTH_USERS_DB[username] = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "is_active": True,
    }
import typing as tp
import fastapi

from sqlalchemy.orm import Session
from db import models
from models.user import UserCreate

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_username_or_name_or_surname(db: Session, username: tp.Optional[str] = None, name: tp.Optional[str] = None, surname: tp.Optional[str] = None):
    query = db.query(models.User)
    if username:
        query = query.filter(models.User.username == username)
    if name:
        query = query.filter(models.User.name == name)
    if surname:
        query = query.filter(models.User.surname == surname)

    return query.all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = models.User.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        name=user.name,
        surname=user.surname,
        age=user.age,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.username = user.username
        db_user.email = user.email
        db_user.name = user.name
        db_user.surname = user.surname
        db_user.age = user.age
        if user.password:
            db_user.hashed_password = models.User.get_password_hash(user.password)
        db.commit()
        db.refresh(db_user)
    else:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user 
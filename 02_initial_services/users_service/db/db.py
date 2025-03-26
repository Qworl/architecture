import typing as tp

from models import user as user_models

users_db: tp.List[user_models.User] = [
    user_models.User(
        id=1,
        username="admin",
        email="admin@example.com",
        name="Admin",
        surname="Admin",
        age=30,
    ),
]
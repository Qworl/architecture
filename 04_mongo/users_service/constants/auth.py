SECRET_KEY = "d7e152bc34a34ea3adec8b9c57a14c3bb3b95d64a5a2ed9ce1dcbcf68d302e8d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
AUTH_USERS_DB = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        # "secret"
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "is_active": True,
    }
}
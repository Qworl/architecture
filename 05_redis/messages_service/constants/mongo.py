import os

MONGO_URL = os.getenv("MONGO_URI", "mongodb://mongo-db:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "messages_db")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "messages") 
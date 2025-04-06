from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POSTGRES_USER = os.getenv("DB_LOGIN", "stud")
POSTGRES_PASSWORD = os.getenv("DB_PASSWORD", "stud")
POSTGRES_DB = os.getenv("DB_DATABASE", "archdb")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "6432")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"

# Логирование параметров подключения (без пароля)
logger.info(f"Connecting to database at {DB_HOST}:{DB_PORT}/{POSTGRES_DB} as {POSTGRES_USER}")

try:
    engine = create_engine(DATABASE_URL)
    logger.info("Database connection established successfully")
except Exception as e:
    logger.error(f"Error connecting to database: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
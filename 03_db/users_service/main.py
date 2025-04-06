import contextlib
import json
import os
import logging

import fastapi
from fastapi import responses
from fastapi.middleware import cors

from api import token as token_api
from api import users as users_api

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    logger.info("Application startup")
    with open("openapi.json", "w") as f:
        json.dump(app.openapi(), f)
    yield
    logger.info("Application shutdown")

app = fastapi.FastAPI(
    title="User Management Service",
    description="Сервис для управления пользователями",
    version="1.0.0",
    lifespan=lifespan,
    openapi_url="/user-service/openapi.json"
)

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(token_api.router)
app.include_router(users_api.router)

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to User Management API. Visit /docs for documentation."}

@app.get("/openapi.json", tags=["root"])
def get_operapi():
    return responses.FileResponse(os.path.join("/app", "openapi.json"))

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
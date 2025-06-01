import contextlib
import json
import os

import fastapi
from fastapi import responses
from fastapi.middleware import cors

from api import messages as messages_api


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    with open("openapi.json", "w") as f:
        json.dump(app.openapi(), f)

    yield


app = fastapi.FastAPI(
    title="Message Management Service",
    description="Сервис для управления сообщениями",
    version="1.0.0",
    lifespan=lifespan,
    openapi_url="/message-service/openapi.json"
)

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(messages_api.router)


@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to Message Management API. Visit /docs for documentation."}


@app.get("/openapi.json", tags=["root"])
def get_operapi():
    return responses.FileResponse(os.path.join("/app", "openapi.json"))

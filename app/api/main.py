import logging

from fastapi import FastAPI

from app.config import validate_environment
from app.api.routes.chat import router as chat_router
from app.api.routes.whatsapp import router as whatsapp_router
from app.api.routes.conversation import router as conversations_router

logging.basicConfig(
    level=logging.INFO,
)

validate_environment()

app = FastAPI()

app.include_router(chat_router)
app.include_router(whatsapp_router)
app.include_router(conversations_router)

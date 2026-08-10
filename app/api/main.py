import logging

from fastapi import FastAPI
from app.api.routes.chat import router as chat_router
from app.api.routes.whatsapp import router as whatsapp_router

logging.basicConfig(
    level=logging.INFO,
)

app = FastAPI()

app.include_router(chat_router)
app.include_router(whatsapp_router)

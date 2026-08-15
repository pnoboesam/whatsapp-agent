import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import validate_environment
from app.api.routes.chat import router as chat_router
from app.api.routes.whatsapp import router as whatsapp_router
from app.api.routes.contact import router as contact_router
from app.api.routes.conversation import router as conversations_router

logging.basicConfig(
    level=logging.INFO,
)

validate_environment()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(whatsapp_router)
app.include_router(contact_router)
app.include_router(conversations_router)

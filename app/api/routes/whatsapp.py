import os
from dotenv import load_dotenv

from fastapi import APIRouter, Query, HTTPException, status

load_dotenv()

router = APIRouter(prefix="/api/v1/whatsapp", tags=["whatsapp"])

@router.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
):
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")

    if hub_mode == "subscribe" and hub_verify_token == verify_token:
        return int(hub_challenge)

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Verification failed")

@router.post("/webhook")
def receive_message():
    ...


import os
from dotenv import load_dotenv

from app.agent import agent
from app.services.whatsapp import send_message

from fastapi import APIRouter, Query, HTTPException, Request, status

load_dotenv()

router = APIRouter(prefix="/api/v1/whatsapp", tags=["whatsapp"])

# Check if incoming message is text
def extract_message(payload: dict):

    try:
        value = payload["entry"][0]["changes"][0]["value"]
        messages = value.get("messages")

        if not messages:
            return None

        message = messages[0]

        if message.get("type") != "text":
            return None

        wa_number = message["from"]
        text = message["text"]["body"]

        return wa_number, text

    except (KeyError, IndexError, TypeError):
        return None


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
async def receive_message(request:Request):
    payload = await request.json()

    result = extract_message(payload)

    if result is None:
        return {"status": "ignored"}

    wa_number, text = result

    response = agent.chat(
        wa_number,
        text
    )

    await send_message(
        recipient=wa_number,
        message=response
    )

    return {"status": "ok"}


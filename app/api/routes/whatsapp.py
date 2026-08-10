import os
import hmac
import hashlib
import logging
from dotenv import load_dotenv

from app.agent import agent
from app.services.whatsapp import send_message

from fastapi import APIRouter, Query, HTTPException, Request, status, BackgroundTasks

load_dotenv()
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/whatsapp", tags=["whatsapp"])


def verify_signature(payload: bytes, signature: str | None) -> bool:

    app_secret = os.getenv("META_APP_SECRET")

    if not app_secret or not signature:
        return False

    if not signature.startswith("sha256="):
        return False

    expected_signature = hmac.new(
        app_secret.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()

    received_signature = signature.removeprefix("sha256=")

    return hmac.compare_digest(
        expected_signature,
        received_signature,
    )


async def process_message(wa_number: str, text: str):
    logger.info("Background processing started for %s", wa_number)
    
    try:    
        response = agent.chat(
            wa_number,
            text
        )
        await send_message(
            recipient=wa_number,
            message=response
        )
        logger.info("Background processing completed for %s", wa_number)

    except Exception:
        logger.exception("Message processing failed")



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

        return {
            "wa_number": message["from"],
            "text": message["text"]["body"],
            "message_id": message["id"],
        }

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
async def receive_message(request:Request, background_tasks: BackgroundTasks):
    body = await request.body()

    signature = request.headers.get(
        "X-Hub-Signature-256"
    )

    if not verify_signature(body, signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature",
        )

    payload = await request.json()

    result = extract_message(payload)

    if result is None:
        return {"status": "ignored"}

    wa_number = result["wa_number"]
    text = result["text"]
    message_id = result["message_id"]

    background_tasks.add_task(
        process_message,
        wa_number,
        text,
    )

    return {"status": "ok"}


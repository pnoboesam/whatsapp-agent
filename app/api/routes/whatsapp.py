import os
import hmac
import hashlib
import logging
from dotenv import load_dotenv

from app.agent import agent
from app.services.whatsapp import send_message
from app.services.db_businesses import get_business
from app.services.db_contacts import get_or_create_contact
from app.services.db_conversations import ( 
    get_or_create_conversation, 
    update_conversation_after_message,
)
from app.services.db_messages import create_message

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


async def process_message(
        wa_number: str, 
        text: str,
        business_id: str,
        contact_id: str,
        conversation_id: str,
        ):
    logger.info("Background processing started for %s", wa_number)
    
    try:    
        response = agent.chat(
            wa_number,
            text
        )

        send_response = await send_message(
            recipient=wa_number,
            message=response
        )
        
        outbound_message_id = send_response["messages"][0]["id"]

        create_message(
            business_id=business_id,
            contact_id=contact_id,
            conversation_id=conversation_id,
            external_message_id=outbound_message_id,
            content=response,
            direction="outbound",
            sender_type="ai",
            status="sent",
            raw_payload=send_response,
        )

        update_conversation_after_message(
            conversation_id=conversation_id,
            message=response,
            increment_unread=False,
        )

        logger.info(
            "Outbound message persisted, WhatsApp message sent: business=%s "
            "contact=%s conversation=%s whatsapp_message_id=%s",
            business_id,
            contact_id,
            conversation_id,
            outbound_message_id,
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
            "whatsapp_name": value["contacts"][0]["profile"]["name"],
            "phone_number_id": value["metadata"]["phone_number_id"],
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

    text = result["text"]
    wa_number = result["wa_number"]
    message_id = result["message_id"]
    phone_number_id = result["phone_number_id"]
    whatsapp_name = result["whatsapp_name"]

    business = get_business(phone_number_id)

    if business is None:
        logger.error(
            "No business found for WhatsApp phone number ID %s",
            phone_number_id,
        )
        return {"status": "ignored"}

    business_id = business["id"]
    contact = get_or_create_contact(
        business_id=business_id,
        whatsapp_phone=wa_number,
        whatsapp_name=whatsapp_name
        )

    logger.info(
        "Contact resolved: business=%s contact=%s",
        business_id,
        contact["id"],
    )

    conversation = get_or_create_conversation(
        business_id=business_id,
        contact_id=contact["id"],
        whatsapp_phone=wa_number,
    )

    logger.info(
        "Conversation resolved: business=%s contact=%s conversation=%s",
        business_id,
        contact["id"],
        conversation["id"]
    )

    message = create_message(
        business_id=business_id,
        contact_id=contact["id"],
        conversation_id=conversation["id"],
        external_message_id=message_id,
        content=text,
        direction="inbound",
        sender_type="customer",
        status="received",
        raw_payload=payload,
    )

    if message is None:
        logger.info(
            "Duplicate message ignored: %s",
            message_id
        )
        return {"status": "duplicate"}

    update_conversation_after_message(
        conversation_id=conversation["id"],
        message=text,
        increment_unread=True,
    )
    
    logger.info(
        "Message resolved: business=%s contact=%s conversation=%s whatsapp_message_id=%s",
        business_id,
        contact["id"],
        conversation["id"],
        message_id
    )

    if not conversation["ai_enabled"]:
        return {"status": "human_handling"}        
     
    background_tasks.add_task(
        process_message,
        wa_number,
        text,
        business_id,
        contact["id"],
        conversation["id"],
    )

    return {"status": "ok"}



import logging

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from app.db.client import supabase
from app.services.db_conversations import (
    get_conversation_by_id,
    mark_conversation_as_read,
    set_conversation_ai_enabled,
    update_conversation_after_message,
)
from app.services.db_messages import create_message
from app.services.whatsapp import send_message

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/conversations", tags=["conversations"])

class HumanMessageRequest(BaseModel):
    human_message: str

@router.get("")
def get_conversations():
    response = (
        supabase
        .table("conversations")
        .select("*")
        .order("last_message_at", desc=True)
        .execute()
    )

    return response.data


@router.get("/{conversation_id}/messages")
def get_conversation_messages(conversation_id: str):
    response = (
        supabase
        .table("messages")
        .select("*")
        .eq("conversation_id", conversation_id)
        .order("created_at", desc=False)
        .execute()
    )

    return response.data


@router.post("/{conversation_id}/messages")
async def send_human_message(conversation_id: str, request: HumanMessageRequest):
    conversation = get_conversation_by_id(conversation_id)
    human_message = request.human_message

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    send_response = await send_message(
        recipient=conversation["whatsapp_phone"],
        message=human_message,
    )

    outbound_message_id = send_response["messages"][0]["id"]

    created_message = create_message(
        business_id=conversation["business_id"],
        contact_id=conversation["contact_id"],
        conversation_id=conversation_id,
        external_message_id=outbound_message_id,
        content=human_message,
        direction="outbound",
        sender_type="human",
        status="sent",
        raw_payload=send_response,
    )

    update_conversation_after_message(
        conversation_id=conversation_id,
        message=human_message,
        increment_unread=False,
    )

    logger.info(
        "Outbound human message persisted, WhatsApp message sent: business=%s "
        "contact=%s conversation=%s whatsapp_message_id=%s",
        conversation["business_id"],
        conversation["contact_id"],
        conversation_id,
        outbound_message_id,
    )

    return created_message


@router.patch("/{conversation_id}/read")
def mark_as_read(conversation_id: str):

    mark_conversation_as_read(
        conversation_id=conversation_id,
    )
    
    return {"status": "ok"}


@router.patch("/{conversation_id}/ai")
def toggle_ai(conversation_id: str, ai_enabled:bool):

    set_conversation_ai_enabled(
        conversation_id=conversation_id,
        ai_enabled=ai_enabled,
    )

    return {
        "status": "ok",
        "ai_enabled": ai_enabled,
    }
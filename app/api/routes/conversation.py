from app.db.client import supabase
from fastapi import APIRouter

from app.services.db_conversations import mark_conversation_as_read, set_conversation_ai_enabled

router = APIRouter(prefix="/api/v1/conversations", tags=["conversations"])

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
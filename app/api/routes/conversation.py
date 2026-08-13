from app.db.client import supabase
from fastapi import APIRouter

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


@router.post("/{conversation_id}/read")
def mark_conversation_as_read(conversation_id: str):

    supabase.rpc(
        "mark_conversation_as_read",
        {
            "p_conversation_id": conversation_id,
        },
    ).execute()
    
    return {"status": "ok"}
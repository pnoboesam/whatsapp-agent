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
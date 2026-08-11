from app.db.client import supabase
from postgrest.exceptions import APIError

def create_message(
    business_id: str,
    conversation_id: str,
    contact_id: str,
    external_message_id: str,
    content: str,
):
    try:
        response = (
            supabase
            .table("messages")
            .insert({
                "business_id": business_id,
                "conversation_id": conversation_id,
                "contact_id": contact_id,
                "external_message_id": external_message_id,
                "direction": "inbound",
                "sender_type": "customer",
                "content": content,
                "message_type": "text",
                "status": "received",
            })
            .execute()
        )

        return response.data[0]

    except APIError as exc:
        if "duplicate key" in str(exc):
            return None

        raise


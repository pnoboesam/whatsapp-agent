from app.db.client import supabase

def get_or_create_conversation(business_id: str, contact_id: str, whatsapp_phone: str):
    response = (
        supabase
        .table("conversations")
        .select("*")
        .eq("business_id", business_id)
        .eq("contact_id", contact_id)
        .maybe_single()
        .execute()
    )

    if response:
        return response.data

    response = (
        supabase
        .table("conversations")
        .insert({
            "business_id": business_id,
            "contact_id": contact_id,
            "whatsapp_phone": whatsapp_phone,
        })
        .execute()
    )

    return response.data[0]


def update_conversation_after_message(
    conversation_id: str,
    message: str,
    increment_unread: bool,
):    
    response = (
        supabase
        .rpc(
            "update_conversation_after_message",
            {
                "p_conversation_id": conversation_id,
                "p_message": message,
                "p_increment_unread": increment_unread,
            },
        )
        .execute()
    )

    return response


def mark_conversation_as_read(conversation_id: str):

    supabase.rpc(
        "mark_conversation_as_read",
        {
            "p_conversation_id": conversation_id,
        },
    ).execute()


def set_conversation_ai_enabled(
    conversation_id: str,
    ai_enabled: bool,
):
    supabase.rpc(
        "set_conversation_ai_enabled",
        {
            "p_conversation_id": conversation_id,
            "p_ai_enabled": ai_enabled,
        },
    ).execute()
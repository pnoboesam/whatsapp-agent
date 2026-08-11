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

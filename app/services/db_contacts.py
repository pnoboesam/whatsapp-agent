from app.db.client import supabase

def get_or_create_contact(business_id: str, whatsapp_phone: str, whatsapp_name: str):
    response = (
        supabase
        .table("contacts")
        .select("*")
        .eq("business_id", business_id)
        .eq("whatsapp_phone", whatsapp_phone)
        .maybe_single()
        .execute()
    )

    if response:
        return response.data

    response = (
        supabase
        .table("contacts")
        .insert({
            "business_id": business_id,
            "whatsapp_phone": whatsapp_phone,
            "whatsapp_name": whatsapp_name,
        })
        .execute()
    )

    return response.data[0]



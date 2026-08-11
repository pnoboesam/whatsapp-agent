from app.db.client import supabase

def get_business_by_phone_number_id(phone_number_id: str):
    response = (
        supabase
        .table("businesses")
        .select("*")
        .eq("whatsapp_phone_number_id", phone_number_id)
        .maybe_single()
        .execute()
    )

    return response.data if response else None

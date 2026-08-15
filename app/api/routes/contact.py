from fastapi  import APIRouter

from app.db.client import supabase
from app.services.db_contacts import get_contact_by_id

router = APIRouter(prefix="/api/v1/contacts", tags=["contacts"])

@router.get("/contacts/{contact_id}")
async def get_contact_by_id(contact_id: str):
    response = (
        supabase
        .table("contacts")
        .select("*")
        .eq("id", contact_id)
        .maybe_single()
        .execute()
    )

    return response.data



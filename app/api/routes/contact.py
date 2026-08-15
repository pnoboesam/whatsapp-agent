from fastapi  import APIRouter

from app.db.client import supabase

router = APIRouter(prefix="/api/v1/contacts", tags=["contacts"])

@router.get("/{contact_id}")
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



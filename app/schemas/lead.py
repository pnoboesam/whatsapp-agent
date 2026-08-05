from pydantic import BaseModel

class Lead(BaseModel):
    full_name: str
    phone_number: str
    location: str
    concern: str
    wa_number: str
    source: str = 'WhatsApp'
    issue_category: str
    remarks: str

    
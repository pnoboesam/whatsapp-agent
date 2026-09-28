from pydantic import BaseModel

class HandOffRequest(BaseModel):
    reason: str
    
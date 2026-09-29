from datetime import datetime
from pydantic import BaseModel

class ChatRequest(BaseModel):
    conversation_id: str
    thread_id: str
    message: str

class ChatResponse(BaseModel):
    response:str
    thread_id: str
    timestamp: datetime
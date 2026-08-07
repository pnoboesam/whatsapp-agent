from fastapi import APIRouter
from datetime import datetime, timezone
from app.agent import agent
from app.api.schemas import ChatResponse, ChatRequest


router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
def chat(payload: ChatRequest):

    response = agent.chat(payload.thread_id, payload.message)
    
    return ChatResponse(
        response=response,
        thread_id = payload.thread_id,
        timestamp=datetime.now(timezone.utc),
        )



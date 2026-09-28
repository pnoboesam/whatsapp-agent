from langchain_core.messages import HumanMessage
from app.db.checkpointer import get_checkpointer

def sync_message_to_agent(
    conversation_id: str,
    message: str,
    sender_type: str,
):
    config = {
        "configurable": {
            "thread_id": conversation_id
        }
    }

    if sender_type == "customer":
        new_message = HumanMessage(content=message)

    elif sender_type == "human":
        new_message = HumanMessage(
            content=f"[CLINIC STAFF]: {message}"
        )

    else:
        raise ValueError(f"Unsupported sender type: {sender_type}")

    with get_checkpointer() as checkpointer:
        checkpointer.update_state(
            config,
            {"messages": [new_message]}
        )
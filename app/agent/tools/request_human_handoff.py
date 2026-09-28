from langchain.tools import tool, ToolRuntime

from app.agent.context import AgentContext
from app.schemas.handoff_request import HandOffRequest
from app.services.db_conversations import handoff_conversation

@tool(args_schema=HandOffRequest)
def request_human_handoff(reason: str, runtime: ToolRuntime[AgentContext]):
    """
    Request that a human staff member take over the conversation.
    """

    conversation_id = runtime.context.conversation_id

    handoff_conversation(
        conversation_id=conversation_id,
        reason=reason
    )

    return "Human takeover requested"
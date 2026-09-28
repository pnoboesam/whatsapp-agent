import os
from dotenv import load_dotenv
from datetime import datetime, timezone

from app.prompts.prompts import load_prompt
from app.agent.context import AgentContext
from app.db.checkpointer import get_checkpointer

from .tools.retrieval_tool import retriever_tool
from .tools.append_lead_details import append_lead_details
from .tools.request_human_handoff import request_human_handoff

from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import PromptTemplate

load_dotenv()

prompt_template = load_prompt('wa_agent_promptv2')
llm = ChatOpenRouter(
    model = 'openai/gpt-5.6-luna',
    temperature = 0,
)


def chat (
        conversation_id: str,
        wa_number: str,
        message: str
    ) -> str:

    with get_checkpointer() as checkpointer:
        # checkpointer.setup()

        prompt = PromptTemplate.from_template(prompt_template)
        SYSTEM_PROMPT = prompt.invoke({
            "wa_number": wa_number, 
            "current_time": datetime.now(timezone.utc).isoformat()
            }).text
    
        agent = create_agent(
            model=llm,
            tools=[
                retriever_tool,
                append_lead_details,
                request_human_handoff
                ],
            system_prompt=(SYSTEM_PROMPT),
            context_schema=AgentContext,
            checkpointer=checkpointer,
        )

        config = {'configurable': {'thread_id': conversation_id}}

   
        result = agent.invoke(
            {
                "messages": [{
                    "role":"user",
                    "content": message
                }]
            },
            config = config,
            context=AgentContext(
                conversation_id=str(conversation_id),
            )
        )

        return result['messages'][-1].content    
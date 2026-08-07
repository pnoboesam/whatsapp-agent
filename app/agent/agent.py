import os
from dotenv import load_dotenv
from icecream import ic as icprint
from datetime import datetime, timezone

from app.prompts.prompts import load_prompt
from .tools.retrieval_tool import retriever_tool
from .tools.append_lead_details import append_lead_details

from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import PromptTemplate
from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()

DB_URI = os.getenv('DATABASE_URL')
prompt_template = load_prompt('wa_agent_promptv1')
current_time = datetime.now(timezone.utc).isoformat()

llm = ChatOpenRouter(
    model = 'openai/gpt-5.6-luna',
    temperature = 0,
)


def chat (thread_id: str, message: str) -> str:

    with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
        # checkpointer.setup()

        prompt = PromptTemplate.from_template(prompt_template)
        SYSTEM_PROMPT = prompt.invoke({
            "wa_number": thread_id, 
            "current_time": current_time
            }).text
    
        agent = create_agent(
            model=llm,
            tools=[retriever_tool, append_lead_details],
            system_prompt=(SYSTEM_PROMPT),
            checkpointer=checkpointer,
        )

        config = {'configurable': {'thread_id': thread_id}}

   
        result = agent.invoke(
            {
                "messages": [{
                    "role":"user",
                    "content": message
                }]
            },
            config = config
        )

        return result['messages'][-1].content    



"""
## Test Agent Flow -------------------------


with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    # checkpointer.setup()
   
    agent = create_agent(
        model=llm,
        tools=[retriever_tool, append_lead_details],
        system_prompt=(SYSTEM_PROMPT),
        checkpointer=checkpointer,
    )


    config = {'configurable': {'thread_id': '233501234566'}}

    
    print("Agent Started (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        result = agent.invoke(
            {
                "messages": [{
                    "role":"user",
                    "content": user_input
                }]
            },
            config = config,
        )

        print(f"\nAgent: {result['messages'][-1].content}\n")

## Test Agent Flow -------------------------
"""

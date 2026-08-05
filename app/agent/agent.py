import os
from dotenv import load_dotenv
from icecream import ic as icprint

from app.prompts.prompts import load_prompt
from .tools.retrieval_tool import retriever_tool
from .tools.append_lead_details import append_lead_details

from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()

DB_URI = os.getenv('DATABASE_URL')
SYSTEM_PROMPT = load_prompt('wa_agent_prompt') 

llm = ChatOpenRouter(
    model = 'openai/gpt-5.6-luna',
    temperature = 0,
)

"""

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    # checkpointer.setup()
   
    agent = create_agent(
        model=llm,
        tools=[retriever_tool, append_lead_details],
        system_prompt=(SYSTEM_PROMPT),
        checkpointer=checkpointer,
    )


    config = {'configurable': {'thread_id': '233501234566'}}
    

    result = agent.invoke(
        {
            "messages": [{
                "role":"user",
                "content": "what is my name"
            }]
        },
        config = config
    )

    print(result['messages'][-1].content)

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


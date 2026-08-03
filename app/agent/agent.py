from app.prompts import load_prompt
from .retrieval_tool import retriever_tool

from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter

from icecream import ic as print


llm = ChatOpenRouter(
    model = 'openai/gpt-5.6-luna',
    temperature = 0,
)

SYSTEM_PROMPT = load_prompt('wa_agent_promptv1')
agent = create_agent(
    model=llm,
    tools=[retriever_tool],
    system_prompt=(SYSTEM_PROMPT),
)

result = agent.invoke({
    "messages": [{
        "role":"user",
        "content": "Do you accept apex"
    }]
})

print(result['messages'][-1].content)

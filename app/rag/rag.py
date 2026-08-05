from pathlib import Path

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from .retrieval import get_retriever
from app.prompts.prompts import load_prompt
from icecream import ic as print


retriever = get_retriever()

template = load_prompt('rag_promptv1')

prompt = ChatPromptTemplate.from_template(template)
llm = ChatOpenRouter(
    model = 'openai/gpt-5.6-luna',
    temperature = 0,
)


chain = (
    {"context": RunnablePassthrough() | retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


def answer_question(question: str):
    answer = chain.invoke(question)
    return answer

# print(answer_question('where are you located'))
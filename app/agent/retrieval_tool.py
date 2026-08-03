from app.rag.retrieval import get_retriever
from langchain_core.tools import create_retriever_tool


retriever = get_retriever()

retriever_tool = create_retriever_tool(
    retriever,
    name='kb_search',
    description="""
        Search the company's knowledge base to answer questions about services,
        pricing, consultation fees, insurance, operating hours,
        locations, policies, treatments, and other business information.
        Use this tool whenever the answer depends on information stored in the
        knowledge base rather than general world knowledge.
        """
)
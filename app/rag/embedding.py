from langchain_openai import OpenAIEmbeddings
from app.config import OPENROUTER_API_KEY

def get_embedding_model():
    embedding_model = OpenAIEmbeddings(
        model="openai/text-embedding-3-small",
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )

    return embedding_model
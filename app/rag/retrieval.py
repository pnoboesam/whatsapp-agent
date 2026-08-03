from icecream import ic as print
from langchain_chroma import Chroma
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

from .chunker import chunks
from .embedding import get_embedding_model
from app.config import BASE_DIR


CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

def get_retriever(k:int = 5):
    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=get_embedding_model()
    )
    vector_retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": k})


    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = k

    retriever = EnsembleRetriever(
        retrievers=[
            vector_retriever,
            bm25_retriever,
        ],
        weights=[0.7, 0.3]
    )

    return retriever
from pinecone import Pinecone

from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

from .chunker import chunks
from .embeddings import get_embedding_model
from .pinecone_retriever import PineconeRetriever

from app.config import PINECONE_API_KEY


INDEX_NAME = "elitecare"
NAMESPACE = "clinic_knowledge_docs"


def get_retriever(k: int = 5):

    # -------------------------
    # Pinecone
    # -------------------------

    pc = Pinecone(api_key=PINECONE_API_KEY)

    index = pc.Index(INDEX_NAME)

    embedding_model = get_embedding_model()

    vector_retriever = PineconeRetriever(
        index=index,
        embedding_model=embedding_model,
        namespace=NAMESPACE,
        k=k,
    )

    # -------------------------
    # BM25
    # -------------------------

    bm25_retriever = BM25Retriever.from_documents(chunks)

    bm25_retriever.k = k

    # -------------------------
    # Hybrid retrieval
    # -------------------------

    retriever = EnsembleRetriever(
        retrievers=[
            vector_retriever,
            bm25_retriever,
        ],
        weights=[0.5, 0.5],
    )

    return retriever
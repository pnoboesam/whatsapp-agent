import shutil
from pathlib import Path
from icecream import ic as print
from langchain_chroma import Chroma

from .chunker import chunks
from app.config import BASE_DIR 
from .embedding import get_embedding_model


CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

if Path(CHROMA_DIR).exists():
    print("Removing existing vector database...")
    shutil.rmtree(CHROMA_DIR)


print("Building new vector database...")
Chroma.from_documents(
    documents=chunks,
    embedding=get_embedding_model(),
    persist_directory=CHROMA_DIR
)
print(f"Indexed {len(chunks)} chunks successfully.")

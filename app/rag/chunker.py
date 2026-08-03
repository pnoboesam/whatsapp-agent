from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import BASE_DIR
from icecream import ic as print

def chunker():
    FILE_PATH = BASE_DIR / "data" / "EliteCare Knowledge Base.pdf"
    loader = PyPDFLoader(FILE_PATH)
    pages = loader.load()


    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size = 300,
        chunk_overlap = 50
    )
    chunks = text_splitter.split_documents(pages)

    return chunks

chunks = chunker()

print(f"{len(chunks)} chunks created!!")
import os

from pinecone import Pinecone, ServerlessSpec

from .chunker import chunks
from .embeddings import get_embedding_model
from app.config import PINECONE_API_KEY


embedding_model = get_embedding_model()

# --------------------------------------------------
# Pinecone configuration
INDEX_NAME = "elitecare"
NAMESPACE = "clinic_knowledge_docs"

pc = Pinecone(api_key=PINECONE_API_KEY)
# --------------------------------------------------

test_embedding = embedding_model.embed_query("test")
dimension = len(test_embedding)

if not pc.has_index(INDEX_NAME):
    print(f"Creating Pinecone index: {INDEX_NAME}")

    pc.create_index(
        name=INDEX_NAME,
        vector_type="dense",
        dimension=dimension,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1",
        ),
        deletion_protection="disabled",
    )

    print("Pinecone index created.")


# --------------------------------------------------
# Connect to the Pinecone index
index = pc.Index(INDEX_NAME)
# --------------------------------------------------


# --------------------------------------------------
# Replace existing corpus
print("Removing existing documents...")

index.delete(
    delete_all=True,
    namespace=NAMESPACE
)

print("Uploading chunks to Pinecone...")

# Generate embeddings
texts = [chunk.page_content for chunk in chunks]
vectors = embedding_model.embed_documents(texts)

# Build pinecone records
records = []

for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
    records.append({
        "id": f"chunk-{i}",
        "values": vector,
        "metadata": {
            **chunk.metadata,
            "text": chunk.page_content,
        },
    })

# Upsert
index.upsert(
    vectors=records,
    namespace=NAMESPACE,
)

print(f"Indexed {len(records)} chunks successfully.")
# --------------------------------------------------

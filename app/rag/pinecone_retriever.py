from pinecone import Pinecone
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import ConfigDict


class PineconeRetriever(BaseRetriever):

    index: object
    embedding_model: object
    namespace: str
    k: int = 5

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager=None,
    ) -> list[Document]:

        query_vector = self.embedding_model.embed_query(query)

        results = self.index.query(
            vector=query_vector,
            top_k=self.k,
            namespace=self.namespace,
            include_metadata=True,
        )

        documents = []

        for match in results["matches"]:

            metadata = match["metadata"]

            documents.append(
                Document(
                    page_content=metadata["text"],
                    metadata={
                        key: value
                        for key, value in metadata.items()
                        if key != "text"
                    }
                    | {
                        "score": match["score"]
                    },
                )
            )

        return documents
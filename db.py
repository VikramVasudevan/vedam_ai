import chromadb

from embeddings import get_embedding


class VedamDatabase:
    def __init__(self) -> None:
        self.chroma_client = chromadb.Client(
            chromadb.Settings(anonymized_telemetry=False)
        )

    def load(self, collection_name: str, ids, documents, embeddings, metadatas):
        collection = self.chroma_client.get_or_create_collection(name=collection_name)
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(self, collection_name: str, query: str, n_results=2):
        collection = self.chroma_client.get_or_create_collection(name=collection_name)
        response = collection.query(
            query_embeddings=[get_embedding(query)], n_results=n_results
        )
        return response

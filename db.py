import chromadb

from config import VedamConfig
from embeddings import get_embedding


class VedamDatabase:
    def __init__(self) -> None:
        self.chroma_client = chromadb.Client(
            chromadb.Settings(anonymized_telemetry=False)
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name=VedamConfig.collectionName
        )

    def load(self, ids, documents, embeddings, metadatas):
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(self, query: str, n_results=2):
        response = self.collection.query(
            query_embeddings=[get_embedding(query)], n_results=n_results
        )
        return response

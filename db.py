import chromadb

from config import VedamConfig
from embeddings import get_embedding
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class VedamDatabase:
    def __init__(self) -> None:
        self.chroma_client = chromadb.PersistentClient(path=VedamConfig.dbStorePath)

    def does_data_exist(self, collection_name: str) -> bool:
        collection = self.chroma_client.get_or_create_collection(name=collection_name)
        num_rows = collection.count()
        logger.info("num_rows in %s = %d", collection_name, num_rows)
        return num_rows > 0

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

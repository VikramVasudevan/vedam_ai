import logging
from file_handler import page_text_generator
from db import VedamDatabase
from embeddings import get_embedding

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class OcrLoader:
    def __init__(self) -> None:
        self.BATCH_SIZE = 100
        self.db = VedamDatabase()

    def load(self):
        logger.info("🚀 Starting OCR file ingestion into ChromaDB...")
        batch = []
        total_loaded = 0

        for item in page_text_generator():
            logger.debug(f"📄 Queued page {item['metadata']['page']} for embedding and storage")
            batch.append(item)
            if len(batch) == self.BATCH_SIZE:
                logger.info(f"📦 Loading batch of {self.BATCH_SIZE} pages to ChromaDB...")
                self.db.load(
                    documents=[d["document"] for d in batch],
                    ids=[d["id"] for d in batch],
                    metadatas=[d["metadata"] for d in batch],
                    embeddings=[get_embedding(d["document"]) for d in batch],
                )
                total_loaded += len(batch)
                logger.info(f"✅ Total loaded so far: {total_loaded}")
                batch = []

        if batch:
            logger.info(f"📦 Loading final batch of {len(batch)} pages to ChromaDB...")
            self.db.load(
                documents=[d["document"] for d in batch],
                ids=[d["id"] for d in batch],
                metadatas=[d["metadata"] for d in batch],
                embeddings=[get_embedding(d["document"]) for d in batch],
            )
            total_loaded += len(batch)
            logger.info(f"✅ Final total pages loaded: {total_loaded}")

        logger.info("🏁 OCR ingestion complete.")

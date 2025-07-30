from pypdf import PdfReader
from config import VedamConfig
import logging
from db import VedamDatabase
from embeddings import get_embedding
import chromadb

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class VedamPdfReader:
    def __init__(self) -> None:
        self.db = VedamDatabase()

    def read(self):
        reader = PdfReader(VedamConfig.shuklaYajurVedamPdfPath)
        documents = []
        embeddings = []
        metadatas = []
        ids = []
        BATCH_SIZE = 100
        MAX_PAGES = 100
        total_pages_loaded = 0
        for page_number, page in enumerate(reader.pages):
            # logger.info("reading page #%d", page_number)
            text = page.extract_text()
            if text:
                logger.info("Extrated text = %s",text)
                ids.append(str(page_number))
                documents.append(text)
                embeddings.append(get_embedding(text))
                metadatas.append(
                    {"page": page_number, "number_of_characters": len(text)}
                )

            if len(documents) == BATCH_SIZE:
                # load to chroma db
                logger.info("loading %d records to database", len(documents))
                self.db.load(
                    ids=ids,
                    documents=documents,
                    embeddings=embeddings,
                    metadatas=metadatas,
                )
                total_pages_loaded = total_pages_loaded + len(documents)
                logger.info("total pages loaded to database = %d", total_pages_loaded)

                # clear arrays
                documents = []
                embeddings = []
                ids = []
                metadatas = []

            if total_pages_loaded >= MAX_PAGES:
                logger.warning("Max Limit Reached")
                break

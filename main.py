from db import VedamDatabase
from vedam_pdf_reader import VedamPdfReader
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main():
    logger.info("Hello from vedam-ai!")
    vedamPdfReader = VedamPdfReader()
    vedamPdfReader.read()
    db = VedamDatabase()
    response = db.search(query="front-line fighters", n_results=2)
    logger.info("response = \n\n %s", response)
    logger.info("****Done")


if __name__ == "__main__":
    main()

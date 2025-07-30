from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from multiprocessing import Pool, cpu_count
from config import VedamConfig
from file_handler import write_to_file_and_create_dir
import os


class VedamPdfOCRReader:
    def __init__(self, scripture_name: str):
        self.scripture_config = [
            scripture
            for scripture in VedamConfig.scriptures
            if scripture["name"] == scripture_name
        ][0]
        self.pdf_path = self.scripture_config["pdf_path"]
        self.lang = self.scripture_config["language"]
        self.output_dir = self.scripture_config["output_dir"]
        os.makedirs(self.output_dir, exist_ok=True)

    def _ocr_single_page(self, args):
        i, image = args
        print(f"🔍 OCR page {i+1}")
        text = pytesseract.image_to_string(image, lang=self.lang)
        file_path = os.path.join(self.output_dir, f"page{i}.txt")
        write_to_file_and_create_dir(file_path, text)
        return text

    def read(self, max_pages=5, dpi=300):
        print("🖼️ Converting PDF to images...")
        images = convert_from_path(self.pdf_path, dpi=dpi, thread_count=8)
        images = images[:max_pages]

        # Prepare arguments for pool: (page_index, image)
        args = list(enumerate(images))

        print(f"⚡ Starting OCR with {cpu_count()} parallel workers")
        with Pool(processes=cpu_count()) as pool:
            all_texts = pool.map(self._ocr_single_page, args)

        return all_texts


if __name__ == "__main__":
    VedamPdfOCRReader(scripture_name="vishnu_puranam").read(max_pages=1100)

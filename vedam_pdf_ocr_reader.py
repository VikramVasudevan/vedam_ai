from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from multiprocessing import Pool, cpu_count
from config import VedamConfig
from file_handler import write_to_file_and_create_dir
import os

class VedamPdfOCRReader:
    def __init__(self):
        self.pdf_path = VedamConfig.shuklaYajurVedamSmallPdfPath
        self.lang = "san+eng"
        self.output_dir = "./output"
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
        images = convert_from_path(self.pdf_path, dpi=dpi)
        images = images[:max_pages]

        # Prepare arguments for pool: (page_index, image)
        args = list(enumerate(images))

        print(f"⚡ Starting OCR with {cpu_count()} parallel workers")
        with Pool(processes=cpu_count()) as pool:
            all_texts = pool.map(self._ocr_single_page, args)

        return all_texts

if __name__ == "__main__":
    VedamPdfOCRReader().read(max_pages=1100)

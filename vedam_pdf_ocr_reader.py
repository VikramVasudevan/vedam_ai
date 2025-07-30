from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os
from config import VedamConfig  # your config path
from file_handler import write_to_file_and_create_dir

class VedamPdfOCRReader:
    def __init__(self):
        self.pdf_path = VedamConfig.shuklaYajurVedamSmallPdfPath
        self.lang = "san+eng"  # change to 'hin' for Hindi

    def read(self, max_pages=5, dpi=300):
        print(f"🧾 Converting PDF to images ...")
        images = convert_from_path(self.pdf_path, dpi=dpi)
        all_texts = []

        for i, image in enumerate(images[:max_pages]):
            print(f"🧾 Processing page {i+1}...")
            text = pytesseract.image_to_string(image, lang=self.lang)
            write_to_file_and_create_dir(file_path_str=f"./output/page{i}.txt", content=text)
            print(f"📝 Page {i+1} Text:\n{text[:200]}...\n")
            all_texts.append(text)

        return all_texts

if __name__ == "__main__":
    VedamPdfOCRReader().read(max_pages=50)
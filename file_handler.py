import os
from pathlib import Path

from config import VedamConfig

def write_to_file_and_create_dir(file_path_str, content):
    """
    Writes content to a specified file, creating parent directories if they don't exist.

    Args:
        file_path_str (str): The path to the file, including its name.
        content (str): The string content to write to the file.
    """
    file_path = Path(file_path_str)
    
    # Create parent directories if they don't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write content to the file
    with open(file_path, 'w', encoding="utf-8") as f:
        f.write(content)

import os

def page_text_generator(output_dir=VedamConfig.outputDir):
    for filename in sorted(os.listdir(output_dir), key=lambda f: int(f.strip("page").strip(".txt"))):
        if filename.endswith(".txt"):
            page_num = int(filename.strip("page").strip(".txt"))
            file_path = os.path.join(output_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    yield {
                        "id": str(page_num),
                        "document": text,
                        "metadata": {
                            "page": page_num,
                            "file": filename,
                            "num_chars": len(text)
                        }
                    }

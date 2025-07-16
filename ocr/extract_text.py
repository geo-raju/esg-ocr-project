from pdf2image import convert_from_path
from pytesseract import image_to_string
from tqdm import tqdm
from PIL import Image
import os

def extract_text_from_file(input_path, output_path):
    all_text = ""

    ext = os.path.splitext(input_path)[1].lower()

    if ext == ".pdf":
        images = convert_from_path(input_path)
        for i, img in enumerate(tqdm(images, desc="Processing PDF pages")):
            text = image_to_string(img)
            all_text += f"\n\n--- Page {i+1} ---\n\n{text}"
    elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        try:
            img = Image.open(input_path)
            text = image_to_string(img)
            all_text = f"\n\n--- Image File ---\n\n{text}"
        except Exception as e:
            print(f"Error reading image: {e}")
            return
    else:
        print("Unsupported file type.")
        return

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(all_text)


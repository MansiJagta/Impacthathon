import os
import pytesseract
from dotenv import load_dotenv

print("Loading .env...")
load_dotenv()

tess_path = os.getenv("TESSERACT_CMD")
print(f"TESSERACT_CMD from .env: {tess_path}")

if tess_path:
    pytesseract.pytesseract.tesseract_cmd = tess_path
    print("Testing Tesseract version...")
    try:
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract version: {version}")
    except Exception as e:
        print(f"Error getting Tesseract version: {e}")
else:
    print("TESSERACT_CMD not found in environment.")

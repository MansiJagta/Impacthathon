import os
import pytesseract
import fitz  # PyMuPDF
import cv2
import numpy as np
from dotenv import load_dotenv

load_dotenv()

pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh

def extract_text_from_image(path):
    img = cv2.imread(path)
    processed = preprocess_image(img)
    return pytesseract.image_to_string(processed, config="--oem 3 --psm 4")

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        pix = page.get_pixmap()
        img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        processed = preprocess_image(img_array)
        text += pytesseract.image_to_string(processed, config="--oem 3 --psm 4")
    doc.close()
    return text
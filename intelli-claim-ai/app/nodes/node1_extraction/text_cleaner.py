import os
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
from dotenv import load_dotenv

load_dotenv()

pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")
POPPLER_PATH = os.getenv("POPPLER_PATH")


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
    pages = convert_from_path(path, poppler_path=POPPLER_PATH)
    text = ""

    for page in pages:
        img = np.array(page)
        processed = preprocess_image(img)
        text += pytesseract.image_to_string(processed, config="--oem 3 --psm 4")

    return text
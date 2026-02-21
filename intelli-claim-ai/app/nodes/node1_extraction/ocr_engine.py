import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

tesseract_cmd = os.getenv("TESSERACT_CMD")
if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd


def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    return gray


def extract_text_from_image(image_path):
    processed = preprocess_image(image_path)
    if processed is None:
        return ""
    text = pytesseract.image_to_string(processed)
    return text
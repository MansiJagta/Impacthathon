import os
from pathlib import Path

from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError
from pypdf import PdfReader


def pdf_to_images(pdf_path, output_folder="temp_images"):
    os.makedirs(output_folder, exist_ok=True)
    poppler_path = os.getenv("POPPLER_PATH")
    if poppler_path:
        poppler_path = str(Path(poppler_path))

    try:
        pages = convert_from_path(pdf_path, poppler_path=poppler_path)
    except PDFInfoNotInstalledError as exc:
        raise RuntimeError("Poppler is not configured for pdf2image conversion") from exc

    image_paths = []
    for i, page in enumerate(pages):
        path = f"{output_folder}/page_{i}.jpg"
        page.save(path, "JPEG")
        image_paths.append(path)

    return image_paths


def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        texts = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                texts.append(page_text)
        return "\n".join(texts).strip()
    except Exception:
        return ""
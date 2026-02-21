import os
from app.utils.file_loader import extract_text_from_pdf, pdf_to_images
from .ocr_engine import extract_text_from_image
from .document_classifier import classify_document
from .field_extractors import (
    extract_policy_fields,
    extract_bill_fields,
    extract_id_fields,
    extract_report_fields
)


def extract_from_file(file_path):
    texts = []

    if file_path.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_path)
        if extracted_text:
            return extracted_text

        try:
            images = pdf_to_images(file_path)
            for img in images:
                texts.append(extract_text_from_image(img))
        except Exception:
            return ""
    else:
        texts.append(extract_text_from_image(file_path))

    return "\n".join(texts)


def extract_documents(file_paths):

    results = []

    for file_path in file_paths:

        text = extract_from_file(file_path)
        doc_type = classify_document(text)

        if doc_type == "policy":
            fields = extract_policy_fields(text)

        elif doc_type == "bill":
            fields = extract_bill_fields(text)

        elif doc_type == "id_proof":
            fields = extract_id_fields(text)

        elif doc_type == "report":
            fields = extract_report_fields(text)

        else:
            fields = {}

        results.append({
            "file": os.path.basename(file_path),
            "document_type": doc_type,
            "extracted_text": text,
            "structured_fields": fields,
            "confidence": 0.85
        })

    return {
        "total_documents": len(results),
        "documents": results
    }
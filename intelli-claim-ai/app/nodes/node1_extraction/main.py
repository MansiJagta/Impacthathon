import sys
import argparse
def cli_mode():
    parser = argparse.ArgumentParser(description="Node1 Document Extraction CLI")
    parser.add_argument('--files', nargs='+', required=True, help='List of file paths to extract')
    parser.add_argument('--types', nargs='+', required=True, help='List of document types (policy, bill, id_proof, report)')
    args = parser.parse_args()

    if len(args.files) != len(args.types):
        print("Error: Number of files and types must match.")
        sys.exit(1)

    claim_id = f"CL-{uuid.uuid4().hex[:6].upper()}"
    documents_extracted = {}
    for file_path, doc_type in zip(args.files, args.types):
        extracted = process_document(file_path, classify_document(doc_type))
        documents_extracted[doc_type] = extracted

    result = {
        "claim_id": claim_id,
        "documents_extracted": documents_extracted,
        "extraction_confidence": 0.95,
    }
    import json
    print(json.dumps(result, indent=2))
if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_mode()
from fastapi import FastAPI, UploadFile, File, Form
from typing import List
import os
import uuid

from .ocr_engine import extract_text_from_pdf, extract_text_from_image
from .extractor import (
    extract_policy_fields,
    extract_bill_fields,
    extract_id_fields,
    extract_report_fields,
)

app = FastAPI(title="Node1 OCR API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def classify_document(doc_type: str):
    if doc_type.lower() == "policy":
        return "policy"
    if doc_type.lower() == "bill":
        return "bill"
    if doc_type.lower() == "id_proof":
        return "id_proof"
    if doc_type.lower() == "report":
        return "report"
    return "unknown"


def process_document(file_path: str, doc_type: str):
    if file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_image(file_path)

    if doc_type == "policy":
        return extract_policy_fields(text)

    elif doc_type == "bill":
        return extract_bill_fields(text)

    elif doc_type == "id_proof":
        return extract_id_fields(text)

    elif doc_type == "report":
        return extract_report_fields(text)

    return {}


@app.post("/upload")
async def upload_documents(
    files: List[UploadFile] = File(...), doc_types: List[str] = Form(...)
):
    claim_id = f"CL-{uuid.uuid4().hex[:6].upper()}"
    documents_extracted = {}

    for file, doc_type in zip(files, doc_types):
        unique_name = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        extracted = process_document(file_path, classify_document(doc_type))
        documents_extracted[doc_type] = extracted

    return {
        "claim_id": claim_id,
        "documents_extracted": documents_extracted,
        "extraction_confidence": 0.95,
    }
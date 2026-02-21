import os
import re
from app.nodes.node1_extraction.ocr_engine import extract_text_from_image, extract_text_from_pdf


def extract_money(text):
    return re.findall(r"(?:rs\.?|re\.?)\s?\d[\d,]*|\b\d{5,}\b", text, re.I)


def classify_document(text: str) -> str:
    text = text.lower()

    if "policy" in text:
        return "policy"
    if "invoice" in text or "total" in text:
        return "bill"
    if "aadhaar" in text or "id" in text:
        return "id_proof"
    if "incident" in text or "report" in text:
        return "report"

    return "unknown"


def extract_policy_fields(text):
    policy_numbers = re.findall(
        r"policy\s*(?:no|number)?\s*[:\-]?\s*(\d[\dA-Z\/\-]*\/[\dA-Z\/\-]+)", text, re.I
    )

    premium_amounts = extract_money(text)

    return {
        "policy_number": policy_numbers,
        "premium_amounts": premium_amounts,
        "holder_name": [],
        "address": [],
    }


def extract_bill_fields(text):
    return {
        "invoice_number": re.findall(
            r"invoice\s*(?:no)?[:\-]?\s*([A-Z0-9\-]+)", text, re.I
        ),
        "amount": extract_money(text),
        "date": re.findall(r"\d{2}[-/]\w+[-/]\d{4}", text),
    }


def extract_id_fields(text):
    return {
        "name": re.findall(r"name[:\-]?\s*([A-Z ]+)", text, re.I),
        "id_number": re.findall(r"\d{12}", text),
    }


def extract_report_fields(text):
    return {
        "incident_date": re.findall(r"\d{2}[-/]\w+[-/]\d{4}", text),
        "description": text[:200],
    }


def process_documents(claim_id: str, file_paths: list[str]):
    documents = []

    for path in file_paths:
        if path.lower().endswith(".pdf"):
            text = extract_text_from_pdf(path)
        else:
            text = extract_text_from_image(path)

        doc_type = classify_document(text)
        fields = {}

        if doc_type == "policy":
            fields = extract_policy_fields(text)
        elif doc_type == "bill":
            fields = extract_bill_fields(text)
        elif doc_type == "id_proof":
            fields = extract_id_fields(text)
        elif doc_type == "report":
            fields = extract_report_fields(text)

        documents.append({
            "file": path,
            "document_type": doc_type,
            "structured_fields": fields,
            "extracted_text": text
        })

    return {
        "claim_id": claim_id,
        "documents": documents,
        "extraction_confidence": 0.95,
    }


def extract_documents(file_paths: list[str], claim_id: str = "AUTO"):
    """Alias for LangGraph compatibility"""
    return process_documents(claim_id, file_paths)

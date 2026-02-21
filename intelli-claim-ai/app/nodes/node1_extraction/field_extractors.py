import re


def extract_policy_fields(text):
    return {
        "policy_number": re.findall(r"POLICY\s*NO[:\-]?\s*(\w+)", text, re.I),
        "holder_name": re.findall(r"NAME[:\-]?\s*([A-Z ]+)", text, re.I),
        "address": re.findall(r"ADDRESS[:\-]?\s*(.+)", text, re.I),
    }


def extract_bill_fields(text):
    return {
        "invoice_number": re.findall(r"INVOICE\s*NO[:\-]?\s*(\w+)", text, re.I),
        "amount": re.findall(r"TOTAL\s*AMOUNT[:\-]?\s*(\d+)", text, re.I),
        "date": re.findall(r"DATE[:\-]?\s*(\d{2}/\d{2}/\d{4})", text, re.I),
    }


def extract_id_fields(text):
    return {
        "name": re.findall(r"NAME[:\-]?\s*([A-Z ]+)", text, re.I),
        "id_number": re.findall(r"\d{12}", text),
    }


def extract_report_fields(text):
    return {
        "incident_date": re.findall(r"DATE[:\-]?\s*(\d{2}/\d{2}/\d{4})", text, re.I),
        "description": text[:200]
    }
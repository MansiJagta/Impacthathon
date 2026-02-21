def classify_document(text: str) -> str:
    text = text.lower()

    if "policy number" in text or "coverage" in text:
        return "policy"

    if "invoice" in text or "total amount" in text:
        return "bill"

    if "aadhaar" in text or "id number" in text:
        return "id_proof"

    if "incident" in text or "report" in text:
        return "report"

    return "other"
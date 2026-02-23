import hashlib


def compute_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def detect_duplicates(documents):
    hashes = {}
    duplicates = []

    for doc in documents:
        text = doc.get("extracted_text", "")
        h = compute_hash(text)

        if h in hashes:
            duplicates.append(doc["file"])
        else:
            hashes[h] = doc["file"]

    return duplicates
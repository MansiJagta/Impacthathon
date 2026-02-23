from pathlib import Path

from app.nodes.node1_extraction.extractor import process_documents


def pick_non_empty_file(patterns):
    sample_dir = Path("sample_docs")
    for pattern in patterns:
        for candidate in sorted(sample_dir.glob(pattern)):
            if candidate.is_file() and candidate.stat().st_size > 0:
                return str(candidate)
    return None


pdf_file = pick_non_empty_file(["*.pdf"])
image_file = pick_non_empty_file(["*.jpg", "*.jpeg", "*.png"])

files = [path for path in [pdf_file, image_file] if path]

if not files:
    raise FileNotFoundError(
        "No non-empty files found in sample_docs. Add at least one PDF or image."
    )

print("Using files:", files)
result = process_documents("dummy_claim_id", files)

print("\n===== EXTRACTION RESULT =====\n")
print(result)
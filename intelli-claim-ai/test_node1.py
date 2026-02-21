from app.nodes.node1_extraction.extractor import extract_documents

# ⭐ Put real files here
files = [
    "sample_docs/policy.pdf",
    "sample_docs/bill.jpg"
]

result = extract_documents(files)

print("\n===== EXTRACTION RESULT =====\n")
print(result)
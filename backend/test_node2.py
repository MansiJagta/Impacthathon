from app.nodes.node1_extraction.extractor import extract_documents
from app.nodes.node2_cross_validation.validator import cross_validate

files = [
    "sample_docs/policy_motor_sample.pdf",
    "sample_docs/bill_repair_sample.pdf",
    "sample_docs/id_proof_sample.pdf",
    "sample_docs/incident_report_sample.pdf"
]

node1_output = extract_documents(files)
node2_output = cross_validate(node1_output)

print("\n===== NODE 2 RESULT =====\n")
print(node2_output)
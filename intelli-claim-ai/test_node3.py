from app.nodes.node1_extraction.extractor import extract_documents
from app.nodes.node3_policy_coverage.policy_agent import verify_policy_coverage

files = [
    "sample_docs/policy_motor_sample.pdf",
    "sample_docs/bill_repair_sample.pdf",
    "sample_docs/incident_report_sample.pdf"
]

node1_output = extract_documents(files)
result = verify_policy_coverage(node1_output)

print("\n===== NODE 3 RESULT =====\n")
print(result)
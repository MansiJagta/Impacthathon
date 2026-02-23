from pathlib import Path

from app.nodes.node1_extraction.extractor import extract_documents
from app.nodes.node3_policy_coverage.policy_fetcher import fetch_policy
from app.nodes.node4_fraud_detection.fraud_agent import fraud_detection

project_root = Path(__file__).resolve().parent
sample_docs_dir = project_root / "sample_docs"

candidate_files = [
    sample_docs_dir / "policy_motor_sample.pdf",
    sample_docs_dir / "bill_repair_sample.pdf",
    sample_docs_dir / "incident_report_sample.pdf",
    sample_docs_dir / "policy.pdf",
    sample_docs_dir / "bill.jpg",
]

files = [str(path) for path in candidate_files if path.exists()]

if not files:
    raise FileNotFoundError("No sample documents found in sample_docs directory")

node1_output = extract_documents(files)
policy = fetch_policy("MOT-12345678")

result = fraud_detection(node1_output, policy)
print(result)
import uuid

# -----------------------------
# NODE IMPORTS
# -----------------------------
from app.nodes.node1_extraction.extractor import extract_documents
from app.nodes.node2_cross_validation.validator import cross_validate
from app.nodes.node3_policy_coverage.policy_agent import verify_policy_coverage
from app.nodes.node3_policy_coverage.policy_fetcher import fetch_policy
from app.nodes.node4_fraud_detection.fraud_agent import fraud_detection
from app.nodes.node5_predictive.predictive_agent import predictive_analysis
from app.nodes.node6_explanation.explanation_agent import generate_explanation
from app.nodes.node7_decision.decision_agent import make_claim_decision
from app.nodes.node8_subrogation.subrogation_agent import analyze_subrogation

# HITL service
from app.services.hitl_service import store_high_risk_claim


# ======================================================
# CONFIGURATION
# ======================================================
PREDICTED_COST_THRESHOLD = 50000  # Node 5 threshold


# ======================================================
# STEP 1 — LOAD CLAIM DOCUMENTS
# ======================================================
files = [
    "sample_docs/policy_motor_sample.pdf",
    "sample_docs/bill_repair_sample.pdf",
    "sample_docs/incident_report_sample.pdf"
]

print("\n========== CLAIM PROCESSING STARTED ==========\n")


# ======================================================
# STEP 2 — NODE 1 EXTRACTION
# ======================================================
node1_output = extract_documents(files)
print("NODE 1 COMPLETE — DOCUMENT EXTRACTION")


# ======================================================
# STEP 3 — NODE 2 VALIDATION
# ======================================================
node2_output = cross_validate(node1_output)
print("NODE 2 COMPLETE — CROSS DOCUMENT VALIDATION")


# ======================================================
# STEP 4 — NODE 3 POLICY COVERAGE
# ======================================================
node3_output = verify_policy_coverage(node1_output)
print("NODE 3 COMPLETE — POLICY COVERAGE")


# Fetch policy for fraud analysis
policy = fetch_policy("MOT-12345678")


# ======================================================
# STEP 5 — NODE 4 FRAUD DETECTION
# ======================================================
node4_output = fraud_detection(node1_output, policy)
print("NODE 4 COMPLETE — FRAUD ANALYSIS")


# ======================================================
# STEP 6 — NODE 5 PREDICTIVE ANALYSIS
# ======================================================
node5_output = predictive_analysis(
    node1_output,
    node2_output,
    node3_output,
    node4_output
)
print("NODE 5 COMPLETE — PREDICTIVE FORECASTING")


# ======================================================
# STEP 7 — NODE 6 EXPLANATION (XAI)
# ======================================================
node6_output = generate_explanation(
    node2_output,
    node3_output,
    node4_output
)
print("NODE 6 COMPLETE — EXPLAINABLE AI GENERATED")


# ======================================================
# STEP 8 — NODE 7 FINAL DECISION
# ======================================================
node7_output = make_claim_decision(node3_output, node4_output)
print("NODE 7 COMPLETE — CLAIM DECISION")


# ======================================================
# STEP 9 — NODE 8 SUBROGATION ANALYSIS
# ======================================================
node8_output = analyze_subrogation(node1_output)
print("NODE 8 COMPLETE — RECOVERY ANALYSIS")


# ======================================================
# STEP 10 — HITL STORAGE LOGIC
# ======================================================
claim_id = str(uuid.uuid4())

risk_level = node4_output.get("risk_level", "LOW")
predicted_cost = node5_output.get("predicted_final_cost", 0)
human_review = node7_output.get("human_review_required", False)

store_flag = False

# condition 1 — high risk
if risk_level in ["HIGH", "CRITICAL"]:
    store_flag = True

# condition 2 — medium risk but expensive claim
elif risk_level == "MEDIUM" and predicted_cost >= PREDICTED_COST_THRESHOLD:
    store_flag = True

# condition 3 — decision engine requests human review
elif human_review:
    store_flag = True


if store_flag:
    store_high_risk_claim(
        claim_id,
        node1_output,
        node2_output,
        node3_output,
        node4_output,
        node6_output  # AI explanation stored
    )
    print("\nHITL ESCALATION: CLAIM STORED IN hitl_db")
else:
    print("\nAUTOMATED PROCESSING: NO HUMAN REVIEW NEEDED")


# ======================================================
# FINAL SYSTEM OUTPUT
# ======================================================
print("\n========== FINAL CLAIM SUMMARY ==========\n")

print("FRAUD RESULT:")
print(node4_output)

print("\nPREDICTIVE RESULT:")
print(node5_output)

print("\nFINAL DECISION:")
print(node7_output)

print("\nSUBROGATION:")
print(node8_output)

print("\nAI EXPLANATION:\n")
print(node6_output["explanation_text"])

print("\n========== PROCESSING COMPLETE ==========")
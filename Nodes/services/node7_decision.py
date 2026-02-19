DECISION_MODEL_VERSION = "decision_v1.0"
FRAUD_ESCALATION_THRESHOLD = 0.8
APPROVE_THRESHOLD = 0.3
REVIEW_THRESHOLD = 0.6


def make_decision(explanation_output):

    risk_score = explanation_output["risk_score"]
    fraud_score = explanation_output["audit_trail"]["fraud_score"]

    # -------------------------
    # 1️⃣ FRAUD OVERRIDE FIRST
    # -------------------------
    if fraud_score >= FRAUD_ESCALATION_THRESHOLD:
        return {
            "final_status": "ESCALATED_FRAUD_REVIEW",
            "risk_score": risk_score,
            "threshold_applied": FRAUD_ESCALATION_THRESHOLD,
            "decision_reason": "Fraud score exceeded escalation threshold.",
            "confidence": round(1 - risk_score, 2),
            "requires_human_review": True,
            "next_actions": ["assign_to_senior_investigator"],
            "decision_model": DECISION_MODEL_VERSION,
        }

    # -------------------------
    # 2️⃣ NORMAL RISK LOGIC
    # -------------------------
    if risk_score < APPROVE_THRESHOLD:
        final_status = "APPROVED"
        requires_review = False
        next_actions = ["disburse_payment", "close_claim"]

    elif risk_score < REVIEW_THRESHOLD:
        final_status = "FLAGGED_FOR_REVIEW"
        requires_review = True
        next_actions = ["assign_to_adjuster"]

    else:
        final_status = "REJECTED"
        requires_review = True
        next_actions = ["investigate_claim"]

    return {
        "final_status": final_status,
        "risk_score": risk_score,
        "threshold_applied": APPROVE_THRESHOLD,
        "decision_reason": "Risk score evaluated against thresholds.",
        "confidence": round(1 - risk_score, 2),
        "requires_human_review": requires_review,
        "next_actions": next_actions,
        "decision_model": DECISION_MODEL_VERSION,
    }

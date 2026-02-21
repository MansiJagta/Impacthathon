def make_claim_decision(node3_output, node4_output):

    fraud_score = node4_output.get("fraud_score", 0)
    risk_level = node4_output.get("risk_level", "LOW")
    is_covered = node3_output.get("is_covered", False)

    if not is_covered:
        return {
            "final_status": "REJECTED",
            "reason": "Policy does not cover claim",
            "human_review_required": False
        }

    if fraud_score >= 0.8:
        return {
            "final_status": "ESCALATED_FRAUD_REVIEW",
            "reason": "Very high fraud risk",
            "human_review_required": True
        }

    if fraud_score < 0.3:
        return {
            "final_status": "APPROVED",
            "reason": "Low fraud risk and covered",
            "human_review_required": False
        }

    if fraud_score < 0.6:
        return {
            "final_status": "FLAGGED_FOR_REVIEW",
            "reason": "Moderate fraud risk",
            "human_review_required": True
        }

    return {
        "final_status": "REJECTED",
        "reason": "High risk claim",
        "human_review_required": True
    }
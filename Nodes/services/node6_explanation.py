from datetime import datetime


EXPLANATION_MODEL_VERSION = "explanation_v2.3"


def generate_explanation(claim_input, predictive_output):
    """
    Combines reasoning from all previous nodes
    and prepares structured explanation + audit trail.
    """

    policy = claim_input.policy_analysis
    fraud = claim_input.fraud_analysis
    predictive = predictive_output["predictive_analysis"]

    detailed_reasoning = []

    # Cross Validation Node (Example)
    detailed_reasoning.append(
        {
            "node": "Cross Validation",
            "finding": "Documents processed successfully",
            "confidence": round(claim_input.consistency_score, 2),
        }
    )

    # Policy Coverage Node
    coverage_finding = (
        f"Claim covered under policy type {policy.policy_type}"
        if policy.is_covered
        else "Claim not covered under policy terms"
    )

    detailed_reasoning.append(
        {
            "node": "Policy Coverage",
            "finding": coverage_finding,
            "confidence": round(policy.confidence, 2),
        }
    )

    # Fraud Detection Node
    fraud_finding = (
        "High fraud indicators detected"
        if fraud.fraud_score > 0.7
        else "No significant fraud indicators"
    )

    detailed_reasoning.append(
        {
            "node": "Fraud Detection",
            "finding": fraud_finding,
            "confidence": round(fraud.confidence, 2),
        }
    )

    # Predictive Node
    detailed_reasoning.append(
        {
            "node": "Predictive Analysis",
            "finding": f"Predicted cost ₹{predictive['predicted_cost']} "
            f"with severity {predictive['damage_severity']}",
            "confidence": round(predictive["prediction_confidence"], 2),
        }
    )

    # Risk score (simple weighted logic example)
    risk_score = round(
        (fraud.fraud_score * 0.5)
        + ((1 - policy.coverage_score) * 0.3)
        + ((1 - claim_input.consistency_score) * 0.2),
        2,
    )

    explanation = {
        "summary": f"Claim {claim_input.claim_id} processed with risk score {risk_score}.",
        "detailed_reasoning": detailed_reasoning,
        "final_verdict": f"Risk score calculated at {risk_score}",
    }

    audit_trail = {
        "claim_id": claim_input.claim_id,
        "timestamp": datetime.utcnow().isoformat(),
        "policy_number": policy.policy_number,
        "fraud_score": fraud.fraud_score,
        "risk_score": risk_score,
        "predictive_output": predictive,
    }

    return {
        "explanation": explanation,
        "audit_trail": audit_trail,
        "explanation_model": EXPLANATION_MODEL_VERSION,
        "risk_score": risk_score,
    }

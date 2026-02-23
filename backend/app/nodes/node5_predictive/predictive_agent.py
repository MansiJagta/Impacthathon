import random


# --------------------------------
# Helper: extract claim amount
# --------------------------------
def extract_claim_amount(node1_output):
    for doc in node1_output["documents"]:
        if doc["document_type"] == "bill":
            fields = doc.get("structured_fields", {})
            raw_amt = fields.get("amount")
            
            # Handle list vs scalar from different extraction sources
            if isinstance(raw_amt, list):
                raw_amt = raw_amt[0] if raw_amt else 0
            
            if not raw_amt:
                continue

            try:
                if isinstance(raw_amt, str):
                    # Remove non-numeric chars except decimal
                    clean_amt = "".join(c for c in raw_amt if c.isdigit() or c == ".")
                    return float(clean_amt) if clean_amt else 0.0
                return float(raw_amt)
            except (TypeError, ValueError):
                return 0.0
    return 0.0


# --------------------------------
# Damage severity classification
# --------------------------------
def estimate_severity(amount):

    if amount < 20000:
        return "LOW"
    elif amount < 80000:
        return "MEDIUM"
    else:
        return "HIGH"


# --------------------------------
# Settlement time estimation
# --------------------------------
def estimate_settlement_days(severity, fraud_score):

    base_days = {
        "LOW": 7,
        "MEDIUM": 21,
        "HIGH": 45
    }[severity]

    # fraud increases investigation time
    extra = int(fraud_score * 30)

    return base_days + extra


# --------------------------------
# Reserve recommendation
# --------------------------------
def estimate_reserve(amount, fraud_score):

    # insurers keep extra buffer for risky claims
    buffer = amount * (0.1 + fraud_score * 0.2)
    return round(amount + buffer, 2)


# --------------------------------
# Final cost estimation
# --------------------------------
def predict_final_cost(amount, fraud_score, consistency_score):

    # risk inflation
    inflation = 1 + (fraud_score * 0.3)

    # inconsistency uncertainty
    uncertainty = 1 + (1 - consistency_score) * 0.2

    predicted = amount * inflation * uncertainty
    return round(predicted, 2)


# --------------------------------
# Confidence score
# --------------------------------
def prediction_confidence(consistency_score, fraud_score):

    confidence = 0.7 * consistency_score + 0.3 * (1 - fraud_score)
    return round(confidence, 2)


# --------------------------------
# MAIN NODE 5 FUNCTION
# --------------------------------
def predictive_analysis(
    node1_output,
    node2_output,
    node3_output,
    node4_output
):

    claim_amount = extract_claim_amount(node1_output)
    fraud_score = node4_output.get("fraud_score", 0)
    consistency_score = node2_output.get("consistency_score", 1)

    severity = estimate_severity(claim_amount)

    predicted_cost = predict_final_cost(
        claim_amount,
        fraud_score,
        consistency_score
    )

    reserve = estimate_reserve(claim_amount, fraud_score)

    settlement_days = estimate_settlement_days(
        severity,
        fraud_score
    )

    confidence = prediction_confidence(
        consistency_score,
        fraud_score
    )

    return {
        "predicted_final_cost": predicted_cost,
        "damage_severity": severity,
        "recommended_reserve": reserve,
        "estimated_settlement_days": settlement_days,
        "prediction_confidence": confidence
    }
import random


# --------------------------------
# Helper: extract claim amount
# --------------------------------
def extract_claim_amount(node1_output):
    for doc in node1_output["documents"]:
        if doc["document_type"] == "bill":
            amt = doc["structured_fields"].get("amount", [0])[0]
            try:
                return float(amt)
            except:
                return 0
    return 0


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
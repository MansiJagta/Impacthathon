from fastapi import APIRouter
from datetime import datetime
import numpy as np

from models.schemas import ClaimInput
from services.similarity import find_similar_claims
from services.node6_explanation import generate_explanation
from services.node7_decision import make_decision
from database import reviewer_queue, live_claims

router = APIRouter()

_model_ref = None


def set_model_reference(ref_func):
    global _model_ref
    _model_ref = ref_func


@router.post("/predict")
def predict(input_data: ClaimInput):

    model = _model_ref()

    existing = live_claims.find_one({"claim_id": input_data.claim_id})
    if existing:
        return {"error": "Claim already exists"}

    policy = input_data.policy_analysis
    fraud = input_data.fraud_analysis
    extracted = input_data.extracted_data

    features = [
        float(policy.policy_limit),
        float(policy.deductible),
        float(fraud.fraud_score),
    ]

    predicted_cost = float(model.predict([features])[0])

    similar_claims = find_similar_claims(
        extracted.damage_description, policy.policy_type, top_k=3
    )

    if similar_claims:
        avg_cost = float(np.mean([c["final_cost"] for c in similar_claims]))
        settlement_days = int(np.mean([c["settlement_days"] for c in similar_claims]))
        variance = (
            ((predicted_cost - avg_cost) / avg_cost) * 100 if avg_cost != 0 else 0
        )
    else:
        avg_cost = 0.0
        settlement_days = 15
        variance = 0.0

    severity = (
        "HIGH"
        if predicted_cost > 100000
        else "MEDIUM"
        if predicted_cost > 40000
        else "LOW"
    )

    prediction_confidence = round((1 - abs(variance) / 100) * policy.coverage_score, 2)
    prediction_confidence = max(0.0, min(1.0, prediction_confidence))

    predictive_analysis = {
        "predicted_cost": int(predicted_cost),
        "predicted_cost_range": {
            "min": int(predicted_cost * 0.95),
            "max": int(predicted_cost * 1.05),
        },
        "damage_severity": severity,
        "recommended_reserve": int(predicted_cost * 1.05),
        "predicted_timeline_days": settlement_days,
        "prediction_confidence": prediction_confidence,
        "similar_claims_reference": similar_claims,
        "cost_anomaly": {
            "is_anomaly": abs(variance) > 20,
            "expected_cost": int(avg_cost),
            "variance_percent": round(variance, 2),
        },
    }

    explanation_output = generate_explanation(
        input_data, {"predictive_analysis": predictive_analysis}
    )

    decision_output = make_decision(explanation_output)

    if decision_output["requires_human_review"]:
        fraud_score = explanation_output["audit_trail"]["fraud_score"]

        reviewer_queue.insert_one(
            {
                "claim_id": input_data.claim_id,
                "priority": "HIGH" if fraud_score >= 0.8 else "MEDIUM",
                "status": "PENDING",
                "assigned_reviewer": None,
                "created_at": datetime.utcnow(),
            }
        )

    claim_record = {
        "claim_id": input_data.claim_id,
        "claim_input": input_data.model_dump(),
        "documents": [doc.model_dump() for doc in input_data.documents],
        "predictive_analysis": predictive_analysis,
        "explanation": explanation_output["explanation"],
        "audit_trail": explanation_output["audit_trail"],
        "decision": decision_output,
        "workflow_status": decision_output["final_status"],
        "human_review": {
            "required": decision_output["requires_human_review"],
            "assigned_to": None,
            "review_notes": [],
            "additional_info_requested": False,
            "requested_fields": [],
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    live_claims.insert_one(claim_record)

    return {
        "predictive_analysis": predictive_analysis,
        "explanation": explanation_output["explanation"],
        "audit_trail": explanation_output["audit_trail"],
        "decision": decision_output,
    }


@router.get("/claim/{claim_id}")
def get_claim(claim_id: str):

    claim = live_claims.find_one({"claim_id": claim_id}, {"_id": 0})

    if not claim:
        return {"error": "Claim not found"}

    return claim

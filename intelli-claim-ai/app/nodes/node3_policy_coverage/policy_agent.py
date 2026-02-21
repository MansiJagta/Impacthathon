from datetime import datetime
from .policy_fetcher import fetch_policy
from .coverage_checker import is_policy_active, calculate_covered_amount
from .exclusions_engine import check_exclusions


# --------------------------------
# extract claim context from node1 output
# --------------------------------

def extract_claim_context(node1_output):

    policy_number = None
    claim_amount = 0
    incident_date = None
    description = ""

    for doc in node1_output["documents"]:

        fields = doc.get("structured_fields", {})
        dtype = doc.get("document_type")

        if dtype == "policy":
            policy_number = fields.get("policy_number", [None])[0]

        if dtype == "bill":
            amt = fields.get("amount", [0])[0]
            claim_amount = float(amt)

        if dtype == "report":
            incident_date = fields.get("incident_date", [None])[0]
            description = fields.get("description", "")

    if incident_date:
        incident_date = datetime.strptime(incident_date, "%d/%m/%Y")

    return {
        "policy_number": policy_number,
        "claim_amount": claim_amount,
        "incident_date": incident_date,
        "description": description,
        "incident_type": "accident"
    }


# --------------------------------
# NODE 3 MAIN FUNCTION
# --------------------------------

def verify_policy_coverage(node1_output):

    context = extract_claim_context(node1_output)

    policy = fetch_policy(context["policy_number"])

    if not policy:
        return {
            "is_covered": False,
            "reason": "policy not found"
        }

    # policy active?
    active = is_policy_active(policy, context["incident_date"])

    if not active:
        return {
            "is_covered": False,
            "reason": "policy not active on incident date"
        }

    # exclusions
    exclusions_triggered = check_exclusions(policy, context)

    if exclusions_triggered:
        return {
            "is_covered": False,
            "reason": "policy exclusion triggered",
            "exclusions": exclusions_triggered
        }

    # payout
    covered_amount, deductible = calculate_covered_amount(
        policy,
        context["claim_amount"]
    )

    return {
        "is_covered": True,
        "covered_amount": covered_amount,
        "deductible": deductible,
        "policy_limit": policy["sumInsured"],
        "exclusions_triggered": [],
        "confidence": 0.95
    }
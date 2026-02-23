from datetime import datetime


def parse_date(d):
    if not d:
        return None
    return datetime.strptime(d, "%d/%m/%Y")


def is_policy_active(policy, incident_date):

    start = policy["effectiveDate"]
    end = policy["expiryDate"]

    start = start.replace(tzinfo=None)
    end = end.replace(tzinfo=None)

    return start <= incident_date <= end


def calculate_covered_amount(policy, claim_amount):

    coverage = policy["coverageDetails"]
    deductible = coverage.get("deductible", 0)

    limits = coverage.get("limits", {})
    own_damage_limit = limits.get("ownDamage", policy.get("sumInsured", 0))

    payable = claim_amount - deductible

    if payable < 0:
        payable = 0

    if isinstance(own_damage_limit, (int, float)):
        payable = min(payable, own_damage_limit)

    return payable, deductible
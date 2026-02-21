from datetime import datetime
from .fraud_rules import round_amount_check
from .benford import benford_score
from .watchlist_scan import watchlist_match
from .anomaly_models import anomaly_score


def _parse_date(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.replace(tzinfo=None)
    if isinstance(value, str):
        for date_format in ("%d/%m/%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(value, date_format)
            except ValueError:
                continue
    return None


def _first_field_value(fields, key, default):
    value = fields.get(key, default)
    if isinstance(value, list):
        return value[0] if value else default
    return value


def extract_context(node1_output, policy):

    claim_amount = 0
    claimant_name = ""
    incident_date = None

    for doc in node1_output.get("documents", []):
        fields = doc.get("structured_fields", {})
        dtype = doc.get("document_type")

        if dtype == "bill":
            raw_amount = _first_field_value(fields, "amount", 0)
            claim_amount = float(raw_amount or 0)

        if dtype == "policy":
            claimant_name = str(_first_field_value(fields, "holder_name", "") or "")

        if dtype == "report":
            incident_date = _first_field_value(fields, "incident_date", None)

    incident_date = _parse_date(incident_date)

    policy_start = _parse_date(policy.get("effectiveDate"))
    days_since_policy = 0
    if incident_date and policy_start:
        days_since_policy = (incident_date - policy_start).days

    return claim_amount, claimant_name, days_since_policy


def fraud_detection(node1_output, policy):

    amount, name, days_since_policy = extract_context(node1_output, policy)

    indicators = []
    score = 0

    # round amount rule
    if round_amount_check(amount):
        indicators.append("round number claim amount")
        score += 0.1

    # timing fraud
    if days_since_policy < 7:
        indicators.append("claim too soon after policy start")
        score += 0.2

    # benford
    b_score = benford_score(amount)
    if b_score > 0.2:
        indicators.append("benford distribution anomaly")
        score += 0.2

    # watchlist
    matched, name_hit = watchlist_match(name)
    if matched:
        indicators.append(f"watchlist match: {name_hit}")
        score += 0.4

    # ML anomaly
    if anomaly_score(amount, days_since_policy):
        indicators.append("ml anomaly detected")
        score += 0.3

    score = min(score, 1.0)

    # risk level
    if score < 0.3:
        risk = "LOW"
    elif score < 0.6:
        risk = "MEDIUM"
    elif score < 0.85:
        risk = "HIGH"
    else:
        risk = "CRITICAL"

    return {
        "fraud_score": round(score, 2),
        "fraud_indicators": indicators,
        "risk_level": risk
    }
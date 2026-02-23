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
            try:
                if isinstance(raw_amount, str):
                    clean_amt = "".join(c for c in raw_amount if c.isdigit() or c == ".")
                    claim_amount = float(clean_amt) if clean_amt else 0.0
                else:
                    claim_amount = float(raw_amount or 0)
            except (TypeError, ValueError):
                claim_amount = 0.0

        # Prefer richer LLM extraction
        if not claimant_name:
            claimant_name = fields.get("claimer_name") or str(_first_field_value(fields, "holder_name", "") or "")

        if not incident_date:
            res = fields.get("incident_date")
            incident_date = res[0] if isinstance(res, list) and res else res

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

    # 1. Qualitative AI Analysis
    from app.services.llm_service import llm_service
    # Combine all document texts for context
    context_text = "\n\n".join([
        f"Doc: {doc.get('document_type')}\nText: {doc.get('extracted_text', '')[:1000]}"
        for doc in node1_output.get("documents", [])
    ])
    ai_analysis = llm_service.analyze_claim_context(context_text)
    
    if ai_analysis:
        indicators.extend(ai_analysis.get("fraud_indicators", []))
        # Initial score from AI
        ai_risk_map = {"LOW": 0.1, "MEDIUM": 0.3, "HIGH": 0.6, "CRITICAL": 0.9}
        score += ai_risk_map.get(ai_analysis.get("risk_level", "LOW"), 0.1)

    # 2. Programmatic Rules (Supplemental)
    # round amount rule
    if round_amount_check(amount):
        if "round number claim amount" not in indicators:
            indicators.append("round number claim amount")
        score += 0.05

    # timing fraud
    if days_since_policy < 7:
        if "claim too soon after policy start" not in indicators:
            indicators.append("claim too soon after policy start")
        score += 0.1

    # benford
    b_score = benford_score(amount)
    if b_score > 0.2:
        if "benford distribution anomaly" not in indicators:
            indicators.append("benford distribution anomaly")
        score += 0.1

    # watchlist
    matched, name_hit = watchlist_match(name)
    if matched:
        indicators.append(f"watchlist match: {name_hit}")
        score += 0.3

    # ML anomaly
    if anomaly_score(amount, days_since_policy):
        if "ml anomaly detected" not in indicators:
            indicators.append("ml anomaly detected")
        score += 0.2

    score = min(score, 1.0)

    # risk level (Recalculate based on total score)
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
        "risk_level": risk,
        "reasoning": ai_analysis.get("reasoning", "No qualitative analysis available"),
        "confidence": ai_analysis.get("extraction_confidence", 0.8)
    }
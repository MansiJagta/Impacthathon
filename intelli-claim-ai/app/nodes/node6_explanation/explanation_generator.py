from datetime import datetime


def generate_explanation(node2_output, node3_output, node4_output):

    explanation = []

    # validation summary
    explanation.append("DOCUMENT CONSISTENCY ANALYSIS:")
    explanation.append(
        f"Consistency score: {node2_output.get('consistency_score')}"
    )

    if node2_output.get("mismatches"):
        explanation.append(
            f"Mismatches detected: {node2_output['mismatches']}"
        )
    else:
        explanation.append("No document inconsistencies detected.")

    # coverage summary
    explanation.append("\nPOLICY COVERAGE ANALYSIS:")
    if node3_output.get("is_covered"):
        explanation.append("Claim is covered under policy terms.")
        explanation.append(
            f"Covered amount: {node3_output.get('covered_amount')}"
        )
    else:
        explanation.append(
            f"Claim not covered. Reason: {node3_output.get('reason')}"
        )

    # fraud summary
    explanation.append("\nFRAUD RISK ANALYSIS:")
    explanation.append(
        f"Fraud score: {node4_output.get('fraud_score')}"
    )
    explanation.append(
        f"Risk level: {node4_output.get('risk_level')}"
    )

    if node4_output.get("fraud_indicators"):
        explanation.append(
            f"Fraud indicators: {node4_output['fraud_indicators']}"
        )

    explanation.append("\nSYSTEM RECOMMENDATION:")
    if node4_output.get("risk_level") in ["HIGH", "CRITICAL"]:
        explanation.append(
            "Claim requires human investigator review."
        )
    else:
        explanation.append(
            "Claim can proceed with automated processing."
        )

    return {
        "generated_at": datetime.utcnow(),
        "explanation_text": "\n".join(explanation)
    }
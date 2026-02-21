def analyze_subrogation(node1_output):

    description = ""

    for doc in node1_output["documents"]:
        if doc["document_type"] == "report":
            description = doc["structured_fields"].get("description", "").lower()

    recovery_possible = False
    reason = None

    if "rear-end collision" in description:
        recovery_possible = True
        reason = "Other driver likely at fault"

    if "third party" in description:
        recovery_possible = True
        reason = "Third party liability detected"

    return {
        "subrogation_possible": recovery_possible,
        "recovery_probability": 0.7 if recovery_possible else 0.0,
        "reason": reason
    }
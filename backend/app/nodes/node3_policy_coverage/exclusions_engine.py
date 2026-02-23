def check_exclusions(policy, claim_context):

    triggered = []

    exclusions = policy.get("exclusions", [])
    incident_type = claim_context.get("incident_type", "").lower()
    description = claim_context.get("description", "").lower()

    for exclusion in exclusions:
        e = exclusion.lower()

        if "alcohol" in e and "alcohol" in description:
            triggered.append(exclusion)

        if "commercial" in e and "commercial" in description:
            triggered.append(exclusion)

        if "intentional" in e and "intentional" in description:
            triggered.append(exclusion)

        if "racing" in e and "race" in description:
            triggered.append(exclusion)

    return triggered
from app.database.mongo import policies_collection


def fetch_policy(policy_number: str):
    policy = policies_collection.find_one({"policyNumber": policy_number})

    if not policy:
        return None

    return policy
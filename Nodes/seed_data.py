import random
from database import collection

# generate_embedding is imported but not used in this script presently,
# but we'll keep it as requested to avoid 'unused' errors if the user expects it.
from similarity import generate_embedding


def seed_database():
    print("Clearing existing data...")
    collection.delete_many({})  # clear old data

    severities = ["LOW", "MEDIUM", "HIGH"]
    claim_types = ["motor", "health", "property"]

    damage_descriptions = {
        "motor": [
            "rear bumper damage",
            "front collision impact",
            "windshield crack",
            "engine flooding",
            "side door dent",
            "total loss collision",
        ],
        "health": [
            "hospitalization for dengue",
            "knee replacement surgery",
            "cardiac bypass procedure",
            "fracture treatment",
            "ICU admission for pneumonia",
        ],
        "property": [
            "fire damage in kitchen",
            "water leakage ceiling damage",
            "burglary theft loss",
            "earthquake structural crack",
            "electrical short circuit damage",
        ],
    }

    print("Seeding new data...")
    for i in range(50):
        claim_type = random.choice(claim_types)
        damage_desc = random.choice(damage_descriptions[claim_type])
        final_cost = random.randint(20000, 150000)

        claim = {
            "claim_id": f"CL-{i:03d}",
            "damage_description": damage_desc,
            "policy_limit": random.randint(100000, 500000),
            "deductible": random.randint(500, 5000),
            "fraud_score": round(random.uniform(0.05, 0.9), 2),
            "final_cost": final_cost,
            "settlement_days": random.randint(3, 45),
            "severity": random.choice(severities),
        }

        collection.insert_one(claim)

    print(f"Successfully seeded {collection.count_documents({})} claims!")


if __name__ == "__main__":
    seed_database()

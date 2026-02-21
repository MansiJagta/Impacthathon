from app.database.mongo import policies_collection
from datetime import datetime

policy = {
    "policyNumber": "MOT-12345678",
    "policyType": "motor",
    "holderName": "JOHN SMITH",

    "effectiveDate": datetime(2026,1,1),
    "expiryDate": datetime(2026,12,31),

    "sumInsured": 500000,

    "coverageDetails": {
        "deductible": 5000,
        "limits": {
            "ownDamage": 500000
        }
    },

    "exclusions": [
        "Driving under influence of alcohol",
        "Commercial use of vehicle",
        "Intentional damage",
        "Racing"
    ]
}

policies_collection.insert_one(policy)
print("Policy inserted successfully")
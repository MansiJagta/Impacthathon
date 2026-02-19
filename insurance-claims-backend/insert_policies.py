# insert_policies.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

async def insert_policies():
    """Insert policy data into MongoDB for Node 3 to use"""
    
    print("="*60)
    print("📄 INSERTING POLICY DATA INTO MONGODB")
    print("="*60)
    
    # Connect to MongoDB
    mongo_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DB_NAME", "insurance_claiming_platform")
    
    if not mongo_uri:
        print("❌ MONGODB_URI not found in .env file")
        return
    
    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    
    # Test connection
    await client.admin.command('ping')
    print("✅ Connected to MongoDB Atlas")
    
    # Define policy data that matches what Node 3 expects
    policies = [
        {
            "policyNumber": "MOT-123456",
            "policyType": "motor",
            "holderName": "John Smith",
            "holderId": "CUST-78901",
            "effectiveDate": "2026-01-01T00:00:00Z",
            "expiryDate": "2026-12-31T00:00:00Z",
            "sumInsured": 500000,
            "coverageDetails": {
                "comprehensive": True,
                "thirdParty": True,
                "personalAccident": True,
                "deductible": 5000,
                "limits": {
                    "ownDamage": 500000,
                    "thirdParty": "unlimited",
                    "personalAccident": 200000,
                    "passengerCover": 100000
                }
            },
            "exclusions": [
                "Driving under influence of alcohol/drugs",
                "Vehicle used for commercial purposes",
                "Driving without valid license",
                "Wear and tear / mechanical breakdown",
                "Damage to tyres and tubes unless vehicle damaged simultaneously",
                "War or nuclear perils",
                "Intentional damage",
                "Racing or speed testing"
            ]
        },
        {
            "policyNumber": "HEALTH-456789",
            "policyType": "health",
            "holderName": "Robert Johnson",
            "holderId": "CUST-78903",
            "effectiveDate": "2026-01-15T00:00:00Z",
            "expiryDate": "2027-01-14T00:00:00Z",
            "sumInsured": 500000,
            "coverageDetails": {
                "hospitalization": True,
                "dayCare": True,
                "domiciliary": True,
                "deductible": 2000,
                "limits": {
                    "annual": 500000,
                    "roomRent": 10000,
                    "icuRent": 20000
                }
            },
            "exclusions": [
                "Pre-existing conditions (first 4 years)",
                "Cosmetic surgery",
                "Dental treatment (unless accident)",
                "Alternative medicine",
                "Self-inflicted injuries"
            ]
        }
    ]
    
    # Insert policies (replace if exists)
    for policy in policies:
        result = await db.policies.update_one(
            {"policyNumber": policy["policyNumber"]},
            {"$set": policy},
            upsert=True
        )
        
        if result.upserted_id:
            print(f"✅ Inserted new policy: {policy['policyNumber']}")
        else:
            print(f"🔄 Updated existing policy: {policy['policyNumber']}")
    
    # Verify insertion
    count = await db.policies.count_documents({})
    print(f"\n📊 Total policies in database: {count}")
    
    # Show sample
    sample = await db.policies.find_one({"policyNumber": "MOT-123456"})
    if sample:
        print(f"\n✅ Sample policy loaded:")
        print(f"   • Policy: {sample.get('policyNumber')}")
        print(f"   • Holder: {sample.get('holderName')}")
        print(f"   • Deductible: {sample['coverageDetails'].get('deductible')}")
    
    client.close()
    print("\n🔌 Disconnected from MongoDB")

if __name__ == "__main__":
    asyncio.run(insert_policies())
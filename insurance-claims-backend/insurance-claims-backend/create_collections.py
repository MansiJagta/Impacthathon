# create_collections.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def create_collections():
    print("="*50)
    print("📦 CREATING MONGODB COLLECTIONS")
    print("="*50)
    
    mongo_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DB_NAME", "insurance_claiming_platform")
    
    if not mongo_uri:
        print("❌ MONGODB_URI not found in .env file")
        return
    
    print(f"📂 Connecting to database: {db_name}")
    
    client = None
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas")
        
        # Create claims collection (if it doesn't exist)
        collections = await db.list_collection_names()
        
        if "claims" not in collections:
            await db.create_collection("claims")
            print("✅ Created 'claims' collection")
        else:
            print("ℹ️ 'claims' collection already exists")
        
        # Create index on claim_id for faster lookups
        await db.claims.create_index("claim_id", unique=True)
        print("✅ Created index on claim_id")
        
        # Create index on policyNumber in policies collection (if it exists)
        if "policies" in collections:
            await db.policies.create_index("policyNumber", unique=True)
            print("✅ Created index on policyNumber")
        else:
            print("⚠️ 'policies' collection not found - skipping index")
        
        # Create sample document in claims (optional)
        sample_claim = {
            "claim_id": "SAMPLE-001",
            "claim_amount": 75000,
            "status": "testing"
        }
        await db.claims.insert_one(sample_claim)
        print("✅ Added sample claim document")
        
        print("\n📊 Collection Status:")
        print(f"   • claims: {await db.claims.count_documents({})} documents")
        if "policies" in collections:
            print(f"   • policies: {await db.policies.count_documents({})} documents")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        if client:
            client.close()  # NOT await - this is synchronous!
            print("🔌 Connection closed")

if __name__ == "__main__":
    asyncio.run(create_collections())
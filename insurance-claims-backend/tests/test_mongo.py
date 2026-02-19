# test_mongo.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    print("="*50)
    print("🔌 TESTING MONGODB CONNECTION")
    print("="*50)
    
    # Get connection string
    mongo_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DB_NAME", "insurance_claiming_platform")
    
    if not mongo_uri:
        print("❌ MONGODB_URI not found in .env file")
        return False
    
    print(f"📂 Database: {db_name}")
    print(f"🔗 URI: {mongo_uri[:50]}...")
    
    client = None
    try:
        # Connect
        client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Ping the database
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        
        # List databases
        dbs = await client.list_database_names()
        print(f"📊 Available databases: {dbs}")
        
        # Check if our database exists
        if db_name in dbs:
            print(f"✅ Database '{db_name}' exists")
            
            # List collections
            db = client[db_name]
            collections = await db.list_collection_names()
            print(f"📁 Collections: {collections}")
            
            if "claims" in collections:
                count = await db.claims.count_documents({})
                print(f"📊 Claims collection has {count} documents")
            else:
                print("ℹ️ 'claims' collection not found - this is OK for now")
                
            if "policies" in collections:
                count = await db.policies.count_documents({})
                print(f"📊 Policies collection has {count} documents")
            else:
                print("ℹ️ 'policies' collection not found - this is OK for now")
        else:
            print(f"⚠️ Database '{db_name}' not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
        
    finally:
        if client:
            client.close()
            print("🔌 Connection closed")

if __name__ == "__main__":
    asyncio.run(test_connection())
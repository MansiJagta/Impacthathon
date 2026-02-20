# app/database/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo.errors import OperationFailure

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ROOT_ENV_PATH = PROJECT_ROOT / ".env"
TESTS_ENV_PATH = PROJECT_ROOT / "tests" / ".env"

load_dotenv(ROOT_ENV_PATH)
if not os.getenv("MONGODB_URI") and TESTS_ENV_PATH.exists():
    load_dotenv(TESTS_ENV_PATH)

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

mongodb = MongoDB()

async def connect_to_mongo():
    """Connect to MongoDB Atlas"""
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        raise ValueError("MONGODB_URI is not set. Add it to .env or tests/.env")

    mongodb.client = AsyncIOMotorClient(mongodb_uri, serverSelectionTimeoutMS=10000)
    db_name = os.getenv("MONGODB_DB") or os.getenv("MONGODB_DB_NAME")
    if not db_name:
        raise ValueError("MONGODB_DB or MONGODB_DB_NAME is not set in environment")

    mongodb.db = mongodb.client[db_name] if db_name else None

    try:
        await mongodb.client.admin.command("ping")
    except OperationFailure as exc:
        raise RuntimeError(
            "MongoDB Atlas authentication failed. Verify username/password in MONGODB_URI."
        ) from exc

    print("✅ Connected to MongoDB Atlas")

async def close_mongo_connection():
    """Close MongoDB connection"""
    if mongodb.client:
        mongodb.client.close()
        print("🔌 Disconnected from MongoDB")

def get_database():
    """Get database instance"""
    return mongodb.db

def get_collection(collection_name: str):
    """Get specific collection"""
    return mongodb.db[collection_name]
"""Policy CRUD operations."""

# app/database/repositories/policy_repo.py
from motor.motor_asyncio import AsyncIOMotorCollection
from app.database.mongodb import get_collection
from app.models.policy import PolicyModel
from typing import Optional

class PolicyRepository:
    """Repository for policy operations"""
    
    def __init__(self):
        self._collection = None
    
    @property
    def collection(self) -> AsyncIOMotorCollection:
        """Lazy-load collection"""
        if self._collection is None:
            self._collection = get_collection("policies")
        return self._collection
    
    async def find_by_policy_number(self, policy_number: str) -> Optional[dict]:
        """Find policy by policy number"""
        return await self.collection.find_one({"policyNumber": policy_number})
    
    async def find_all(self, limit: int = 100) -> list:
        """Find all policies (for testing)"""
        cursor = self.collection.find().limit(limit)
        return await cursor.to_list(length=limit)

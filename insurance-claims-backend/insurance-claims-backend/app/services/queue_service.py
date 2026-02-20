"""Underwriter queue management."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pymongo import ReturnDocument

from app.database.mongodb import connect_to_mongo, mongodb


class QueueService:
	"""Service for HITL underwriter queue stored in HITL_db."""

	def __init__(self) -> None:
		self.database_name = "HITL_db"
		self.collection_name = "flagged_claims"

	async def _get_collection(self):
		if mongodb.client is None:
			await connect_to_mongo()
		return mongodb.client[self.database_name][self.collection_name]

	async def list_flagged_claims(
		self,
		status: Optional[str] = None,
		limit: int = 50,
	) -> List[Dict[str, Any]]:
		collection = await self._get_collection()
		query: Dict[str, Any] = {}
		if status:
			query["status"] = status

		cursor = collection.find(query).sort("updated_at", -1).limit(limit)
		items = await cursor.to_list(length=limit)

		for item in items:
			item["_id"] = str(item["_id"])

		return items

	async def update_flag_status(
		self,
		claim_id: str,
		status: str,
		reviewer: Optional[str] = None,
		notes: Optional[str] = None,
	) -> Optional[Dict[str, Any]]:
		collection = await self._get_collection()

		update_doc: Dict[str, Any] = {
			"status": status,
			"updated_at": datetime.utcnow().isoformat(),
		}
		if reviewer:
			update_doc["reviewed_by"] = reviewer
		if notes:
			update_doc["review_notes"] = notes

		result = await collection.find_one_and_update(
			{"claim_id": claim_id},
			{"$set": update_doc},
			return_document=ReturnDocument.AFTER,
		)

		if result is None:
			return None

		result["_id"] = str(result["_id"])
		return result

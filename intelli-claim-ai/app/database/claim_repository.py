from __future__ import annotations

from datetime import datetime
from typing import Any

from app.database.mongo import claims_collection


def _utcnow() -> datetime:
	return datetime.utcnow()


def create_claim_record(claim_document: dict[str, Any]) -> str:
	now = _utcnow()
	claim_document.setdefault("created_at", now)
	claim_document.setdefault("updated_at", now)
	result = claims_collection.insert_one(claim_document)
	return str(result.inserted_id)


def get_claim_by_id(claim_id: str) -> dict[str, Any] | None:
	return claims_collection.find_one({"claim_id": claim_id}, {"_id": 0})


def list_claims(
	*,
	claimer_email: str | None = None,
	status: str | None = None,
	claim_type: str | None = None,
	search: str | None = None,
	limit: int = 50,
) -> list[dict[str, Any]]:
	query: dict[str, Any] = {}

	if claimer_email:
		query["claimer.email"] = claimer_email
	if status:
		query["status"] = status
	if claim_type:
		query["claim_type"] = claim_type
	if search:
		query["$or"] = [
			{"claim_id": {"$regex": search, "$options": "i"}},
			{"claim_type": {"$regex": search, "$options": "i"}},
			{"claimer.name": {"$regex": search, "$options": "i"}},
			{"claimer.email": {"$regex": search, "$options": "i"}},
		]

	cursor = claims_collection.find(query, {"_id": 0}).sort("created_at", -1).limit(limit)
	return list(cursor)


def list_reviewer_queue(fraud_threshold: float = 0.6, limit: int = 50) -> list[dict[str, Any]]:
	cursor = (
		claims_collection.find(
			{
				"status": {"$in": ["PENDING_REVIEW", "FLAGGED_FOR_REVIEW", "ESCALATED_FRAUD_REVIEW"]},
				"fraud_score": {"$gte": fraud_threshold},
			},
			{"_id": 0},
		)
		.sort("fraud_score", -1)
		.limit(limit)
	)
	return list(cursor)


def list_processed_claims(limit: int = 100) -> list[dict[str, Any]]:
	cursor = (
		claims_collection.find(
			{"status": {"$in": ["APPROVED", "REJECTED", "REQUESTED_MORE_INFO"]}},
			{"_id": 0},
		)
		.sort("updated_at", -1)
		.limit(limit)
	)
	return list(cursor)


def update_claim_review(
	claim_id: str,
	*,
	status: str,
	reviewer: dict[str, Any],
	note: str | None,
) -> bool:
	update_doc: dict[str, Any] = {
		"status": status,
		"review": {
			"reviewer": reviewer,
			"note": note,
			"reviewed_at": _utcnow(),
		},
		"updated_at": _utcnow(),
	}
	result = claims_collection.update_one({"claim_id": claim_id}, {"$set": update_doc})
	return result.matched_count > 0


def get_claimer_stats(claimer_email: str) -> dict[str, Any]:
	pipeline = [
		{"$match": {"claimer.email": claimer_email}},
		{
			"$group": {
				"_id": None,
				"total": {"$sum": 1},
				"approved": {"$sum": {"$cond": [{"$eq": ["$status", "APPROVED"]}, 1, 0]}},
				"pending": {
					"$sum": {
						"$cond": [
							{"$in": ["$status", ["PENDING_REVIEW", "FLAGGED_FOR_REVIEW", "ESCALATED_FRAUD_REVIEW"]]},
							1,
							0,
						]
					}
				},
				"flagged": {
					"$sum": {
						"$cond": [
							{"$in": ["$status", ["FLAGGED_FOR_REVIEW", "ESCALATED_FRAUD_REVIEW"]]},
							1,
							0,
						]
					}
				},
				"rejected": {"$sum": {"$cond": [{"$eq": ["$status", "REJECTED"]}, 1, 0]}},
				"avg_amount": {"$avg": "$claim_amount"},
				"last_claim_at": {"$max": "$created_at"},
			}
		},
	]

	rows = list(claims_collection.aggregate(pipeline))
	if not rows:
		return {
			"total": 0,
			"approved": 0,
			"pending": 0,
			"flagged": 0,
			"rejected": 0,
			"avg_amount": 0.0,
			"last_claim_at": None,
		}
	row = rows[0]
	row.pop("_id", None)
	return row


def search_user_claims(search_text: str, limit: int = 50) -> list[dict[str, Any]]:
	query = {
		"$or": [
			{"claimer.name": {"$regex": search_text, "$options": "i"}},
			{"claimer.email": {"$regex": search_text, "$options": "i"}},
			{"claim_id": {"$regex": search_text, "$options": "i"}},
		]
	}
	cursor = claims_collection.find(query, {"_id": 0}).sort("created_at", -1).limit(limit)
	return list(cursor)


def get_admin_metrics() -> dict[str, Any]:
	pipeline = [
		{
			"$group": {
				"_id": None,
				"total_claims": {"$sum": 1},
				"approved": {"$sum": {"$cond": [{"$eq": ["$status", "APPROVED"]}, 1, 0]}},
				"flagged": {
					"$sum": {
						"$cond": [
							{"$in": ["$status", ["FLAGGED_FOR_REVIEW", "ESCALATED_FRAUD_REVIEW"]]},
							1,
							0,
						]
					}
				},
				"avg_fraud_score": {"$avg": "$fraud_score"},
				"avg_process_minutes": {"$avg": "$processing_minutes"},
			}
		}
	]
	rows = list(claims_collection.aggregate(pipeline))
	if not rows:
		return {
			"total_claims": 0,
			"approved": 0,
			"flagged": 0,
			"avg_fraud_score": 0.0,
			"avg_process_minutes": 0.0,
		}
	row = rows[0]
	row.pop("_id", None)
	return row


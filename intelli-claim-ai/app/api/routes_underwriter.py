from __future__ import annotations

from collections import Counter
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.database.claim_repository import (
	get_admin_metrics,
	get_claim_by_id,
	get_claimer_stats,
	list_claims,
	list_processed_claims,
	list_reviewer_queue,
	search_user_claims,
	update_claim_review,
)
from app.models.api_schemas import (
	AdminDashboardResponse,
	ClaimSummary,
	ReviewerDecisionRequest,
	ReviewerDecisionResponse,
	ReviewerQueueResponse,
	SearchUserResponse,
)

router = APIRouter(prefix="/api", tags=["reviewer", "admin"])


def _badge_for_status(status: str) -> str:
	if status == "APPROVED":
		return "Approved"
	if status == "REJECTED":
		return "Rejected"
	if status in {"FLAGGED_FOR_REVIEW", "ESCALATED_FRAUD_REVIEW"}:
		return "Flagged"
	return "Pending"


def _to_summary(row: dict[str, Any]) -> ClaimSummary:
	return ClaimSummary(
		claim_id=row.get("claim_id", ""),
		claim_type=row.get("claim_type", "Unknown"),
		claim_amount=float(row.get("claim_amount", 0.0) or 0.0),
		status=row.get("status", "PENDING_REVIEW"),
		badge=_badge_for_status(row.get("status", "PENDING_REVIEW")),
		fraud_score=float(row.get("fraud_score", 0.0) or 0.0),
		risk_score=float(row.get("risk_score", row.get("fraud_score", 0.0)) or 0.0),
		created_at=row.get("created_at"),
		summary=row.get("decision_reason") or row.get("status"),
	)


@router.get("/reviewer/queue", response_model=ReviewerQueueResponse)
def get_reviewer_queue(
	fraud_threshold: float = Query(default=0.6, ge=0.0, le=1.0),
	limit: int = Query(default=50, ge=1, le=200),
):
	rows = list_reviewer_queue(fraud_threshold=fraud_threshold, limit=limit)
	return ReviewerQueueResponse(claims=[_to_summary(row) for row in rows])


@router.get("/reviewer/history")
def get_reviewer_history(limit: int = Query(default=100, ge=1, le=300)):
	rows = list_processed_claims(limit=limit)
	return {
		"count": len(rows),
		"claims": [_to_summary(row).model_dump() for row in rows],
	}


@router.post("/reviewer/claims/{claim_id}/decision", response_model=ReviewerDecisionResponse)
def review_claim(claim_id: str, payload: ReviewerDecisionRequest):
	claim = get_claim_by_id(claim_id)
	if not claim:
		raise HTTPException(status_code=404, detail="Claim not found")

	status_mapping = {
		"approve": "APPROVED",
		"reject": "REJECTED",
		"request_more_info": "REQUESTED_MORE_INFO",
	}
	new_status = status_mapping[payload.decision]

	ok = update_claim_review(
		claim_id,
		status=new_status,
		reviewer={"name": payload.reviewer_name, "email": payload.reviewer_email},
		note=payload.note,
	)
	if not ok:
		raise HTTPException(status_code=404, detail="Claim not found")

	return ReviewerDecisionResponse(
		claim_id=claim_id,
		updated_status=new_status,
		message="Review decision saved",
	)


@router.get("/reviewer/users/search", response_model=SearchUserResponse)
def search_user(query: str = Query(..., min_length=1), limit: int = Query(default=50, ge=1, le=300)):
	rows = search_user_claims(query, limit=limit)
	claims = [_to_summary(row) for row in rows]

	email_candidates = [row.get("claimer", {}).get("email") for row in rows if row.get("claimer")]
	email = email_candidates[0] if email_candidates else query
	stats = get_claimer_stats(email)

	return SearchUserResponse(
		query=query,
		claims=claims,
		stats={
			"total_claims": int(stats.get("total", 0)),
			"approval_rate": (
				round((int(stats.get("approved", 0)) / max(int(stats.get("total", 0)), 1)) * 100, 2)
			),
			"avg_amount": float(stats.get("avg_amount", 0.0) or 0.0),
			"last_claim_at": stats.get("last_claim_at"),
		},
	)


@router.get("/admin/dashboard", response_model=AdminDashboardResponse)
def get_admin_dashboard():
	metrics = get_admin_metrics()
	claims = list_claims(limit=1000)

	total = int(metrics.get("total_claims", 0))
	approved = int(metrics.get("approved", 0))
	flagged = int(metrics.get("flagged", 0))

	by_type = Counter((row.get("claim_type") or "Unknown") for row in claims)
	claims_by_type = {
		"Health": 0.0,
		"Motor": 0.0,
		"Property": 0.0,
	}
	if total > 0:
		for key in claims_by_type:
			claims_by_type[key] = round((by_type.get(key, 0) / total) * 100, 2)

	auto_rate = round((approved / max(total, 1)) * 100, 2)
	fraud_flagged_pct = round((flagged / max(total, 1)) * 100, 2)

	return AdminDashboardResponse(
		total_claims=total,
		auto_rate=auto_rate,
		avg_process_minutes=float(metrics.get("avg_process_minutes", 0.0) or 0.0),
		fraud_accuracy=round((1.0 - float(metrics.get("avg_fraud_score", 0.0) or 0.0)) * 100, 2),
		fraud_flagged_pct=fraud_flagged_pct,
		fraud_cleared_pct=round(100 - fraud_flagged_pct, 2),
		claims_by_type=claims_by_type,
	)


@router.get("/admin/users/activity")
def get_user_activity(limit: int = Query(default=100, ge=1, le=500)):
	rows = list_claims(limit=limit)
	users: dict[str, dict[str, Any]] = {}

	for row in rows:
		claimer = row.get("claimer", {})
		key = claimer.get("email") or claimer.get("name")
		if not key:
			continue
		if key not in users:
			users[key] = {
				"user": claimer.get("name") or claimer.get("email"),
				"email": claimer.get("email"),
				"role": "Claimer",
				"claims": 0,
				"approved": 0,
				"last_active": row.get("updated_at") or row.get("created_at"),
			}
		users[key]["claims"] += 1
		if row.get("status") == "APPROVED":
			users[key]["approved"] += 1
		recent_time = row.get("updated_at") or row.get("created_at")
		if recent_time and (users[key]["last_active"] is None or recent_time > users[key]["last_active"]):
			users[key]["last_active"] = recent_time

	activity = []
	for _, entry in users.items():
		total_claims = entry["claims"]
		activity.append(
			{
				"user": entry["user"],
				"email": entry["email"],
				"role": entry["role"],
				"claims": total_claims,
				"approval_rate": round((entry["approved"] / max(total_claims, 1)) * 100, 2),
				"last_active": entry["last_active"],
			}
		)

	activity.sort(key=lambda item: item["claims"], reverse=True)
	return {"count": len(activity), "users": activity}


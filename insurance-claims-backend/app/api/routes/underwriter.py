"""Underwriter queue endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.services.queue_service import QueueService

router = APIRouter(prefix="/underwriter", tags=["underwriter"])
queue_service = QueueService()


class ReviewUpdateRequest(BaseModel):
	status: str
	reviewer: Optional[str] = None
	notes: Optional[str] = None


@router.get("/queue")
async def list_queue(
	status: Optional[str] = Query(default=None),
	limit: int = Query(default=50, ge=1, le=200),
):
	return await queue_service.list_flagged_claims(status=status, limit=limit)


@router.patch("/queue/{claim_id}")
async def update_queue_status(claim_id: str, payload: ReviewUpdateRequest):
	allowed_statuses = {"PENDING_REVIEW", "APPROVED", "REJECTED", "ESCALATED"}
	if payload.status not in allowed_statuses:
		raise HTTPException(status_code=400, detail=f"Invalid status. Allowed: {sorted(allowed_statuses)}")

	updated = await queue_service.update_flag_status(
		claim_id=claim_id,
		status=payload.status,
		reviewer=payload.reviewer,
		notes=payload.notes,
	)
	if updated is None:
		raise HTTPException(status_code=404, detail=f"Claim {claim_id} not found in HITL queue")

	return updated

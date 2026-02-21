from __future__ import annotations

import os
import uuid
from datetime import datetime
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile

from app.core.langgraph_builder import run_claim_workflow
from app.database.claim_repository import (
	create_claim_record,
	get_claim_by_id,
	get_claimer_stats,
	list_claims,
)
from app.models.api_schemas import (
	ClaimDetailsResponse,
	ClaimReasoningItem,
	ClaimSubmitRequest,
	ClaimSummary,
	ClaimerDashboardResponse,
	DashboardStats,
)

router = APIRouter(prefix="/api/claims", tags=["claims"])


def _make_claim_id() -> str:
	return f"CL-{datetime.utcnow().year}-{uuid.uuid4().hex[:6].upper()}"


def _badge_for_status(status: str) -> str:
	mapping = {
		"APPROVED": "Approved",
		"REJECTED": "Rejected",
		"PENDING_REVIEW": "Pending",
		"FLAGGED_FOR_REVIEW": "Flagged",
		"ESCALATED_FRAUD_REVIEW": "Flagged",
		"REQUESTED_MORE_INFO": "Pending",
	}
	return mapping.get(status, "Pending")


def _risk_score_from_fraud(fraud_score: float) -> float:
	return min(max(fraud_score, 0.0), 1.0)


def _first(value: Any) -> Any:
	if isinstance(value, list):
		return value[0] if value else None
	return value


def _infer_claim_data_from_node1(node1_output: dict[str, Any]) -> dict[str, Any]:
	documents = node1_output.get("documents", []) if isinstance(node1_output, dict) else []
	policy_number: str | None = None
	claim_amount: float | None = None
	claimer_name: str | None = None
	claimer_address: str | None = None

	for doc in documents:
		fields = doc.get("structured_fields", {}) if isinstance(doc, dict) else {}
		doc_type = doc.get("document_type") if isinstance(doc, dict) else None

		if doc_type == "policy" and not policy_number:
			policy_number = _first(fields.get("policy_number"))

		if doc_type == "bill" and claim_amount is None:
			raw_amount = _first(fields.get("amount"))
			try:
				claim_amount = float(raw_amount) if raw_amount is not None else None
			except (TypeError, ValueError):
				claim_amount = None

		if doc_type == "id_proof":
			if not claimer_name:
				claimer_name = _first(fields.get("name"))
			if not claimer_address:
				claimer_address = _first(fields.get("address"))

	return {
		"policy_number": policy_number,
		"claim_amount": claim_amount,
		"claimer_name": claimer_name,
		"claimer_address": claimer_address,
	}


def _build_submit_response(claim_id: str, final_state: dict[str, Any]) -> dict[str, Any]:
	node3 = final_state.get("node3_output", {})
	node4 = final_state.get("node4_output", {})
	node6 = final_state.get("node6_output", {})
	node7 = final_state.get("node7_output", {})

	status = node7.get("final_status", "PENDING_REVIEW")
	decision_reason = node7.get("reason")
	fraud_score = float(node4.get("fraud_score", 0.0) or 0.0)

	return {
		"claim_id": claim_id,
		"status": status,
		"badge": _badge_for_status(status),
		"decision_reason": decision_reason,
		"fraud_score": fraud_score,
		"covered": bool(node3.get("is_covered", False)),
		"covered_amount": node3.get("covered_amount"),
		"explanation": node6.get("explanation_text"),
	}


def _persist_claim(claim_payload: dict[str, Any], final_state: dict[str, Any], claim_id: str) -> None:
	node3 = final_state.get("node3_output", {})
	node4 = final_state.get("node4_output", {})
	node6 = final_state.get("node6_output", {})
	node7 = final_state.get("node7_output", {})

	status = node7.get("final_status", "PENDING_REVIEW")
	decision_reason = node7.get("reason")
	fraud_score = float(node4.get("fraud_score", 0.0) or 0.0)

	create_claim_record(
		{
			"claim_id": claim_id,
			"claim_type": claim_payload["claim_type"],
			"claim_amount": claim_payload["claim_amount"],
			"policy_number": claim_payload["policy_number"],
			"claimer": claim_payload["claimer"],
			"form_data": claim_payload.get("form_data", {}),
			"document_paths": claim_payload["document_paths"],
			"status": status,
			"decision_reason": decision_reason,
			"human_review_required": bool(node7.get("human_review_required", False)),
			"fraud_score": fraud_score,
			"risk_score": _risk_score_from_fraud(fraud_score),
			"node2_output": final_state.get("node2_output", {}),
			"node3_output": node3,
			"node4_output": node4,
			"node5_output": final_state.get("node5_output", {}),
			"node6_output": node6,
			"node7_output": node7,
			"node8_output": final_state.get("node8_output", {}),
			"processing_minutes": 0.0,
			"created_at": datetime.utcnow(),
			"updated_at": datetime.utcnow(),
		}
	)


def _to_summary(doc: dict[str, Any]) -> ClaimSummary:
	status = doc.get("status", "PENDING_REVIEW")
	fraud_score = float(doc.get("fraud_score", 0.0) or 0.0)
	return ClaimSummary(
		claim_id=doc.get("claim_id", ""),
		claim_type=doc.get("claim_type", "Unknown"),
		claim_amount=float(doc.get("claim_amount", 0.0) or 0.0),
		status=status,
		badge=_badge_for_status(status),
		fraud_score=fraud_score,
		risk_score=_risk_score_from_fraud(fraud_score),
		created_at=doc.get("created_at"),
		summary=doc.get("decision_reason") or doc.get("status"),
	)


def _build_reasoning(doc: dict[str, Any]) -> list[ClaimReasoningItem]:
	node2 = doc.get("node2_output", {})
	node3 = doc.get("node3_output", {})
	node4 = doc.get("node4_output", {})
	node5 = doc.get("node5_output", {})

	items = [
		ClaimReasoningItem(
			node="Cross Validation",
			finding=str(node2.get("reason") or "Documents validated"),
			confidence=node2.get("confidence"),
		),
		ClaimReasoningItem(
			node="Policy Coverage",
			finding="Covered" if node3.get("is_covered") else str(node3.get("reason") or "Not covered"),
			confidence=node3.get("confidence"),
		),
		ClaimReasoningItem(
			node="Fraud Detection",
			finding=", ".join(node4.get("fraud_indicators", [])) or "No major anomaly",
			confidence=node4.get("fraud_score"),
		),
		ClaimReasoningItem(
			node="Predictive Analysis",
			finding=str(node5.get("summary") or "Predictive model assessed claim"),
			confidence=node5.get("confidence"),
		),
	]
	return items


@router.post("/submit")
def submit_claim(payload: ClaimSubmitRequest):
	if not payload.document_paths:
		raise HTTPException(status_code=400, detail="document_paths is required to run the LangGraph workflow")

	claim_id = payload.claim_id or _make_claim_id()

	try:
		final_state = run_claim_workflow(claim_id=claim_id, document_paths=payload.document_paths)
	except Exception as exc:  # noqa: BLE001
		raise HTTPException(status_code=500, detail=f"Claim workflow failed: {exc}") from exc

	_persist_claim(
		{
			"claim_type": payload.claim_type,
			"claim_amount": payload.claim_amount,
			"policy_number": payload.policy_number,
			"claimer": payload.claimer.model_dump(),
			"form_data": payload.form_data,
			"document_paths": payload.document_paths,
		},
		final_state,
		claim_id,
	)

	return _build_submit_response(claim_id, final_state)


@router.post("/submit-upload")
async def submit_claim_with_upload(
	files: list[UploadFile] = File(...),
	claim_type: str = Form(default="Health"),
	claimer_email: str = Form(default=""),
	claimer_phone: str | None = Form(default=None),
	claimer_address: str | None = Form(default=None),
	claimer_name: str | None = Form(default=None),
	claim_id: str | None = Form(default=None),
):
	if not files:
		raise HTTPException(status_code=400, detail="At least one document is required")

	allowed_claim_types = {"Health", "Motor", "Property"}
	if claim_type not in allowed_claim_types:
		raise HTTPException(status_code=400, detail="claim_type must be one of Health, Motor, Property")

	upload_root = os.path.join("temp_images", "uploads")
	os.makedirs(upload_root, exist_ok=True)

	saved_paths: list[str] = []
	for file in files:
		if not file.filename:
			continue
		safe_name = os.path.basename(file.filename)
		ext = os.path.splitext(safe_name)[1].lower()
		if ext not in {".pdf", ".png", ".jpg", ".jpeg", ".webp"}:
			raise HTTPException(status_code=400, detail=f"Unsupported file type for {safe_name}")

		unique_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}_{safe_name}"
		dest = os.path.join(upload_root, unique_name)
		content = await file.read()
		with open(dest, "wb") as out:
			out.write(content)
		saved_paths.append(dest)

	if not saved_paths:
		raise HTTPException(status_code=400, detail="No valid files were uploaded")

	resolved_claim_id = claim_id or _make_claim_id()
	try:
		final_state = run_claim_workflow(claim_id=resolved_claim_id, document_paths=saved_paths)
	except Exception as exc:  # noqa: BLE001
		raise HTTPException(status_code=500, detail=f"Claim workflow failed: {exc}") from exc

	inferred = _infer_claim_data_from_node1(final_state.get("node1_output", {}))
	final_policy_number = inferred.get("policy_number") or "UNKNOWN"
	final_claim_amount = float(inferred.get("claim_amount") or 0.0)
	final_claimer_name = claimer_name or inferred.get("claimer_name") or "Unknown Claimer"
	final_claimer_address = claimer_address or inferred.get("claimer_address")
	final_claimer_email = claimer_email or "unknown@example.com"

	_persist_claim(
		{
			"claim_type": claim_type,
			"claim_amount": final_claim_amount,
			"policy_number": final_policy_number,
			"claimer": {
				"name": final_claimer_name,
				"email": final_claimer_email,
				"phone": claimer_phone,
				"address": final_claimer_address,
			},
			"form_data": {
				"auto_extracted": True,
				"node1_output": final_state.get("node1_output", {}),
			},
			"document_paths": saved_paths,
		},
		final_state,
		resolved_claim_id,
	)

	response = _build_submit_response(resolved_claim_id, final_state)
	response["extracted_claim_data"] = {
		"claim_type": claim_type,
		"claim_amount": final_claim_amount,
		"policy_number": final_policy_number,
		"claimer": {
			"name": final_claimer_name,
			"email": final_claimer_email,
			"phone": claimer_phone,
			"address": final_claimer_address,
		},
		"document_paths": saved_paths,
	}
	return response


@router.get("/dashboard/{claimer_email}", response_model=ClaimerDashboardResponse)
def get_claimer_dashboard(claimer_email: str):
	stats = get_claimer_stats(claimer_email)
	recent = list_claims(claimer_email=claimer_email, limit=5)

	return ClaimerDashboardResponse(
		stats=DashboardStats(
			total=int(stats.get("total", 0)),
			approved=int(stats.get("approved", 0)),
			pending=int(stats.get("pending", 0)),
			flagged=int(stats.get("flagged", 0)),
		),
		recent_claims=[_to_summary(item) for item in recent],
	)


@router.get("")
def get_claims(
	claimer_email: str | None = Query(default=None),
	status: str | None = Query(default=None),
	claim_type: str | None = Query(default=None),
	search: str | None = Query(default=None),
	limit: int = Query(default=50, ge=1, le=200),
):
	rows = list_claims(
		claimer_email=claimer_email,
		status=status,
		claim_type=claim_type,
		search=search,
		limit=limit,
	)
	return {
		"count": len(rows),
		"claims": [_to_summary(row).model_dump() for row in rows],
	}


@router.get("/{claim_id}", response_model=ClaimDetailsResponse)
def get_claim_details(claim_id: str):
	doc = get_claim_by_id(claim_id)
	if not doc:
		raise HTTPException(status_code=404, detail="Claim not found")

	claimer = doc.get("claimer") or {}
	fraud_score = float(doc.get("fraud_score", 0.0) or 0.0)
	decision = doc.get("node7_output", {})

	return ClaimDetailsResponse(
		claim_id=doc.get("claim_id", ""),
		claim_type=doc.get("claim_type", "Unknown"),
		claim_amount=float(doc.get("claim_amount", 0.0) or 0.0),
		status=doc.get("status", "PENDING_REVIEW"),
		ai_decision=decision.get("final_status"),
		confidence=doc.get("node3_output", {}).get("confidence"),
		fraud_score=fraud_score,
		risk_score=float(doc.get("risk_score", _risk_score_from_fraud(fraud_score))),
		policy_number=doc.get("policy_number"),
		claimer={
			"name": claimer.get("name", ""),
			"email": claimer.get("email", ""),
			"phone": claimer.get("phone"),
			"address": claimer.get("address"),
		},
		metadata=doc.get("form_data", {}),
		reasoning=_build_reasoning(doc),
		explanation=doc.get("node6_output", {}).get("explanation_text"),
		documents=doc.get("document_paths", []),
	)


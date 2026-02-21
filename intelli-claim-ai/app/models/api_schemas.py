from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class ClaimerInfo(BaseModel):
    name: str
    email: str
    phone: str | None = None
    address: str | None = None


class ClaimSubmitRequest(BaseModel):
    claim_id: str | None = None
    claim_type: Literal["Health", "Motor", "Property"]
    claim_amount: float
    policy_number: str
    document_paths: list[str] = Field(default_factory=list)
    form_data: dict[str, Any] = Field(default_factory=dict)
    claimer: ClaimerInfo


class ClaimSummary(BaseModel):
    claim_id: str
    claim_type: str
    claim_amount: float
    status: str
    badge: str
    fraud_score: float = 0.0
    risk_score: float = 0.0
    created_at: datetime | None = None
    summary: str | None = None


class DashboardStats(BaseModel):
    total: int
    approved: int
    pending: int
    flagged: int


class ClaimerDashboardResponse(BaseModel):
    stats: DashboardStats
    recent_claims: list[ClaimSummary]


class ClaimReasoningItem(BaseModel):
    node: str
    finding: str
    confidence: float | None = None


class ClaimDetailsResponse(BaseModel):
    claim_id: str
    claim_type: str
    claim_amount: float
    status: str
    ai_decision: str | None = None
    confidence: float | None = None
    fraud_score: float = 0.0
    risk_score: float = 0.0
    policy_number: str | None = None
    claimer: ClaimerInfo
    metadata: dict[str, Any] = Field(default_factory=dict)
    reasoning: list[ClaimReasoningItem] = Field(default_factory=list)
    explanation: str | None = None
    documents: list[str] = Field(default_factory=list)


class ReviewerQueueResponse(BaseModel):
    claims: list[ClaimSummary]


class ReviewerDecisionRequest(BaseModel):
    decision: Literal["approve", "reject", "request_more_info"]
    reviewer_name: str
    reviewer_email: str
    note: str | None = None


class ReviewerDecisionResponse(BaseModel):
    claim_id: str
    updated_status: str
    message: str


class SearchUserResponse(BaseModel):
    query: str
    claims: list[ClaimSummary]
    stats: dict[str, Any]


class AdminDashboardResponse(BaseModel):
    total_claims: int
    auto_rate: float
    avg_process_minutes: float
    fraud_accuracy: float
    fraud_flagged_pct: float
    fraud_cleared_pct: float
    claims_by_type: dict[str, float]

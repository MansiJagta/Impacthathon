from pydantic import BaseModel
from typing import List


class UploadedDocument(BaseModel):
    document_name: str
    document_url: str


class ExtractedData(BaseModel):
    damage_description: str
    claim_amount: float


class PolicyAnalysis(BaseModel):
    policy_number: str
    is_covered: bool
    coverage_score: float
    deductible: float
    policy_limit: float
    covered_amount: float
    exclusions_triggered: List[str]
    relevant_clauses: List[str]
    policy_type: str
    holder_name: str
    confidence: float


class TimingAnalysis(BaseModel):
    days_since_policy: int
    is_suspicious: bool


class DuplicateCheck(BaseModel):
    is_duplicate: bool
    similar_claims: List[str]


class BenfordAnalysis(BaseModel):
    passed: bool
    anomaly_score: float


class FraudAnalysis(BaseModel):
    fraud_score: float
    fraud_indicators: List[str]
    duplicate_check: DuplicateCheck
    benford_analysis: BenfordAnalysis
    timing_analysis: TimingAnalysis
    confidence: float


class ClaimInput(BaseModel):
    claim_id: str
    extracted_data: ExtractedData
    consistency_score: float
    policy_analysis: PolicyAnalysis
    fraud_analysis: FraudAnalysis
    documents: List[UploadedDocument] = []


class ReviewNote(BaseModel):
    note: str


class AssignReviewer(BaseModel):
    reviewer_name: str

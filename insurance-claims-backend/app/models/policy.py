# app/models/policy.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class PolicyLimits(BaseModel):
    ownDamage: float
    thirdParty: str = "unlimited"
    personalAccident: float

class CoverageDetails(BaseModel):
    comprehensive: bool = False
    thirdParty: bool = False
    personalAccident: bool = False
    deductible: int = 0
    limits: Dict[str, Any] = Field(default_factory=dict)

class PolicyModel(BaseModel):
    policyNumber: str
    policyType: str
    holderName: str
    holderId: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Dict[str, Any] = Field(default_factory=dict)
    effectiveDate: str | datetime
    expiryDate: str | datetime
    sumInsured: float
    coverageDetails: CoverageDetails
    exclusions: List[str]
    createdAt: Optional[str | datetime] = None
    updatedAt: Optional[str | datetime] = None

    model_config = ConfigDict(extra="ignore")

class CoverageAnalysis(BaseModel):
    """Output model for Node 3"""
    policy_number: str
    is_covered: bool
    coverage_score: float = Field(ge=0, le=1)
    deductible: int
    policy_limit: float
    covered_amount: float
    exclusions_triggered: List[str]
    relevant_clauses: List[str]
    policy_type: str
    holder_name: str
    confidence: float = Field(ge=0, le=1)
    error: Optional[str] = None
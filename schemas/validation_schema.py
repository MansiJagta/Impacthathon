from pydantic import BaseModel, Field
from typing import List, Optional, Literal


# ============================================================
# Individual Check Result
# ============================================================

class CheckResult(BaseModel):
    """
    Represents the result of a single validation check.
    Example checks:
    - name_match_check
    - chronology_check
    - required_docs_check
    - date_consistency_check
    """

    check_name: str = Field(..., description="Unique name of the validation check")

    # Check category for risk breakdown and explainability
    check_type: Optional[Literal[
        "identity",
        "chronology",
        "financial",
        "location",
        "document"
    ]] = Field(
        None,
        description="Category of the check for risk breakdown and analytics"
    )

    # Score: 0 = safe, 1 = high risk (normalized)
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Risk contribution of this check (0 = no risk, 1 = high risk)"
    )

    # Confidence in the check result (model or rule confidence)
    # Default to 1.0 for rule-based checks (deterministic)
    confidence: float = Field(
        1.0,
        ge=0.0,
        le=1.0,
        description="Confidence level of this check"
    )

    # Optional status for readability
    status: Optional[Literal["pass", "fail", "warning"]] = Field(
        None,
        description="Human-readable check outcome"
    )

    # Optional explanation (very useful for explainability node)
    message: Optional[str] = Field(
        None,
        description="Detailed explanation of why this check passed or failed"
    )

    # Optional metadata for deeper analysis
    metadata: Optional[dict] = Field(
        None,
        description="Additional structured data related to the check"
    )


# ============================================================
# Aggregated Validation Output
# ============================================================

class ValidationOutput(BaseModel):
    """
    Aggregated validation output after all checks.
    """

    checks: List[CheckResult] = Field(
        ...,
        description="List of all validation checks performed"
    )

    # Final aggregated risk score (0 to 1)
    total_risk_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Final normalized risk score after combining all checks"
    )

    # Optional risk category (for decision node)
    risk_category: Optional[Literal["low", "medium", "high"]] = Field(
        None,
        description="Risk bucket derived from total_risk_score"
    )

    # Optional decision suggestion
    recommended_action: Optional[
        Literal["approve", "manual_review", "reject"]
    ] = Field(
        None,
        description="System-suggested action based on risk"
    )
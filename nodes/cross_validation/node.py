from typing import Dict, Any, List

from langgraph_flow.state import ClaimState
from schemas.validation_schema import ValidationOutput, CheckResult
from schemas.extraction_schema import (
    HealthClaimExtraction,
    MotorClaimExtraction,
    DeathClaimExtraction,
)
from nodes.cross_validation.checks.name_match_check import NameMatchCheck
from nodes.cross_validation.checks.chronology_check import ChronologyCheck
from nodes.cross_validation.checks.financial_check import FinancialCheck


def cross_validation_node(state: ClaimState) -> Dict[str, Any]:
    """
    LangGraph validation node that performs comprehensive cross-validation checks.
    
    Orchestrates:
    - Name matching checks with fuzzy similarity
    - Date/chronology validation
    - Financial amount validation
    - Risk aggregation and categorization
    
    Returns:
        Dictionary with validation_results (ValidationOutput) and total_risk_score
    """

    extracted = state.get("extracted_entities")
    if not extracted:
        return {
            "validation_results": ValidationOutput(
                checks=[],
                total_risk_score=0.0,
                risk_category="low",
                recommended_action="approve"
            ),
            "total_risk_score": 0.0
        }

    # Initialize check instances
    name_check = NameMatchCheck()
    chronology_check = ChronologyCheck()
    financial_check = FinancialCheck()

    # Run all validation checks
    checks = []

    try:
        checks.extend(name_check.run(extracted))
        checks.extend(chronology_check.run(extracted))
        checks.extend(financial_check.run(extracted))
    except Exception as e:
        print(f"[CrossValidation] Error during validation: {str(e)}")

    # Calculate aggregated risk score
    total_risk_score, risk_category, recommended_action = _aggregate_risk(checks)

    validation_output = ValidationOutput(
        checks=checks,
        total_risk_score=total_risk_score,
        risk_category=risk_category,
        recommended_action=recommended_action
    )

    return {
        "validation_results": validation_output,
        "total_risk_score": total_risk_score
    }


def _aggregate_risk(checks: List[CheckResult]) -> tuple[float, str, str]:
    """
    Aggregate risk scores and determine risk category and recommended action.
    
    Args:
        checks: List of CheckResult objects from all validation checks
        
    Returns:
        Tuple of (total_risk_score, risk_category, recommended_action)
    """
    if not checks:
        return 0.0, "low", "approve"

    # Calculate average risk score
    total_risk_score = sum(check.score for check in checks) / len(checks)

    # Determine risk category and recommended action
    if total_risk_score < 0.3:
        risk_category = "low"
        recommended_action = "approve"
    elif total_risk_score < 0.7:
        risk_category = "medium"
        recommended_action = "manual_review"
    else:
        risk_category = "high"
        recommended_action = "reject"

    return total_risk_score, risk_category, recommended_action

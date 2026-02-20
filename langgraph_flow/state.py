from typing import Optional, Union, TypedDict, Dict, Any

from schemas.extraction_schema import (
    HealthClaimExtraction,
    MotorClaimExtraction,
    DeathClaimExtraction,
)

from schemas.validation_schema import ValidationOutput


# ============================================================
# Graph State Definition
# ============================================================

class ClaimState(TypedDict, total=False):
    """
    This represents the shared memory passed between LangGraph nodes.

    Every node receives this full state and returns partial updates.
    """

    # --------------------------------------------------------
    # INPUT SECTION (from API)
    # --------------------------------------------------------

    claim_type: str
    request_data: Dict[str, Any]
    documents: Dict[str, Any]

    # --------------------------------------------------------
    # EXTRACTION OUTPUT
    # --------------------------------------------------------

    extracted_entities: Optional[
        Union[
            HealthClaimExtraction,
            MotorClaimExtraction,
            DeathClaimExtraction,
        ]
    ]

    # --------------------------------------------------------
    # VALIDATION OUTPUT
    # --------------------------------------------------------

    validation_results: Optional[ValidationOutput]

    # --------------------------------------------------------
    # AGGREGATED SCORES
    # --------------------------------------------------------

    total_risk_score: Optional[float]

    # --------------------------------------------------------
    # FUTURE NODES (Fraud / Payout / Decision Engine)
    # --------------------------------------------------------

    fraud_score: Optional[float]
    payout_prediction: Optional[float]
    final_decision: Optional[str]
from pydantic import BaseModel
from typing import Optional, Union

from schemas.extraction_schema import (
    HealthClaimExtraction,
    MotorClaimExtraction,
    DeathClaimExtraction,
)
from schemas.validation_schema import ValidationOutput


# ============================================================
# Final API Response
# ============================================================

class ClaimProcessingResponse(BaseModel):
    """
    Final structured response returned to client.
    """

    claim_type: str

    extracted_data: Optional[
        Union[
            HealthClaimExtraction,
            MotorClaimExtraction,
            DeathClaimExtraction,
        ]
    ] = None

    validation_result: Optional[ValidationOutput] = None

    # Optional overall status (useful later)
    status: Optional[str] = None
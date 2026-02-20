from datetime import date
from typing import Optional

from schemas.extraction_schema import (
    DeathClaimFormExtraction,
    PersonName,
)


# ============================================================
# Death Claim Form Extractor
# ============================================================

class DeathClaimFormExtractor:
    """
    Extracts structured data from a Death Claim Form.

    Current version:
    - Accepts file path
    - Simulates model API call
    - Returns hardcoded structured output

    Future version:
    - OCR + LLM extraction
    - Structured JSON parsing
    """

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint


    # --------------------------------------------------------
    # Public Method
    # --------------------------------------------------------

    def extract(self, file_path: str) -> DeathClaimFormExtraction:
        model_output = self._call_model_api(file_path)
        structured_output = self._map_to_schema(model_output)
        return structured_output


    # --------------------------------------------------------
    # Simulated Model API Call
    # --------------------------------------------------------

    def _call_model_api(self, file_path: str) -> dict:
        print(f"[DeathClaimFormExtractor] Sending file to model API: {file_path}")

        return {
            "policy_number": "LIFE-556677",
            "claim_number": "DTH-2024-001",
            "deceased_first_name": "Suresh",
            "deceased_last_name": "Patil",
            "nominee_first_name": "Anita",
            "nominee_last_name": "Patil",
            "date_of_death": "2024-02-05",
            "cause_of_death": "Cardiac Arrest",
            "claimed_amount": 500000.0,
        }


    # --------------------------------------------------------
    # Map Model Output to Schema
    # --------------------------------------------------------

    def _map_to_schema(self, model_output: dict) -> DeathClaimFormExtraction:

        try:
            date_of_death = date.fromisoformat(model_output["date_of_death"])
        except Exception:
            date_of_death = None

        return DeathClaimFormExtraction(
            policy_number=model_output.get("policy_number"),
            claim_number=model_output.get("claim_number"),
            deceased_name=PersonName(
                first_name=model_output.get("deceased_first_name"),
                last_name=model_output.get("deceased_last_name"),
            ),
            nominee_name=PersonName(
                first_name=model_output.get("nominee_first_name"),
                last_name=model_output.get("nominee_last_name"),
            ),
            date_of_death=date_of_death,
            cause_of_death=model_output.get("cause_of_death"),
            claimed_amount=model_output.get("claimed_amount"),
        )
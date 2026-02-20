from datetime import date
from typing import Optional

from schemas.extraction_schema import (
    HealthClaimFormExtraction,
    PersonName,
)


# ============================================================
# Health Claim Form Extractor
# ============================================================

class HealthClaimFormExtractor:
    """
    Extracts structured data from a Health Claim Form.

    Current version:
    - Accepts file path
    - Simulates model API call
    - Returns hardcoded structured output

    Future version:
    - Convert PDF to text/image
    - Send to LLM / LayoutLM / Extraction API
    - Parse structured JSON response
    """

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint  # Placeholder for future API


    # --------------------------------------------------------
    # Public Extraction Method
    # --------------------------------------------------------

    def extract(self, file_path: str) -> HealthClaimFormExtraction:
        """
        Main method to extract structured data.
        """

        # 1️⃣ Simulate model API call
        model_output = self._call_model_api(file_path)

        # 2️⃣ Convert model output into schema
        structured_output = self._map_to_schema(model_output)

        return structured_output


    # --------------------------------------------------------
    # Simulated Model API Call (HARDCODED)
    # --------------------------------------------------------

    def _call_model_api(self, file_path: str) -> dict:
        """
        Simulates sending file to ML extraction model.
        Replace this later with real HTTP call.
        """

        print(f"[HealthClaimFormExtractor] Sending file to model API: {file_path}")

        # Hardcoded dummy model response
        return {
            "patient_first_name": "Rahul",
            "patient_last_name": "Sharma",
            "insured_first_name": "Rahul",
            "insured_last_name": "Sharma",
            "policy_number": "HLT-998877",
            "claim_number": "CLM-2024-0001",
            "date_of_admission": "2024-01-10",
            "date_of_discharge": "2024-01-15",
            "diagnosis": "Acute Appendicitis",
            "claimed_amount": 85000.0,
            "hospital_name": "City Care Hospital",
            "hospital_city": "Mumbai",
        }


    # --------------------------------------------------------
    # Map Model Output to Schema
    # --------------------------------------------------------

    def _map_to_schema(self, model_output: dict) -> HealthClaimFormExtraction:
        """
        Converts raw model JSON output into structured Pydantic schema.
        """

        # Safely parse dates
        try:
            admission_date = date.fromisoformat(model_output["date_of_admission"])
        except Exception:
            admission_date = None

        try:
            discharge_date = date.fromisoformat(model_output["date_of_discharge"])
        except Exception:
            discharge_date = None

        return HealthClaimFormExtraction(
            patient_name=PersonName(
                first_name=model_output.get("patient_first_name"),
                last_name=model_output.get("patient_last_name"),
            ),
            insured_name=PersonName(
                first_name=model_output.get("insured_first_name"),
                last_name=model_output.get("insured_last_name"),
            ),
            policy_number=model_output.get("policy_number"),
            claim_number=model_output.get("claim_number"),
            date_of_admission=admission_date,
            date_of_discharge=discharge_date,
            diagnosis=model_output.get("diagnosis"),
            claimed_amount=model_output.get("claimed_amount"),
            hospital_name=model_output.get("hospital_name"),
            hospital_city=model_output.get("hospital_city"),
        )
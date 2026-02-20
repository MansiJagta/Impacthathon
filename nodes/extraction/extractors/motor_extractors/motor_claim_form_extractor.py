from datetime import date
from typing import Optional

from schemas.extraction_schema import (
    MotorClaimFormExtraction,
    PersonName,
)


class MotorClaimFormExtractor:

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint

    def extract(self, file_path: str) -> MotorClaimFormExtraction:
        model_output = self._call_model_api(file_path)
        return self._map_to_schema(model_output)

    def _call_model_api(self, file_path: str) -> dict:
        print(f"[MotorClaimFormExtractor] Sending file to model API: {file_path}")

        return {
            "insured_first_name": "Amit",
            "insured_last_name": "Kulkarni",
            "policy_number": "MTR-445566",
            "claim_number": "MTR-CLM-001",
            "vehicle_registration_number": "MH12AB1234",
            "accident_date": "2024-03-01",
            "accident_location": "Pune Highway",
            "claimed_amount": 75000.0,
        }

    def _map_to_schema(self, model_output: dict) -> MotorClaimFormExtraction:

        try:
            accident_date = date.fromisoformat(model_output["accident_date"])
        except Exception:
            accident_date = None

        return MotorClaimFormExtraction(
            insured_name=PersonName(
                first_name=model_output.get("insured_first_name"),
                last_name=model_output.get("insured_last_name"),
            ),
            policy_number=model_output.get("policy_number"),
            claim_number=model_output.get("claim_number"),
            vehicle_registration_number=model_output.get("vehicle_registration_number"),
            accident_date=accident_date,
            accident_location=model_output.get("accident_location"),
            claimed_amount=model_output.get("claimed_amount"),
        )
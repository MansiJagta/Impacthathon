from datetime import date
from typing import Optional

from schemas.extraction_schema import (
    PolicyDocumentExtraction,
    PersonName,
)


class PolicyBondExtractor:

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint

    def extract(self, file_path: str) -> PolicyDocumentExtraction:
        model_output = self._call_model_api(file_path)
        return self._map_to_schema(model_output)

    def _call_model_api(self, file_path: str) -> dict:
        print(f"[PolicyBondExtractor] Sending file to model API: {file_path}")

        return {
            "policy_number": "LIFE-556677",
            "holder_first_name": "Suresh",
            "holder_last_name": "Patil",
            "policy_start_date": "2015-01-01",
            "policy_end_date": "2035-01-01",
            "sum_assured": 500000.0,
            "premium_amount": 25000.0,
        }

    def _map_to_schema(self, model_output: dict) -> PolicyDocumentExtraction:

        try:
            start_date = date.fromisoformat(model_output["policy_start_date"])
        except Exception:
            start_date = None

        try:
            end_date = date.fromisoformat(model_output["policy_end_date"])
        except Exception:
            end_date = None

        return PolicyDocumentExtraction(
            policy_number=model_output.get("policy_number"),
            policy_holder_name=PersonName(
                first_name=model_output.get("holder_first_name"),
                last_name=model_output.get("holder_last_name"),
            ),
            policy_start_date=start_date,
            policy_end_date=end_date,
            sum_assured=model_output.get("sum_assured"),
            premium_amount=model_output.get("premium_amount"),
        )
from datetime import datetime
from typing import Optional

from schemas.extraction_schema import (
    DrivingLicenseExtraction,
    PersonName,
)


class DrivingLicenseExtractor:

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint

    def extract(self, file_path: str) -> DrivingLicenseExtraction:
        model_output = self._call_model_api(file_path)
        return self._map_to_schema(model_output)

    def _call_model_api(self, file_path: str) -> dict:
        print(f"[DrivingLicenseExtractor] Sending file to model API: {file_path}")

        return {
            "dl_number": "MH1420180001234",
            "driver_first_name": "Amit",
            "driver_last_name": "Kulkarni",
            "date_of_birth": "1990-06-15",
            "issue_date": "2018-07-01",
            "expiry_date": "2038-07-01",
            "issuing_authority": "RTO Pune",
        }

    def _map_to_schema(self, model_output: dict) -> DrivingLicenseExtraction:

        def parse_date(field):
            value = model_output.get(field)
            if not value:
                return None
            try:
                return datetime.fromisoformat(value).date()
            except Exception:
                return None

        return DrivingLicenseExtraction(
            dl_number=model_output.get("dl_number"),
            driver_name=PersonName(
                first_name=model_output.get("driver_first_name"),
                last_name=model_output.get("driver_last_name"),
            ) if model_output.get("driver_first_name") else None,
            date_of_birth=parse_date("date_of_birth"),
            issue_date=parse_date("issue_date"),
            expiry_date=parse_date("expiry_date"),
            issuing_authority=model_output.get("issuing_authority"),
        )
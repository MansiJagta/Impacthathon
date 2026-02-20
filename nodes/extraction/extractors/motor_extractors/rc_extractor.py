from datetime import date
from typing import Optional

from schemas.extraction_schema import (
    RCExtraction,
    PersonName,
)


class RCExtractor:

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint

    def extract(self, file_path: str) -> RCExtraction:
        model_output = self._call_model_api(file_path)
        return self._map_to_schema(model_output)

    def _call_model_api(self, file_path: str) -> dict:
        print(f"[RCExtractor] Sending file to model API: {file_path}")

        return {
            "registration_number": "MH12AB1234",
            "owner_first_name": "Amit",
            "owner_last_name": "Kulkarni",
            "vehicle_model": "Swift Dzire",
            "vehicle_make": "Maruti Suzuki",
            "chassis_number": "CHS123456789",
            "engine_number": "ENG987654321",
            "registration_date": "2018-05-10",
        }

    def _map_to_schema(self, model_output: dict) -> RCExtraction:

        try:
            reg_date = date.fromisoformat(model_output["registration_date"])
        except Exception:
            reg_date = None

        return RCExtraction(
            registration_number=model_output.get("registration_number"),
            owner_name=PersonName(
                first_name=model_output.get("owner_first_name"),
                last_name=model_output.get("owner_last_name"),
            ),
            vehicle_model=model_output.get("vehicle_model"),
            vehicle_make=model_output.get("vehicle_make"),
            chassis_number=model_output.get("chassis_number"),
            engine_number=model_output.get("engine_number"),
            registration_date=reg_date,
        )
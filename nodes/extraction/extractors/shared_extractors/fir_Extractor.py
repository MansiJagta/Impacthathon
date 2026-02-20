from datetime import date
from typing import Optional

from schemas.extraction_schema import FIRExtraction


class FIRExtractor:

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint

    def extract(self, file_path: str) -> FIRExtraction:
        model_output = self._call_model_api(file_path)
        return self._map_to_schema(model_output)

    def _call_model_api(self, file_path: str) -> dict:
        print(f"[FIRExtractor] Sending file to model API: {file_path}")

        return {
            "fir_number": "FIR-778899",
            "police_station_name": "Shivaji Nagar Police Station",
            "fir_date": "2024-03-02",
            "accident_date": "2024-03-01",
            "accident_location": "Pune Highway",
            "complainant_name": "Amit Kulkarni",
        }

    def _map_to_schema(self, model_output: dict) -> FIRExtraction:

        try:
            fir_date = date.fromisoformat(model_output["fir_date"])
        except Exception:
            fir_date = None

        try:
            accident_date = date.fromisoformat(model_output["accident_date"])
        except Exception:
            accident_date = None

        return FIRExtraction(
            fir_number=model_output.get("fir_number"),
            police_station_name=model_output.get("police_station_name"),
            fir_date=fir_date,
            accident_date=accident_date,
            accident_location=model_output.get("accident_location"),
            complainant_name=model_output.get("complainant_name"),
        )
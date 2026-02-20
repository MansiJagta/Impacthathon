from datetime import date
from typing import Optional

from schemas.extraction_schema import HospitalRecordsExtraction


class HospitalRecordsExtractor:

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint

    def extract(self, file_path: str) -> HospitalRecordsExtraction:
        model_output = self._call_model_api(file_path)
        return self._map_to_schema(model_output)

    def _call_model_api(self, file_path: str) -> dict:
        print(f"[HospitalRecordsExtractor] Sending file to model API: {file_path}")

        return {
            "hospital_name": "City Care Hospital",
            "admission_date": "2024-01-28",
            "discharge_date": "2024-02-04",
            "diagnosis": "Severe Cardiac Complications",
            "treatment_summary": "Patient admitted with chest pain. Intensive cardiac care provided.",
        }

    def _map_to_schema(self, model_output: dict) -> HospitalRecordsExtraction:

        try:
            admission_date = date.fromisoformat(model_output["admission_date"])
        except Exception:
            admission_date = None

        try:
            discharge_date = date.fromisoformat(model_output["discharge_date"])
        except Exception:
            discharge_date = None

        return HospitalRecordsExtraction(
            hospital_name=model_output.get("hospital_name"),
            admission_date=admission_date,
            discharge_date=discharge_date,
            diagnosis=model_output.get("diagnosis"),
            treatment_summary=model_output.get("treatment_summary"),
        )
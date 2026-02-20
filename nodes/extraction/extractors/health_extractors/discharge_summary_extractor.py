from datetime import date
from typing import Optional

# Import extraction schema models
from schemas.extraction_schema import (
    DischargeSummaryExtraction,
    PersonName,
    HospitalInfo,
)


# ============================================================
# Discharge Summary Extractor
# ============================================================

class DischargeSummaryExtractor:
    """
    Extracts structured data from a discharge summary document.

    Current version:
    - Accepts file path
    - Simulates model API call
    - Returns hardcoded structured output

    Future version:
    - Convert PDF to text / image
    - Send to LLM / LayoutLM / OCR API
    - Parse structured JSON response
    """

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint  # Placeholder for future model API


    # --------------------------------------------------------
    # Public Method
    # --------------------------------------------------------

    def extract(self, file_path: str) -> DischargeSummaryExtraction:
        """
        Main extraction method.
        """

        # 1️⃣ Simulate sending file to model
        model_output = self._call_model_api(file_path)

        # 2️⃣ Convert model output into schema
        structured_output = self._map_to_schema(model_output)

        return structured_output


    # --------------------------------------------------------
    # Simulated Model Call (HARDCODED FOR NOW)
    # --------------------------------------------------------

    def _call_model_api(self, file_path: str) -> dict:
        """
        Simulates sending the file to an external ML model API.
        Replace this with real HTTP call later.
        """

        print(f"[DischargeSummaryExtractor] Sending file to model API: {file_path}")

        # Hardcoded dummy model response
        return {
            "patient_first_name": "Rahul",
            "patient_last_name": "Sharma",
            "hospital_name": "City Care Hospital",
            "hospital_registration_number": "HOSP12345",
            "hospital_address": "MG Road, Mumbai",
            "admission_date": "2024-01-10",
            "discharge_date": "2024-01-15",
            "primary_diagnosis": "Acute Appendicitis",
            "secondary_diagnosis": "Mild Dehydration",
            "treatment_given": "Appendectomy performed successfully.",
            "doctor_name": "Dr. Amit Mehra",
        }


    # --------------------------------------------------------
    # Map Model Output to Pydantic Schema
    # --------------------------------------------------------

    def _map_to_schema(self, model_output: dict) -> DischargeSummaryExtraction:
        """
        Converts raw model JSON output into structured schema object.
        """

        try:
            admission_date = date.fromisoformat(model_output["admission_date"])
        except Exception:
            admission_date = None

        try:
            discharge_date = date.fromisoformat(model_output["discharge_date"])
        except Exception:
            discharge_date = None

        return DischargeSummaryExtraction(
            patient_name=PersonName(
                first_name=model_output.get("patient_first_name"),
                last_name=model_output.get("patient_last_name"),
            ),
            hospital_info=HospitalInfo(
                hospital_name=model_output.get("hospital_name"),
                hospital_address=model_output.get("hospital_address"),
                hospital_registration_number=model_output.get(
                    "hospital_registration_number"
                ),
            ),
            admission_date=admission_date,
            discharge_date=discharge_date,
            primary_diagnosis=model_output.get("primary_diagnosis"),
            secondary_diagnosis=model_output.get("secondary_diagnosis"),
            treatment_given=model_output.get("treatment_given"),
            doctor_name=model_output.get("doctor_name"),
        )
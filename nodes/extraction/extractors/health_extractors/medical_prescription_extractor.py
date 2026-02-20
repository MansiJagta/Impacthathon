from datetime import date
from typing import Optional, List

from schemas.extraction_schema import (
    MedicalPrescriptionExtraction,
    PersonName,
)


# ============================================================
# Medical Prescription Extractor
# ============================================================

class MedicalPrescriptionExtractor:
    """
    Extracts structured data from a medical prescription document.

    Current version:
    - Accepts file path
    - Simulates model API call
    - Returns hardcoded structured output

    Future version:
    - OCR + LLM extraction
    - Structured JSON parsing
    """

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint  # Placeholder for future model API


    # --------------------------------------------------------
    # Public Extraction Method
    # --------------------------------------------------------

    def extract(self, file_path: str) -> MedicalPrescriptionExtraction:
        """
        Main extraction method.
        """

        # 1️⃣ Simulate model API call
        model_output = self._call_model_api(file_path)

        # 2️⃣ Map model output to schema
        structured_output = self._map_to_schema(model_output)

        return structured_output


    # --------------------------------------------------------
    # Simulated Model API Call (HARDCODED)
    # --------------------------------------------------------

    def _call_model_api(self, file_path: str) -> dict:
        """
        Simulates sending file to extraction model.
        Replace with real HTTP request later.
        """

        print(f"[MedicalPrescriptionExtractor] Sending file to model API: {file_path}")

        # Dummy response
        return {
            "patient_first_name": "Rahul",
            "patient_last_name": "Sharma",
            "doctor_name": "Dr. Amit Mehra",
            "prescription_date": "2024-01-12",
            "medicines_list": [
                "Amoxicillin 500mg",
                "Paracetamol 650mg",
                "Pantoprazole 40mg"
            ]
        }


    # --------------------------------------------------------
    # Map Model Output to Schema
    # --------------------------------------------------------

    def _map_to_schema(self, model_output: dict) -> MedicalPrescriptionExtraction:
        """
        Converts raw model output into structured Pydantic schema.
        """

        # Safe date parsing
        try:
            prescription_date = date.fromisoformat(
                model_output["prescription_date"]
            )
        except Exception:
            prescription_date = None

        return MedicalPrescriptionExtraction(
            patient_name=PersonName(
                first_name=model_output.get("patient_first_name"),
                last_name=model_output.get("patient_last_name"),
            ),
            doctor_name=model_output.get("doctor_name"),
            prescription_date=prescription_date,
            medicines_list=model_output.get("medicines_list"),
        )
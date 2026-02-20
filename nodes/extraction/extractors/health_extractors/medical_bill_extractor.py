from datetime import date
from typing import Optional

from schemas.extraction_schema import (
    HospitalBillExtraction,
    PersonName,
)


# ============================================================
# Hospital Bill Extractor
# ============================================================

class MedicalBillExtractor:
    """
    Extracts structured data from a hospital bill document.

    Current version:
    - Accepts file path
    - Simulates model API call
    - Returns hardcoded structured output

    Future version:
    - OCR + LLM extraction
    - Structured JSON parsing
    """

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint  # Placeholder for future API


    # --------------------------------------------------------
    # Public Extraction Method
    # --------------------------------------------------------

    def extract(self, file_path: str) -> HospitalBillExtraction:
        """
        Main extraction method.
        """

        # 1️⃣ Simulate model call
        model_output = self._call_model_api(file_path)

        # 2️⃣ Map to schema
        structured_output = self._map_to_schema(model_output)

        return structured_output


    # --------------------------------------------------------
    # Simulated Model API Call (HARDCODED)
    # --------------------------------------------------------

    def _call_model_api(self, file_path: str) -> dict:
        """
        Simulates sending the file to a model API.
        Replace this with real HTTP call later.
        """

        print(f"[MedicalBillExtractor] Sending file to model API: {file_path}")

        # Dummy model output
        return {
            "bill_number": "BILL-2024-7788",
            "bill_date": "2024-01-15",
            "hospital_name": "City Care Hospital",
            "patient_first_name": "Rahul",
            "patient_last_name": "Sharma",
            "total_bill_amount": 92000.0,
            "gst_number": "27ABCDE1234F1Z5",
        }


    # --------------------------------------------------------
    # Map Model Output to Schema
    # --------------------------------------------------------

    def _map_to_schema(self, model_output: dict) -> HospitalBillExtraction:
        """
        Converts raw model output to structured Pydantic schema.
        """

        # Safe date parsing
        try:
            bill_date = date.fromisoformat(model_output["bill_date"])
        except Exception:
            bill_date = None

        return HospitalBillExtraction(
            bill_number=model_output.get("bill_number"),
            bill_date=bill_date,
            hospital_name=model_output.get("hospital_name"),
            patient_name=PersonName(
                first_name=model_output.get("patient_first_name"),
                last_name=model_output.get("patient_last_name"),
            ),
            total_bill_amount=model_output.get("total_bill_amount"),
            gst_number=model_output.get("gst_number"),
        )
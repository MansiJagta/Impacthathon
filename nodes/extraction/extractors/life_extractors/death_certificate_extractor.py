from datetime import date
from typing import Optional

from schemas.extraction_schema import (
    DeathCertificateExtraction,
    PersonName,
)


# ============================================================
# Death Certificate Extractor
# ============================================================

class DeathCertificateExtractor:
    """
    Extracts structured data from a Death Certificate.

    Current version:
    - Accepts file path
    - Simulates model API call
    - Returns hardcoded structured output
    """

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint


    # --------------------------------------------------------
    # Public Method
    # --------------------------------------------------------

    def extract(self, file_path: str) -> DeathCertificateExtraction:
        model_output = self._call_model_api(file_path)
        structured_output = self._map_to_schema(model_output)
        return structured_output


    # --------------------------------------------------------
    # Simulated Model API Call
    # --------------------------------------------------------

    def _call_model_api(self, file_path: str) -> dict:
        print(f"[DeathCertificateExtractor] Sending file to model API: {file_path}")

        return {
            "certificate_number": "DC-998877",
            "deceased_first_name": "Suresh",
            "deceased_last_name": "Patil",
            "date_of_birth": "1968-06-15",
            "date_of_death": "2024-02-05",
            "place_of_death": "Mumbai",
            "cause_of_death": "Cardiac Arrest",
            "issuing_authority": "Municipal Corporation of Greater Mumbai",
        }


    # --------------------------------------------------------
    # Map Model Output to Schema
    # --------------------------------------------------------

    def _map_to_schema(self, model_output: dict) -> DeathCertificateExtraction:

        try:
            dob = date.fromisoformat(model_output["date_of_birth"])
        except Exception:
            dob = None

        try:
            dod = date.fromisoformat(model_output["date_of_death"])
        except Exception:
            dod = None

        return DeathCertificateExtraction(
            certificate_number=model_output.get("certificate_number"),
            deceased_name=PersonName(
                first_name=model_output.get("deceased_first_name"),
                last_name=model_output.get("deceased_last_name"),
            ),
            date_of_birth=dob,
            date_of_death=dod,
            place_of_death=model_output.get("place_of_death"),
            cause_of_death=model_output.get("cause_of_death"),
            issuing_authority=model_output.get("issuing_authority"),
        )
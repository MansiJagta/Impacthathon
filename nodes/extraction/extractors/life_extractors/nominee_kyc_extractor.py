from typing import Optional

from schemas.extraction_schema import (
    NomineeKYCExtraction,
    PersonName,
)


class NomineeKYCExtractor:

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint

    def extract(self, file_path: str) -> NomineeKYCExtraction:
        model_output = self._call_model_api(file_path)
        return self._map_to_schema(model_output)

    def _call_model_api(self, file_path: str) -> dict:
        print(f"[NomineeKYCExtractor] Sending file to model API: {file_path}")

        return {
            "nominee_first_name": "Anita",
            "nominee_last_name": "Patil",
            "id_number": "ABCDE1234F",
            "relationship_with_deceased": "Spouse",
            "bank_account_number": "123456789012",
            "bank_ifsc": "HDFC0001234",
        }

    def _map_to_schema(self, model_output: dict) -> NomineeKYCExtraction:

        return NomineeKYCExtraction(
            nominee_name=PersonName(
                first_name=model_output.get("nominee_first_name"),
                last_name=model_output.get("nominee_last_name"),
            ),
            id_number=model_output.get("id_number"),
            relationship_with_deceased=model_output.get("relationship_with_deceased"),
            bank_account_number=model_output.get("bank_account_number"),
            bank_ifsc=model_output.get("bank_ifsc"),
        )
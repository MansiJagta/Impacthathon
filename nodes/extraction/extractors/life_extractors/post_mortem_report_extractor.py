from datetime import date
from typing import Optional

from schemas.extraction_schema import (
    PostMortemExtraction,
    PersonName,
)


class PostMortemReportExtractor:

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint

    def extract(self, file_path: str) -> PostMortemExtraction:
        model_output = self._call_model_api(file_path)
        return self._map_to_schema(model_output)

    def _call_model_api(self, file_path: str) -> dict:
        print(f"[PostMortemReportExtractor] Sending file to model API: {file_path}")

        return {
            "report_number": "PMR-334455",
            "deceased_first_name": "Suresh",
            "deceased_last_name": "Patil",
            "post_mortem_date": "2024-02-06",
            "cause_of_death": "Myocardial Infarction",
            "place_of_examination": "Government Medical College, Mumbai",
        }

    def _map_to_schema(self, model_output: dict) -> PostMortemExtraction:

        try:
            pm_date = date.fromisoformat(model_output["post_mortem_date"])
        except Exception:
            pm_date = None

        return PostMortemExtraction(
            report_number=model_output.get("report_number"),
            deceased_name=PersonName(
                first_name=model_output.get("deceased_first_name"),
                last_name=model_output.get("deceased_last_name"),
            ),
            post_mortem_date=pm_date,
            cause_of_death=model_output.get("cause_of_death"),
            place_of_examination=model_output.get("place_of_examination"),
        )
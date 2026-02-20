from datetime import date
from typing import Optional

from schemas.extraction_schema import RepairBillExtraction


class RepairBillExtractor:

    def __init__(self, model_endpoint: Optional[str] = None):
        self.model_endpoint = model_endpoint

    def extract(self, file_path: str) -> RepairBillExtraction:
        model_output = self._call_model_api(file_path)
        return self._map_to_schema(model_output)

    def _call_model_api(self, file_path: str) -> dict:
        print(f"[RepairBillExtractor] Sending file to model API: {file_path}")

        return {
            "garage_name": "AutoFix Garage",
            "estimate_number": "EST-4455",
            "bill_date": "2024-03-05",
            "total_estimated_amount": 70000.0,
            "final_amount": 73000.0,
            "gst_number": "27ABCDE1234F1Z5",
        }

    def _map_to_schema(self, model_output: dict) -> RepairBillExtraction:

        try:
            bill_date = date.fromisoformat(model_output["bill_date"])
        except Exception:
            bill_date = None

        return RepairBillExtraction(
            garage_name=model_output.get("garage_name"),
            estimate_number=model_output.get("estimate_number"),
            bill_date=bill_date,
            total_estimated_amount=model_output.get("total_estimated_amount"),
            final_amount=model_output.get("final_amount"),
            gst_number=model_output.get("gst_number"),
        )
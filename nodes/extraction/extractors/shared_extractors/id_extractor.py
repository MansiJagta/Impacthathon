from datetime import datetime
from nodes.extraction.services.id_api_service import IdAPIService

from schemas.extraction_schema import (
    IDProofExtraction,
    PersonName,
    Address,
)


class IdExtractor:

    def extract(self, file_path: str) -> IDProofExtraction:
        api_response = IdAPIService().extract(file_path)

        # Default values
        id_type = None
        id_number = None
        name = None
        dob = None
        address = None

        # Safe date parser (handles multiple formats)
        def parse_date(date_str):
            if not date_str:
                return None
            for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
                try:
                    return datetime.strptime(date_str, fmt).date()
                except Exception:
                    continue
            return None

        # ----------------------------
        # PAN
        # ----------------------------
        if "PAN" in api_response:
            id_type = "PAN"
            id_number = api_response.get("PAN")
            name = api_response.get("Name")
            dob = parse_date(api_response.get("DOB"))

        # ----------------------------
        # Aadhaar
        # ----------------------------
        elif "Aadhaar" in api_response:
            id_type = "AADHAAR"
            id_number = api_response.get("Aadhaar")
            name = api_response.get("Name")
            dob = parse_date(api_response.get("DOB"))

            address_text = api_response.get("Address")
            if address_text:
                address = Address(address_line=address_text)

        # ----------------------------
        # Driving License (Handled separately normally)
        # ----------------------------
        elif "DL No" in api_response:
            id_type = "DRIVING_LICENSE"
            id_number = api_response.get("DL No")
            name = api_response.get("Name")
            dob = parse_date(api_response.get("DOB"))

        # Always return full schema (with None defaults)
        return IDProofExtraction(
            id_type=id_type,
            id_number=id_number,
            name_on_id=PersonName(first_name=name) if name else None,
            date_of_birth=dob,
            address=address,
        )
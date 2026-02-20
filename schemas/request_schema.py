from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal


# ---------------------------------------------------
# Base Document Model
# ---------------------------------------------------

class DocumentInput(BaseModel):
    """
    Represents a single uploaded document.
    Can contain:
    - file_path (if already stored)
    - base64 content (if sent inline)
    - metadata
    """
    filename: str
    content_type: Optional[str] = None
    file_path: Optional[str] = None
    base64_content: Optional[str] = None


# ---------------------------------------------------
# Health Claim Documents
# ---------------------------------------------------

class HealthClaimDocuments(BaseModel):
    claim_form: Optional[DocumentInput] = None
    id_proof: Optional[DocumentInput] = None
    discharge_summary: Optional[DocumentInput] = None
    hospital_bills: Optional[DocumentInput] = None
    medical_prescriptions: Optional[DocumentInput] = None


# ---------------------------------------------------
# Motor Claim Documents
# ---------------------------------------------------

class MotorClaimDocuments(BaseModel):
    claim_form: Optional[DocumentInput] = None
    id_proof: Optional[DocumentInput] = None
    fir: Optional[DocumentInput] = None
    rc: Optional[DocumentInput] = None
    driving_license: Optional[DocumentInput] = None
    repair_estimate_or_final_bill: Optional[DocumentInput] = None


# ---------------------------------------------------
# Death Claim Documents
# ---------------------------------------------------

class DeathClaimDocuments(BaseModel):
    death_claim_form: Optional[DocumentInput] = None
    death_certificate: Optional[DocumentInput] = None
    policy_document: Optional[DocumentInput] = None
    hospital_records: Optional[DocumentInput] = None
    post_mortem_report: Optional[DocumentInput] = None
    fir: Optional[DocumentInput] = None
    nominee_kyc_bank_details: Optional[DocumentInput] = None


# ---------------------------------------------------
# Main Claim Request
# ---------------------------------------------------

class ClaimRequest(BaseModel):
    claim_type: Literal["health", "motor", "death"]

    # Only ONE of these will be populated depending on claim_type
    health_documents: Optional[HealthClaimDocuments] = None
    motor_documents: Optional[MotorClaimDocuments] = None
    death_documents: Optional[DeathClaimDocuments] = None

    # Optional future fields
    policy_number: Optional[str] = None
    claim_id: Optional[str] = None


    # ---------------------------------------------------
    # Validator to enforce correct document block
    # ---------------------------------------------------

    @model_validator(mode="after")
    def validate_documents_by_claim_type(self):

        if self.claim_type == "health":
            if not self.health_documents:
                raise ValueError("health_documents must be provided for health claim")
            if self.motor_documents or self.death_documents:
                raise ValueError("Only health_documents allowed for health claim")

        elif self.claim_type == "motor":
            if not self.motor_documents:
                raise ValueError("motor_documents must be provided for motor claim")
            if self.health_documents or self.death_documents:
                raise ValueError("Only motor_documents allowed for motor claim")

        elif self.claim_type == "death":
            if not self.death_documents:
                raise ValueError("death_documents must be provided for death claim")
            if self.health_documents or self.motor_documents:
                raise ValueError("Only death_documents allowed for death claim")

        return self
from pydantic import BaseModel
from typing import Optional, List
from datetime import date


# ============================================================
# -------------------- COMMON REUSABLE -----------------------
# ============================================================

class PersonName(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None


class Address(BaseModel):
    address_line: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None


class HospitalInfo(BaseModel):
    hospital_name: Optional[str] = None
    hospital_address: Optional[str] = None
    hospital_registration_number: Optional[str] = None


class MoneyField(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = "INR"


# ============================================================
# ======================= HEALTH CLAIM =======================
# ============================================================

# -------- Claim Form --------
class HealthClaimFormExtraction(BaseModel):
    patient_name: Optional[PersonName] = None
    insured_name: Optional[PersonName] = None
    policy_number: Optional[str] = None
    claim_number: Optional[str] = None
    date_of_admission: Optional[date] = None
    date_of_discharge: Optional[date] = None
    diagnosis: Optional[str] = None
    claimed_amount: Optional[float] = None
    hospital_name: Optional[str] = None
    hospital_city: Optional[str] = None


# -------- ID Proof --------
class IDProofExtraction(BaseModel):
    id_type: Optional[str] = None  # Aadhaar, PAN, Passport
    id_number: Optional[str] = None
    name_on_id: Optional[PersonName] = None
    date_of_birth: Optional[date] = None
    address: Optional[Address] = None


# -------- Discharge Summary --------
class DischargeSummaryExtraction(BaseModel):
    patient_name: Optional[PersonName] = None
    hospital_info: Optional[HospitalInfo] = None
    admission_date: Optional[date] = None
    discharge_date: Optional[date] = None
    primary_diagnosis: Optional[str] = None
    secondary_diagnosis: Optional[str] = None
    treatment_given: Optional[str] = None
    doctor_name: Optional[str] = None


# -------- Hospital Bills --------
class HospitalBillExtraction(BaseModel):
    bill_number: Optional[str] = None
    bill_date: Optional[date] = None
    hospital_name: Optional[str] = None
    patient_name: Optional[PersonName] = None
    total_bill_amount: Optional[float] = None
    gst_number: Optional[str] = None


# -------- Medical Prescription --------
class MedicalPrescriptionExtraction(BaseModel):
    patient_name: Optional[PersonName] = None
    doctor_name: Optional[str] = None
    prescription_date: Optional[date] = None
    medicines_list: Optional[List[str]] = None


# -------- Final Health Claim Output --------
class HealthClaimExtraction(BaseModel):
    claim_form: Optional[HealthClaimFormExtraction] = None
    id_proof: Optional[IDProofExtraction] = None
    discharge_summary: Optional[DischargeSummaryExtraction] = None
    hospital_bills: Optional[HospitalBillExtraction] = None
    medical_prescriptions: Optional[MedicalPrescriptionExtraction] = None


# ============================================================
# ======================= MOTOR CLAIM ========================
# ============================================================

# -------- Motor Claim Form --------
class MotorClaimFormExtraction(BaseModel):
    insured_name: Optional[PersonName] = None
    policy_number: Optional[str] = None
    claim_number: Optional[str] = None
    vehicle_registration_number: Optional[str] = None
    accident_date: Optional[date] = None
    accident_location: Optional[str] = None
    claimed_amount: Optional[float] = None


# -------- FIR --------
class FIRExtraction(BaseModel):
    fir_number: Optional[str] = None
    police_station_name: Optional[str] = None
    fir_date: Optional[date] = None
    accident_date: Optional[date] = None
    accident_location: Optional[str] = None
    complainant_name: Optional[str] = None


# -------- RC --------
class RCExtraction(BaseModel):
    registration_number: Optional[str] = None
    owner_name: Optional[PersonName] = None
    vehicle_model: Optional[str] = None
    vehicle_make: Optional[str] = None
    chassis_number: Optional[str] = None
    engine_number: Optional[str] = None
    registration_date: Optional[date] = None


# -------- Driving License --------
class DrivingLicenseExtraction(BaseModel):
    dl_number: Optional[str] = None
    driver_name: Optional[PersonName] = None
    date_of_birth: Optional[date] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    issuing_authority: Optional[str] = None


# -------- Repair Estimate / Final Bill --------
class RepairBillExtraction(BaseModel):
    garage_name: Optional[str] = None
    estimate_number: Optional[str] = None
    bill_date: Optional[date] = None
    total_estimated_amount: Optional[float] = None
    final_amount: Optional[float] = None
    gst_number: Optional[str] = None


# -------- Final Motor Claim Output --------
class MotorClaimExtraction(BaseModel):
    claim_form: Optional[MotorClaimFormExtraction] = None
    id_proof: Optional[IDProofExtraction] = None
    fir: Optional[FIRExtraction] = None
    rc: Optional[RCExtraction] = None
    driving_license: Optional[DrivingLicenseExtraction] = None
    repair_estimate_or_final_bill: Optional[RepairBillExtraction] = None


# ============================================================
# ======================= DEATH CLAIM ========================
# ============================================================

# -------- Death Claim Form --------
class DeathClaimFormExtraction(BaseModel):
    policy_number: Optional[str] = None
    claim_number: Optional[str] = None
    deceased_name: Optional[PersonName] = None
    nominee_name: Optional[PersonName] = None
    date_of_death: Optional[date] = None
    cause_of_death: Optional[str] = None
    claimed_amount: Optional[float] = None


# -------- Death Certificate --------
class DeathCertificateExtraction(BaseModel):
    certificate_number: Optional[str] = None
    deceased_name: Optional[PersonName] = None
    date_of_birth: Optional[date] = None
    date_of_death: Optional[date] = None
    place_of_death: Optional[str] = None
    cause_of_death: Optional[str] = None
    issuing_authority: Optional[str] = None


# -------- Policy Document --------
class PolicyDocumentExtraction(BaseModel):
    policy_number: Optional[str] = None
    policy_holder_name: Optional[PersonName] = None
    policy_start_date: Optional[date] = None
    policy_end_date: Optional[date] = None
    sum_assured: Optional[float] = None
    premium_amount: Optional[float] = None


# -------- Hospital Records --------
class HospitalRecordsExtraction(BaseModel):
    hospital_name: Optional[str] = None
    admission_date: Optional[date] = None
    discharge_date: Optional[date] = None
    diagnosis: Optional[str] = None
    treatment_summary: Optional[str] = None


# -------- Post Mortem Report --------
class PostMortemExtraction(BaseModel):
    report_number: Optional[str] = None
    deceased_name: Optional[PersonName] = None
    post_mortem_date: Optional[date] = None
    cause_of_death: Optional[str] = None
    place_of_examination: Optional[str] = None


# -------- Nominee KYC --------
class NomineeKYCExtraction(BaseModel):
    nominee_name: Optional[PersonName] = None
    id_number: Optional[str] = None
    relationship_with_deceased: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_ifsc: Optional[str] = None


# -------- Final Death Claim Output --------
class DeathClaimExtraction(BaseModel):
    death_claim_form: Optional[DeathClaimFormExtraction] = None
    death_certificate: Optional[DeathCertificateExtraction] = None
    policy_document: Optional[PolicyDocumentExtraction] = None
    hospital_records: Optional[HospitalRecordsExtraction] = None
    post_mortem_report: Optional[PostMortemExtraction] = None
    fir: Optional[FIRExtraction] = None
    nominee_kyc_bank_details: Optional[NomineeKYCExtraction] = None
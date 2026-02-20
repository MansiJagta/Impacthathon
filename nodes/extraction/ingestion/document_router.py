from typing import Dict, Any

# Health Schemas
from schemas.extraction_schema import (
    HealthClaimExtraction,
    MotorClaimExtraction,
    DeathClaimExtraction,
)

from nodes.extraction.extractors.shared_extractors.id_extractor import IdExtractor

# ---------------- HEALTH ----------------
from nodes.extraction.extractors.health_extractors.health_claim_form_extractor import HealthClaimFormExtractor
from nodes.extraction.extractors.health_extractors.discharge_summary_extractor import DischargeSummaryExtractor
from nodes.extraction.extractors.health_extractors.medical_bill_extractor import MedicalBillExtractor
from nodes.extraction.extractors.health_extractors.medical_prescription_extractor import MedicalPrescriptionExtractor

# ---------------- MOTOR ----------------
from nodes.extraction.extractors.motor_extractors.motor_claim_form_extractor import MotorClaimFormExtractor
from nodes.extraction.extractors.motor_extractors.rc_extractor import RCExtractor
from nodes.extraction.extractors.motor_extractors.driving_license_extractor import DrivingLicenseExtractor
from nodes.extraction.extractors.motor_extractors.repair_bill_extractor import RepairBillExtractor

# ---------------- SHARED ----------------
from nodes.extraction.extractors.shared_extractors.fir_Extractor import FIRExtractor

# ---------------- LIFE / DEATH ----------------
from nodes.extraction.extractors.life_extractors.death_claim_form_extractor import DeathClaimFormExtractor
from nodes.extraction.extractors.life_extractors.death_certificate_extractor import DeathCertificateExtractor
from nodes.extraction.extractors.life_extractors.policy_bond_extractor import PolicyBondExtractor
from nodes.extraction.extractors.life_extractors.hospital_records_extractor import HospitalRecordsExtractor
from nodes.extraction.extractors.life_extractors.post_mortem_report_extractor import PostMortemReportExtractor
from nodes.extraction.extractors.life_extractors.nominee_kyc_extractor import NomineeKYCExtractor


class DocumentRouter:

    # ============================================================
    # Public Router Entry
    # ============================================================

    def route(self, claim_type: str, documents: Dict[str, Any]):

        if claim_type == "health":
            return self._handle_health(documents)

        elif claim_type == "motor":
            return self._handle_motor(documents)

        elif claim_type == "death":
            return self._handle_death(documents)

        else:
            raise ValueError(f"Unsupported claim type: {claim_type}")

    # ============================================================
    # HEALTH
    # ============================================================

    def _handle_health(self, documents: Dict[str, Any]) -> HealthClaimExtraction:

        return HealthClaimExtraction(
            claim_form=self._extract_if_present(
                HealthClaimFormExtractor(), documents.get("claim_form")
            ),
            id_proof=self._extract_if_present(
                IdExtractor(), documents.get("id_proof")
            ),  # ID handled separately if needed
            discharge_summary=self._extract_if_present(
                DischargeSummaryExtractor(), documents.get("discharge_summary")
            ),
            hospital_bills=self._extract_if_present(
                MedicalBillExtractor(), documents.get("hospital_bills")
            ),
            medical_prescriptions=self._extract_if_present(
                MedicalPrescriptionExtractor(), documents.get("medical_prescriptions")
            ),
        )

    # ============================================================
    # MOTOR
    # ============================================================

    def _handle_motor(self, documents: Dict[str, Any]) -> MotorClaimExtraction:

        return MotorClaimExtraction(
            claim_form=self._extract_if_present(
                MotorClaimFormExtractor(), documents.get("claim_form")
            ),
            id_proof=None,
            fir=self._extract_if_present(
                FIRExtractor(), documents.get("fir")
            ),
            rc=self._extract_if_present(
                RCExtractor(), documents.get("rc")
            ),
            driving_license=self._extract_if_present(
                DrivingLicenseExtractor(), documents.get("driving_license")
            ),
            repair_estimate_or_final_bill=self._extract_if_present(
                RepairBillExtractor(), documents.get("repair_estimate_or_final_bill")
            ),
        )

    # ============================================================
    # DEATH
    # ============================================================

    def _handle_death(self, documents: Dict[str, Any]) -> DeathClaimExtraction:

        return DeathClaimExtraction(
            death_claim_form=self._extract_if_present(
                DeathClaimFormExtractor(), documents.get("death_claim_form")
            ),
            death_certificate=self._extract_if_present(
                DeathCertificateExtractor(), documents.get("death_certificate")
            ),
            policy_document=self._extract_if_present(
                PolicyBondExtractor(), documents.get("policy_document")
            ),
            hospital_records=self._extract_if_present(
                HospitalRecordsExtractor(), documents.get("hospital_records")
            ),
            post_mortem_report=self._extract_if_present(
                PostMortemReportExtractor(), documents.get("post_mortem_report")
            ),
            fir=self._extract_if_present(
                FIRExtractor(), documents.get("fir")
            ),
            nominee_kyc_bank_details=self._extract_if_present(
                NomineeKYCExtractor(), documents.get("nominee_kyc_bank_details")
            ),
        )

    # ============================================================
    # Common Extraction Helper
    # ============================================================

    def _extract_if_present(self, extractor, document_input):

        if not document_input:
            return None

        file_path = document_input.get("file_path")
        if not file_path:
            return None

        return extractor.extract(file_path)
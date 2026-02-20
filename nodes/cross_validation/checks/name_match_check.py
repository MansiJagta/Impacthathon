from typing import List, Optional, Union
import difflib

from schemas.validation_schema import CheckResult
from schemas.extraction_schema import (
    HealthClaimExtraction,
    MotorClaimExtraction,
    DeathClaimExtraction,
    PersonName
)


class NameMatchCheck:
    """
    Performs fuzzy name matching across documents with 0.85 similarity threshold.
    - Similarity >= 0.85: score = 0 (pass)
    - Similarity 0.6-0.85: score = 0.4 (warning)
    - Similarity < 0.6: score = 0.9 (fail)
    """

    def run(self, extracted: Union[HealthClaimExtraction, MotorClaimExtraction, DeathClaimExtraction]) -> List[CheckResult]:
        """Execute name matching checks based on claim type."""
        checks = []

        if isinstance(extracted, HealthClaimExtraction):
            checks.extend(self._health_name_checks(extracted))
        elif isinstance(extracted, MotorClaimExtraction):
            checks.extend(self._motor_name_checks(extracted))
        elif isinstance(extracted, DeathClaimExtraction):
            checks.extend(self._death_name_checks(extracted))

        return [check for check in checks if check is not None]

    @staticmethod
    def _construct_full_name(person_name: Optional[PersonName]) -> Optional[str]:
        """Construct full name from PersonName object."""
        if not person_name:
            return None

        # Handle case where person_name might be a dict
        if isinstance(person_name, dict):
            first = person_name.get("first_name", "").strip() if person_name.get("first_name") else ""
            middle = person_name.get("middle_name", "").strip() if person_name.get("middle_name") else ""
            last = person_name.get("last_name", "").strip() if person_name.get("last_name") else ""
        else:
            first = person_name.first_name.strip() if person_name.first_name else ""
            middle = person_name.middle_name.strip() if person_name.middle_name else ""
            last = person_name.last_name.strip() if person_name.last_name else ""

        parts = [part for part in [first, middle, last] if part]
        return " ".join(parts) if parts else None

    @staticmethod
    def _calculate_similarity(name1: Optional[str], name2: Optional[str]) -> float:
        """Calculate similarity between two names using case-insensitive comparison."""
        if not name1 or not name2:
            return 0.0

        name1_clean = name1.lower().strip()
        name2_clean = name2.lower().strip()

        if name1_clean == name2_clean:
            return 1.0

        return difflib.SequenceMatcher(None, name1_clean, name2_clean).ratio()

    @staticmethod
    def _create_name_check_result(check_name: str, name1: Optional[str], name2: Optional[str],
                                 description: str) -> Optional[CheckResult]:
        """Create name check result with similarity scoring."""
        if not name1 or not name2:
            return None

        similarity = NameMatchCheck._calculate_similarity(name1, name2)

        if similarity >= 0.85:
            score = 0.0
            status = "pass"
        elif similarity >= 0.6:
            score = 0.4
            status = "warning"
        else:
            score = 0.9
            status = "fail"

        return CheckResult(
            check_name=check_name,
            check_type="identity",
            score=score,
            confidence=similarity,
            status=status,
            message=f"{description}: {similarity:.2f} similarity between '{name1}' and '{name2}'",
            metadata={
                "compared_names": [name1, name2],
                "similarity_score": similarity
            }
        )

    def _health_name_checks(self, extracted: HealthClaimExtraction) -> List[Optional[CheckResult]]:
        """Run health claim specific name checks."""
        checks = []

        # Get names from different documents
        claim_form = extracted.claim_form if extracted.claim_form else None
        discharge_summary = extracted.discharge_summary if extracted.discharge_summary else None
        hospital_bills = extracted.hospital_bills if extracted.hospital_bills else None
        id_proof = extracted.id_proof if extracted.id_proof else None

        # claim_form.patient_name ≈ discharge_summary.patient_name
        if claim_form and discharge_summary:
            patient_name_claim = self._construct_full_name(claim_form.patient_name)
            patient_name_discharge = self._construct_full_name(discharge_summary.patient_name)
            checks.append(self._create_name_check_result(
                "patient_name_claim_vs_discharge",
                patient_name_claim,
                patient_name_discharge,
                "Patient name in claim form vs discharge summary"
            ))

        # claim_form.patient_name ≈ hospital_bills.patient_name
        if claim_form and hospital_bills:
            patient_name_claim = self._construct_full_name(claim_form.patient_name)
            patient_name_bill = self._construct_full_name(hospital_bills.patient_name)
            checks.append(self._create_name_check_result(
                "patient_name_claim_vs_bill",
                patient_name_claim,
                patient_name_bill,
                "Patient name in claim form vs hospital bill"
            ))

        # id_proof.name_on_id ≈ claim_form.patient_name
        if id_proof and claim_form:
            id_name = self._construct_full_name(id_proof.name_on_id)
            patient_name = self._construct_full_name(claim_form.patient_name)
            checks.append(self._create_name_check_result(
                "id_proof_vs_patient_name",
                id_name,
                patient_name,
                "Name on ID proof vs patient name in claim form"
            ))

        return checks

    def _motor_name_checks(self, extracted: MotorClaimExtraction) -> List[Optional[CheckResult]]:
        """Run motor claim specific name checks."""
        checks = []

        claim_form = extracted.claim_form if extracted.claim_form else None
        rc = extracted.rc if extracted.rc else None
        driving_license = extracted.driving_license if extracted.driving_license else None
        fir = extracted.fir if extracted.fir else None
        id_proof = extracted.id_proof if extracted.id_proof else None

        # rc.owner_name ≈ claim_form.insured_name
        if rc and claim_form:
            owner_name = self._construct_full_name(rc.owner_name)
            insured_name = self._construct_full_name(claim_form.insured_name)
            checks.append(self._create_name_check_result(
                "rc_owner_vs_insured",
                owner_name,
                insured_name,
                "RC owner name vs insured name in claim form"
            ))

        # driving_license.driver_name ≈ FIR complainant_name
        if driving_license and fir:
            driver_name = self._construct_full_name(driving_license.driver_name)
            complainant_name = fir.complainant_name
            checks.append(self._create_name_check_result(
                "driver_vs_fir_complainant",
                driver_name,
                complainant_name,
                "Driver name vs FIR complainant name"
            ))

        # id_proof.name_on_id ≈ insured_name
        if id_proof and claim_form:
            id_name = self._construct_full_name(id_proof.name_on_id)
            insured_name = self._construct_full_name(claim_form.insured_name)
            checks.append(self._create_name_check_result(
                "id_proof_vs_insured",
                id_name,
                insured_name,
                "Name on ID proof vs insured name"
            ))

        return checks

    def _death_name_checks(self, extracted: DeathClaimExtraction) -> List[Optional[CheckResult]]:
        """Run death claim specific name checks."""
        checks = []

        death_claim_form = extracted.death_claim_form if extracted.death_claim_form else None
        death_certificate = extracted.death_certificate if extracted.death_certificate else None
        policy_document = extracted.policy_document if extracted.policy_document else None
        nominee_kyc = extracted.nominee_kyc_bank_details if extracted.nominee_kyc_bank_details else None

        # death_claim_form.deceased_name ≈ death_certificate.deceased_name
        if death_claim_form and death_certificate:
            deceased_name_form = self._construct_full_name(death_claim_form.deceased_name)
            deceased_name_cert = self._construct_full_name(death_certificate.deceased_name)
            checks.append(self._create_name_check_result(
                "deceased_name_form_vs_cert",
                deceased_name_form,
                deceased_name_cert,
                "Deceased name in claim form vs death certificate"
            ))

        # death_certificate.deceased_name ≈ policy_document.policy_holder_name
        if death_certificate and policy_document:
            deceased_name = self._construct_full_name(death_certificate.deceased_name)
            policy_holder_name = self._construct_full_name(policy_document.policy_holder_name)
            checks.append(self._create_name_check_result(
                "deceased_vs_policy_holder",
                deceased_name,
                policy_holder_name,
                "Deceased name vs policy holder name"
            ))

        # nominee_kyc.nominee_name ≈ death_claim_form.nominee_name
        if nominee_kyc and death_claim_form:
            nominee_name_kyc = self._construct_full_name(nominee_kyc.nominee_name)
            nominee_name_form = self._construct_full_name(death_claim_form.nominee_name)
            checks.append(self._create_name_check_result(
                "nominee_kyc_vs_claim_form",
                nominee_name_kyc,
                nominee_name_form,
                "Nominee name in KYC vs claim form"
            ))

        return checks

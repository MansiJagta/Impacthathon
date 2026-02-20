from typing import List, Optional, Union

from schemas.validation_schema import CheckResult
from schemas.extraction_schema import (
    HealthClaimExtraction,
    MotorClaimExtraction,
    DeathClaimExtraction
)


class ChronologyCheck:
    """
    Validates chronological consistency of dates across documents.
    
    Checks:
    - Date orderings within claim types
    - Dates within policy periods
    - License validity on event dates
    """

    def run(self, extracted: Union[HealthClaimExtraction, MotorClaimExtraction, DeathClaimExtraction]) -> List[CheckResult]:
        """Execute chronology checks based on claim type."""
        checks = []

        if isinstance(extracted, HealthClaimExtraction):
            checks.extend(self._health_chronology_checks(extracted))
        elif isinstance(extracted, MotorClaimExtraction):
            checks.extend(self._motor_chronology_checks(extracted))
        elif isinstance(extracted, DeathClaimExtraction):
            checks.extend(self._death_chronology_checks(extracted))

        return [check for check in checks if check is not None]

    def _health_chronology_checks(self, extracted: HealthClaimExtraction) -> List[Optional[CheckResult]]:
        """Run health claim chronology checks."""
        checks = []

        claim_form = extracted.claim_form if extracted.claim_form else None
        discharge_summary = extracted.discharge_summary if extracted.discharge_summary else None
        hospital_bills = extracted.hospital_bills if extracted.hospital_bills else None
        prescriptions = extracted.medical_prescriptions if extracted.medical_prescriptions else None

        # admission_date ≤ discharge_date
        if claim_form and claim_form.date_of_admission and claim_form.date_of_discharge:
            if claim_form.date_of_admission > claim_form.date_of_discharge:
                checks.append(CheckResult(
                    check_name="admission_discharge_chronology",
                    check_type="chronology",
                    score=0.8,
                    confidence=1.0,
                    status="fail",
                    message=f"Admission date ({claim_form.date_of_admission}) is after discharge date ({claim_form.date_of_discharge})"
                ))
            else:
                checks.append(CheckResult(
                    check_name="admission_discharge_chronology",
                    check_type="chronology",
                    score=0.0,
                    confidence=1.0,
                    status="pass",
                    message="Admission date is before or equal to discharge date"
                ))

        # bill_date ≥ admission_date
        if hospital_bills and hospital_bills.bill_date and claim_form and claim_form.date_of_admission:
            if hospital_bills.bill_date < claim_form.date_of_admission:
                checks.append(CheckResult(
                    check_name="bill_date_chronology",
                    check_type="chronology",
                    score=0.8,
                    confidence=1.0,
                    status="fail",
                    message=f"Bill date ({hospital_bills.bill_date}) is before admission date ({claim_form.date_of_admission})"
                ))
            else:
                checks.append(CheckResult(
                    check_name="bill_date_chronology",
                    check_type="chronology",
                    score=0.0,
                    confidence=1.0,
                    status="pass",
                    message="Bill date is after or on admission date"
                ))

        # prescription_date between admission and discharge
        if (prescriptions and prescriptions.prescription_date and
            claim_form and claim_form.date_of_admission and claim_form.date_of_discharge):
            if not (claim_form.date_of_admission <= prescriptions.prescription_date <= claim_form.date_of_discharge):
                checks.append(CheckResult(
                    check_name="prescription_date_chronology",
                    check_type="chronology",
                    score=0.8,
                    confidence=1.0,
                    status="fail",
                    message=f"Prescription date ({prescriptions.prescription_date}) is not between admission ({claim_form.date_of_admission}) and discharge ({claim_form.date_of_discharge})"
                ))
            else:
                checks.append(CheckResult(
                    check_name="prescription_date_chronology",
                    check_type="chronology",
                    score=0.0,
                    confidence=1.0,
                    status="pass",
                    message="Prescription date is within admission and discharge period"
                ))

        return checks

    def _motor_chronology_checks(self, extracted: MotorClaimExtraction) -> List[Optional[CheckResult]]:
        """Run motor claim chronology checks."""
        checks = []

        claim_form = extracted.claim_form if extracted.claim_form else None
        fir = extracted.fir if extracted.fir else None
        driving_license = extracted.driving_license if extracted.driving_license else None
        repair_bill = extracted.repair_estimate_or_final_bill if extracted.repair_estimate_or_final_bill else None

        # accident_date ≤ fir_date
        if claim_form and fir and claim_form.accident_date and fir.fir_date:
            if claim_form.accident_date > fir.fir_date:
                checks.append(CheckResult(
                    check_name="accident_fir_chronology",
                    check_type="chronology",
                    score=0.8,
                    confidence=1.0,
                    status="fail",
                    message=f"Accident date ({claim_form.accident_date}) is after FIR date ({fir.fir_date})"
                ))
            else:
                checks.append(CheckResult(
                    check_name="accident_fir_chronology",
                    check_type="chronology",
                    score=0.0,
                    confidence=1.0,
                    status="pass",
                    message="Accident date is before or equal to FIR date"
                ))

        # accident_date ≤ repair_bill_date
        if claim_form and repair_bill and claim_form.accident_date and repair_bill.bill_date:
            if claim_form.accident_date > repair_bill.bill_date:
                checks.append(CheckResult(
                    check_name="accident_repair_chronology",
                    check_type="chronology",
                    score=0.8,
                    confidence=1.0,
                    status="fail",
                    message=f"Accident date ({claim_form.accident_date}) is after repair bill date ({repair_bill.bill_date})"
                ))
            else:
                checks.append(CheckResult(
                    check_name="accident_repair_chronology",
                    check_type="chronology",
                    score=0.0,
                    confidence=1.0,
                    status="pass",
                    message="Accident date is before or equal to repair bill date"
                ))

        # driving_license.expiry_date > accident_date
        if driving_license and claim_form and driving_license.expiry_date and claim_form.accident_date:
            if driving_license.expiry_date <= claim_form.accident_date:
                checks.append(CheckResult(
                    check_name="license_validity_check",
                    check_type="chronology",
                    score=0.8,
                    confidence=1.0,
                    status="fail",
                    message=f"Driving license expired ({driving_license.expiry_date}) before accident date ({claim_form.accident_date})"
                ))
            else:
                checks.append(CheckResult(
                    check_name="license_validity_check",
                    check_type="chronology",
                    score=0.0,
                    confidence=1.0,
                    status="pass",
                    message="Driving license was valid during accident date"
                ))

        return checks

    def _death_chronology_checks(self, extracted: DeathClaimExtraction) -> List[Optional[CheckResult]]:
        """Run death claim chronology checks."""
        checks = []

        death_certificate = extracted.death_certificate if extracted.death_certificate else None
        post_mortem = extracted.post_mortem_report if extracted.post_mortem_report else None
        hospital_records = extracted.hospital_records if extracted.hospital_records else None
        policy_document = extracted.policy_document if extracted.policy_document else None

        # date_of_death within policy period
        if (death_certificate and policy_document and death_certificate.date_of_death and
            policy_document.policy_start_date and policy_document.policy_end_date):
            date_of_death = death_certificate.date_of_death
            if not (policy_document.policy_start_date <= date_of_death <= policy_document.policy_end_date):
                checks.append(CheckResult(
                    check_name="death_within_policy_period",
                    check_type="chronology",
                    score=0.8,
                    confidence=1.0,
                    status="fail",
                    message=f"Date of death ({date_of_death}) is not within policy period ({policy_document.policy_start_date} to {policy_document.policy_end_date})"
                ))
            else:
                checks.append(CheckResult(
                    check_name="death_within_policy_period",
                    check_type="chronology",
                    score=0.0,
                    confidence=1.0,
                    status="pass",
                    message="Date of death is within policy period"
                ))

        # post_mortem_date ≥ date_of_death
        if death_certificate and post_mortem and death_certificate.date_of_death and post_mortem.post_mortem_date:
            if post_mortem.post_mortem_date < death_certificate.date_of_death:
                checks.append(CheckResult(
                    check_name="postmortem_date_chronology",
                    check_type="chronology",
                    score=0.8,
                    confidence=1.0,
                    status="fail",
                    message=f"Post mortem date ({post_mortem.post_mortem_date}) is before date of death ({death_certificate.date_of_death})"
                ))
            else:
                checks.append(CheckResult(
                    check_name="postmortem_date_chronology",
                    check_type="chronology",
                    score=0.0,
                    confidence=1.0,
                    status="pass",
                    message="Post mortem date is after or on date of death"
                ))

        # hospital admission ≤ date_of_death
        if hospital_records and death_certificate and hospital_records.admission_date and death_certificate.date_of_death:
            if hospital_records.admission_date > death_certificate.date_of_death:
                checks.append(CheckResult(
                    check_name="hospital_admission_chronology",
                    check_type="chronology",
                    score=0.8,
                    confidence=1.0,
                    status="fail",
                    message=f"Hospital admission date ({hospital_records.admission_date}) is after date of death ({death_certificate.date_of_death})"
                ))
            else:
                checks.append(CheckResult(
                    check_name="hospital_admission_chronology",
                    check_type="chronology",
                    score=0.0,
                    confidence=1.0,
                    status="pass",
                    message="Hospital admission date is before or on date of death"
                ))

        return checks

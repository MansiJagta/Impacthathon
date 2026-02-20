from typing import List, Optional, Union

from schemas.validation_schema import CheckResult
from schemas.extraction_schema import (
    HealthClaimExtraction,
    MotorClaimExtraction,
    DeathClaimExtraction
)


class FinancialCheck:
    """
    Validates financial consistency across claim documents.
    
    Checks:
    - Claimed amounts do not exceed covered/insured amounts
    - Claimed amount matches sum assured (for death claims)
    """

    def run(self, extracted: Union[HealthClaimExtraction, MotorClaimExtraction, DeathClaimExtraction]) -> List[CheckResult]:
        """Execute financial checks based on claim type."""
        checks = []

        if isinstance(extracted, HealthClaimExtraction):
            checks.extend(self._health_financial_checks(extracted))
        elif isinstance(extracted, MotorClaimExtraction):
            checks.extend(self._motor_financial_checks(extracted))
        elif isinstance(extracted, DeathClaimExtraction):
            checks.extend(self._death_financial_checks(extracted))

        return [check for check in checks if check is not None]

    def _health_financial_checks(self, extracted: HealthClaimExtraction) -> List[Optional[CheckResult]]:
        """Run health claim financial checks."""
        checks = []

        claim_form = extracted.claim_form if extracted.claim_form else None
        hospital_bills = extracted.hospital_bills if extracted.hospital_bills else None

        # claimed_amount ≤ total_bill_amount
        if claim_form and hospital_bills and claim_form.claimed_amount and hospital_bills.total_bill_amount:
            if claim_form.claimed_amount > hospital_bills.total_bill_amount:
                checks.append(CheckResult(
                    check_name="claimed_vs_bill_amount",
                    check_type="financial",
                    score=0.85,
                    confidence=1.0,
                    status="fail",
                    message=f"Claimed amount ({claim_form.claimed_amount}) exceeds total bill amount ({hospital_bills.total_bill_amount})"
                ))
            else:
                checks.append(CheckResult(
                    check_name="claimed_vs_bill_amount",
                    check_type="financial",
                    score=0.0,
                    confidence=1.0,
                    status="pass",
                    message="Claimed amount is within bill amount"
                ))

        return checks

    def _motor_financial_checks(self, extracted: MotorClaimExtraction) -> List[Optional[CheckResult]]:
        """Run motor claim financial checks."""
        checks = []

        repair_bill = extracted.repair_estimate_or_final_bill if extracted.repair_estimate_or_final_bill else None

        # final_amount ≤ total_estimated_amount
        if (repair_bill and repair_bill.final_amount and repair_bill.total_estimated_amount):
            if repair_bill.final_amount > repair_bill.total_estimated_amount:
                checks.append(CheckResult(
                    check_name="final_vs_estimated_amount",
                    check_type="financial",
                    score=0.85,
                    confidence=1.0,
                    status="fail",
                    message=f"Final amount ({repair_bill.final_amount}) exceeds estimated amount ({repair_bill.total_estimated_amount})"
                ))
            else:
                checks.append(CheckResult(
                    check_name="final_vs_estimated_amount",
                    check_type="financial",
                    score=0.0,
                    confidence=1.0,
                    status="pass",
                    message="Final amount is within estimated amount"
                ))

        return checks

    def _death_financial_checks(self, extracted: DeathClaimExtraction) -> List[Optional[CheckResult]]:
        """Run death claim financial checks."""
        checks = []

        death_claim_form = extracted.death_claim_form if extracted.death_claim_form else None
        policy_document = extracted.policy_document if extracted.policy_document else None

        # claimed_amount == sum_assured
        if (death_claim_form and policy_document and
            death_claim_form.claimed_amount is not None and policy_document.sum_assured is not None):
            if abs(death_claim_form.claimed_amount - policy_document.sum_assured) > 0.01:  # Allow small floating point differences
                checks.append(CheckResult(
                    check_name="claimed_vs_sum_assured",
                    check_type="financial",
                    score=0.85,
                    confidence=1.0,
                    status="fail",
                    message=f"Claimed amount ({death_claim_form.claimed_amount}) does not match sum assured ({policy_document.sum_assured})"
                ))
            else:
                checks.append(CheckResult(
                    check_name="claimed_vs_sum_assured",
                    check_type="financial",
                    score=0.0,
                    confidence=1.0,
                    status="pass",
                    message="Claimed amount matches sum assured"
                ))

        return checks

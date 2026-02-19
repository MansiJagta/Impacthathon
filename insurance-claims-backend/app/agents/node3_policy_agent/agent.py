"""Main Node 3 implementation."""
# app/agents/node3_policy_agent/agent.py
from typing import Dict, Any, Optional
from datetime import datetime
from app.database.repositories.policy_repo import PolicyRepository
from app.models.policy import PolicyModel, CoverageAnalysis
from app.agents.node3_policy_agent.coverage_checker import CoverageChecker
from app.agents.node3_policy_agent.exclusion_checker import ExclusionChecker
from app.agents.node3_policy_agent.amount_calculator import AmountCalculator
from app.agents.node3_policy_agent.clause_extractor import ClauseExtractor

class PolicyCoverageAgent:
    """
    Node 3: Policy Coverage Agent
    Completely free implementation - NO token limits, NO paid APIs
    """
    
    def __init__(self):
        self.policy_repo = PolicyRepository()
        self.coverage_checker = CoverageChecker()
        self.exclusion_checker = ExclusionChecker()
        self.amount_calculator = AmountCalculator()
        self.clause_extractor = ClauseExtractor()
    
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for Node 3
        
        Expected input in state:
        - policy_number: str
        - claim_amount: float
        - incident_type: str
        - incident_date: str
        - incident_description: str
        
        Returns:
        - policy_analysis: CoverageAnalysis dict
        """
        
        # Extract from state
        policy_number = state.get("policy_number")
        claim_amount = state.get("claim_amount", 0)
        incident_type = state.get("incident_type", "")
        incident_date = state.get("incident_date", "")
        incident_description = state.get("incident_description", "")
        
        # Validate required fields
        if not policy_number:
            return self._error_response("Missing policy number")
        
        # STEP 1: Fetch policy from MongoDB
        policy_data = await self.policy_repo.find_by_policy_number(policy_number)
        
        if not policy_data:
            return self._error_response(f"Policy {policy_number} not found")
        
        # Convert to Pydantic model
        try:
            policy = PolicyModel(**policy_data)
        except Exception as e:
            return self._error_response(f"Invalid policy data: {str(e)}")
        
        # STEP 2: Check policy validity (active/expired)
        is_valid, validity_message = self._check_policy_validity(
            policy.effectiveDate,
            policy.expiryDate,
            incident_date
        )
        
        if not is_valid:
            return self._error_response(validity_message)
        
        # STEP 3: Validate coverage for incident type
        is_covered, coverage_confidence = self.coverage_checker.check_coverage(
            incident_type,
            policy.coverageDetails.model_dump()
        )
        
        # STEP 4: Check exclusions
        triggered_exclusions = self.exclusion_checker.check_exclusions(
            policy.exclusions,
            incident_description
        )
        
        # STEP 5: Calculate covered amount
        covered_amount = self.amount_calculator.calculate(
            claim_amount=claim_amount,
            policy_limit=policy.sumInsured,
            deductible=policy.coverageDetails.deductible,
            is_covered=is_covered,
            exclusions_triggered=triggered_exclusions
        )
        
        # STEP 6: Calculate coverage score
        coverage_score = self._calculate_coverage_score(
            is_valid=is_valid,
            is_covered=is_covered,
            exclusions_count=len(triggered_exclusions),
            within_limit=claim_amount <= policy.sumInsured
        )
        
        # STEP 7: Extract relevant clauses
        relevant_clauses = self.clause_extractor.extract(
            incident_type=incident_type,
            policy_type=policy.policyType
        )
        
        # STEP 8: Prepare final output
        analysis = CoverageAnalysis(
            policy_number=policy.policyNumber,
            is_covered=is_covered and len(triggered_exclusions) == 0,
            coverage_score=coverage_score,
            deductible=policy.coverageDetails.deductible,
            policy_limit=policy.sumInsured,
            covered_amount=covered_amount,
            exclusions_triggered=triggered_exclusions,
            relevant_clauses=relevant_clauses,
            policy_type=policy.policyType,
            holder_name=policy.holderName,
            confidence=0.99
        )
        
        return {"policy_analysis": analysis.model_dump()}
    
    def _check_policy_validity(self, effective_date, expiry_date, incident_date: str) -> tuple:
        """Check if policy was active on incident date"""
        try:
            # Parse dates (handle both datetime objects and ISO strings)
            effective = self._to_datetime(effective_date)
            expiry = self._to_datetime(expiry_date)
            incident = datetime.fromisoformat(incident_date.replace('Z', '+00:00'))
            
            if incident < effective:
                return False, f"Policy not effective yet (starts {effective.date()})"
            elif incident > expiry:
                return False, f"Policy expired on {expiry.date()}"
            else:
                return True, "Policy active"
        except Exception as e:
            return False, f"Date validation error: {str(e)}"

    def _to_datetime(self, value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        raise ValueError(f"Unsupported date type: {type(value)}")
    
    def _calculate_coverage_score(self, is_valid: bool, is_covered: bool,
                                  exclusions_count: int, within_limit: bool) -> float:
        """Calculate confidence score for coverage decision"""
        score = 0.0
        
        if is_valid:
            score += 0.2
        if is_covered:
            score += 0.5
        if exclusions_count == 0:
            score += 0.2
        if within_limit:
            score += 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _error_response(self, error_msg: str) -> Dict:
        """Return error response"""
        return {
            "policy_analysis": {
                "error": error_msg,
                "is_covered": False,
                "coverage_score": 0.0,
                "covered_amount": 0,
                "exclusions_triggered": [],
                "confidence": 1.0
            }
        }
"""Covered amount calculation."""
# app/agents/node3_policy_agent/amount_calculator.py
from typing import List

class AmountCalculator:
    """Simple amount calculator - NO ML needed"""
    
    def calculate(self, claim_amount: float, policy_limit: float,
                  deductible: int, is_covered: bool,
                  exclusions_triggered: List[str]) -> float:
        """
        Calculate final covered amount after limits and deductibles
        """
        if not is_covered or exclusions_triggered:
            return 0.0
        
        # Apply policy limit
        covered = min(claim_amount, policy_limit)
        
        # Apply deductible
        covered = max(0, covered - deductible)
        
        return round(covered, 2)
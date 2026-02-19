"""Coverage validation logic."""
# app/agents/node3_policy_agent/coverage_checker.py
from typing import Tuple

class CoverageChecker:
    """Simple rule-based coverage checker - NO ML NEEDED"""
    
    def __init__(self):
        # Simple mapping of incident types to coverage categories
        self.coverage_mapping = {
            "accident": "comprehensive",
            "collision": "comprehensive",
            "crash": "comprehensive",
            "theft": "comprehensive",
            "stolen": "comprehensive",
            "fire": "comprehensive",
            "third_party": "thirdParty",
            "liability": "thirdParty",
            "injury": "personalAccident",
            "hurt": "personalAccident"
        }
    
    def check_coverage(self, incident_type: str, coverage_details: dict) -> Tuple[bool, float]:
        """
        Check if incident type is covered by policy
        Returns (is_covered, confidence_score)
        """
        incident_lower = incident_type.lower()
        
        # Find matching coverage category
        coverage_category = None
        for key, category in self.coverage_mapping.items():
            if key in incident_lower:
                coverage_category = category
                break
        
        if not coverage_category:
            return False, 0.1  # Unknown incident type
        
        # Check if coverage exists in policy
        is_covered = coverage_details.get(coverage_category, False)
        
        if is_covered:
            return True, 1.0
        else:
            return False, 0.2
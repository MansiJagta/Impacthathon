"""Relevant clause extraction."""
# app/agents/node3_policy_agent/clause_extractor.py
from typing import List

class ClauseExtractor:
    """Simple template-based clause extractor - NO ML needed"""
    
    def __init__(self):
        self.clause_mapping = {
            "motor": {
                "accident": [
                    "Clause 4.2: Accident coverage - Loss or damage caused by accident, fire, external explosion, lightning, burglary, housebreaking or theft"
                ],
                "theft": [
                    "Clause 5.1: Theft protection - Vehicle theft coverage including parts and accessories"
                ],
                "fire": [
                    "Clause 4.3: Fire and explosion coverage - Damage by fire, external explosion, self-ignition or lightning"
                ],
                "third_party": [
                    "Section 2: Third Party Liability - Legal liability to third parties for bodily injury or property damage"
                ],
                "default": [
                    "General coverage provisions apply as per policy terms"
                ]
            },
            "health": {
                "accident": [
                    "Clause 3.1: Accident hospitalization - Coverage for inpatient treatment due to accident"
                ],
                "illness": [
                    "Clause 3.2: Illness coverage - Hospitalization for covered illnesses"
                ],
                "default": [
                    "Standard health insurance coverage terms apply"
                ]
            },
            "property": {
                "fire": [
                    "Section 1: Fire and allied perils - Coverage for damage by fire, lightning, explosion"
                ],
                "theft": [
                    "Section 2: Burglary and theft - Coverage for theft with forcible entry"
                ],
                "default": [
                    "Standard property insurance coverage applies"
                ]
            }
        }
    
    def extract(self, incident_type: str, policy_type: str) -> List[str]:
        """Extract relevant clauses based on incident type"""
        policy_clauses = self.clause_mapping.get(policy_type, {})
        
        # Find matching clause
        for key, clauses in policy_clauses.items():
            if key in incident_type.lower():
                return clauses
        
        # Return default if no match
        return policy_clauses.get("default", ["General coverage provisions"])
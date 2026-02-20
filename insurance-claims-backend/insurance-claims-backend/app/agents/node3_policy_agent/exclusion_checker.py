"""Exclusion checking logic."""
# app/agents/node3_policy_agent/exclusion_checker.py
from typing import List, Dict
import re

class ExclusionChecker:
    """Simple keyword-based exclusion checker - NO ML NEEDED"""
    
    def __init__(self):
        # Define exclusion keywords (can be loaded from DB in production)
        self.exclusion_keywords: Dict[str, List[str]] = {
            "Driving under influence": ["alcohol", "drunk", "intoxicated", "dwi", "dui", "tipsy"],
            "Commercial use": ["business", "delivery", "commercial", "uber", "ola", "taxi", "cab"],
            "Without valid license": ["no license", "unlicensed", "expired license", "never had license"],
            "Wear and tear": ["maintenance", "old", "worn", "rusted", "corroded", "age"],
            "Intentional damage": ["intentional", "deliberate", "on purpose", "self-inflicted", "planned"],
            "Racing": ["race", "racing", "speed test", "track day", "competition"],
            "War": ["war", "terrorism", "nuclear", "invasion"],
            "Tyres only": ["tyre", "tire", "tyres only", "only tyres"]
        }
    
    def check_exclusions(self, exclusions: List[str], incident_description: str) -> List[str]:
        """
        Check if any exclusions apply to this claim
        Returns list of triggered exclusions
        """
        triggered = []
        description_lower = incident_description.lower()
        
        for exclusion in exclusions:
            # Check direct match
            if exclusion.lower() in description_lower:
                triggered.append(exclusion)
                continue
            
            # Check keyword-based
            for key, keywords in self.exclusion_keywords.items():
                if key.lower() in exclusion.lower():
                    for keyword in keywords:
                        if self._contains_keyword(description_lower, keyword):
                            triggered.append(exclusion)
                            break
        
        return triggered

    def _contains_keyword(self, text: str, keyword: str) -> bool:
        """Match keyword as a whole word/phrase to avoid substring false positives."""
        pattern = r"\b" + re.escape(keyword.lower()) + r"\b"
        return re.search(pattern, text) is not None
"""Mock watchlist screening."""
"""Watchlist checking for known fraudsters."""
# app/agents/node4_fraud_agent/watchlist_checker.py

from typing import Dict, Tuple

class WatchlistChecker:
    """
    Checks claimant and provider against fraud watchlist
    """
    
    def __init__(self):
        # Mock watchlist data
        self.fraudulent_claimants = [
            "Known Fraudster",
            "Serial Claimant",
            "Fake Identity User"
        ]
        
        self.fraudulent_providers = [
            "Quick Fix Garage",
            "Questionable Clinic",
            "Fake Provider Inc",
            "Fraud Law Associates"
        ]
    
    def check_watchlist(self, claimant_name: str, provider_name: str) -> Dict:
        """
        Check if entities are on fraud watchlist
        
        Returns:
            Dict with on_watchlist flag and details
        """
        result = {
            "on_watchlist": False,
            "details": "",
            "score_impact": 0.0
        }
        
        # Check claimant
        for fraud in self.fraudulent_claimants:
            if fraud.lower() in claimant_name.lower():
                result.update({
                    "on_watchlist": True,
                    "details": f"Claimant '{claimant_name}' matches watchlist entry",
                    "score_impact": 0.5
                })
                return result
        
        # Check provider
        for fraud in self.fraudulent_providers:
            if fraud.lower() in provider_name.lower():
                result.update({
                    "on_watchlist": True,
                    "details": f"Provider '{provider_name}' matches watchlist entry",
                    "score_impact": 0.5
                })
                return result
        
        return result
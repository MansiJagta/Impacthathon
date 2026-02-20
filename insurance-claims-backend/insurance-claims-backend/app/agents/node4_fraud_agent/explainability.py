# app/agents/node4_fraud_agent/explainability.py

import shap
import numpy as np
from typing import Dict, Any, List
import pandas as pd

class FraudExplainer:
    """
    Explainable AI using SHAP (SHapley Additive exPlanations)
    Provides human-readable reasons for fraud scores
    """
    
    def __init__(self):
        # Mock feature names for explanations
        self.feature_names = [
            "claim_amount",
            "days_since_policy",
            "days_to_report",
            "document_count",
            "round_amount_flag",
            "provider_volume",
            "claimant_history",
            "network_density"
        ]
        
        # Feature importance weights (from trained model)
        self.feature_importance = {
            "claim_amount": 0.25,
            "days_since_policy": 0.20,
            "provider_volume": 0.15,
            "claimant_history": 0.15,
            "days_to_report": 0.10,
            "network_density": 0.08,
            "document_count": 0.05,
            "round_amount_flag": 0.02
        }
    
    def explain(self, fraud_score: float, indicators: List[Dict], 
                claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate human-readable explanations for fraud decisions
        """
        explanations = []
        top_factors = []
        
        # 1. Explain based on indicators
        for indicator in indicators:
            explanations.append({
                "factor": indicator["type"],
                "description": indicator["details"],
                "severity": indicator.get("severity", "MEDIUM"),
                "contribution": self._get_contribution(indicator["type"])
            })
            
            top_factors.append({
                "name": indicator["type"],
                "impact": self._get_contribution(indicator["type"])
            })
        
        # 2. Generate SHAP-style explanations
        shap_values = self._mock_shap_values(claim_data)
        
        # 3. Create natural language summary
        if fraud_score < 0.3:
            summary = "Low fraud risk. No significant indicators detected."
        elif fraud_score < 0.5:
            summary = "Medium fraud risk. Some suspicious patterns identified."
        elif fraud_score < 0.7:
            summary = "High fraud risk. Multiple strong indicators present."
        else:
            summary = "Critical fraud risk. Immediate investigation required."
        
        # Sort top factors by impact
        top_factors = sorted(top_factors, 
                           key=lambda x: x["impact"], 
                           reverse=True)[:3]
        
        return {
            "summary": summary,
            "fraud_score_explanation": f"This score is based on {len(indicators)} fraud indicators",
            "top_contributing_factors": top_factors,
            "detailed_explanations": explanations,
            "shap_values": shap_values,
            "recommendation": self._get_recommendation(fraud_score, indicators)
        }
    
    def _get_contribution(self, indicator_type: str) -> float:
        """Get the contribution weight of an indicator"""
        weights = {
            "EXACT_DUPLICATE": 0.25,
            "FRAUD_RING_DETECTED": 0.22,
            "EARLY_CLAIM": 0.20,
            "HIGH_VOLUME_PROVIDER": 0.18,
            "NAME_MISMATCH": 0.15,
            "AMOUNT_ANOMALY": 0.12,
            "ML_HIGH_RISK": 0.25,
            "ISOLATION_FOREST_ANOMALY": 0.15
        }
        return weights.get(indicator_type, 0.1)
    
    def _mock_shap_values(self, claim_data: Dict) -> List[float]:
        """Generate mock SHAP values for demonstration"""
        # In production, this would use actual SHAP calculations
        base_value = 0.3  # Base fraud probability
        
        shap_contributions = []
        for feature in self.feature_names:
            # Random contribution for demo
            contribution = np.random.uniform(-0.1, 0.2)
            shap_contributions.append(contribution)
        
        return shap_contributions
    
    def _get_recommendation(self, score: float, indicators: List) -> str:
        """Generate actionable recommendation"""
        if score > 0.7:
            return "Immediate escalation to fraud investigation team required"
        elif score > 0.5:
            return "Manual review by senior underwriter recommended"
        elif indicators:
            return "Review specific indicators flagged above"
        else:
            return "Auto-approve - no action needed"
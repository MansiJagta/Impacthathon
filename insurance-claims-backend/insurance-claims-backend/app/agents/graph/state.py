"""Shared workflow state definition."""
# app/agents/graph/state.py
from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    """Shared state for LangGraph workflow"""
    
    # Input from frontend
    claim_id: str
    policy_number: str
    claim_amount: float
    incident_type: str
    incident_date: str
    incident_description: str
    claimant_name: str
    documents: List[Dict[str, Any]]
    
    # From Node 2 (Cross Validation)
    consistency_score: Optional[float]
    mismatches: Optional[List[Dict]]
    
    # From Node 3 (Policy Coverage)
    policy_analysis: Optional[Dict[str, Any]]
    
    # From Node 4 (Fraud Detection)
    fraud_analysis: Optional[Dict[str, Any]]
    
    # Final decision (to be populated later)
    final_decision: Optional[Dict[str, Any]]
    
    # Error tracking
    errors: List[str]
    status: str  # processing, completed, failed
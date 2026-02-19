# tests/test_anomaly.py

import pytest
import asyncio
from app.agents.node4_fraud_agent.anomaly_detector import AnomalyDetector

@pytest.mark.asyncio
async def test_amount_anomaly():
    detector = AnomalyDetector()
    
    # Test amount just below 1 lakh
    result = await detector.detect({
        "claim_amount": 99000,
        "policy_start_date": "2026-01-01T00:00:00Z",
        "incident_date": "2026-02-15T00:00:00Z",
        "submission_date": "2026-02-16T00:00:00Z"
    })
    
    assert result["score"] > 0
    assert len(result["indicators"]) > 0
    assert result["indicators"][0]["type"] == "AMOUNT_ANOMALY"

@pytest.mark.asyncio
async def test_timing_anomaly():
    detector = AnomalyDetector()
    
    # Test early claim (3 days after policy)
    result = await detector.detect({
        "claim_amount": 50000,
        "policy_start_date": "2026-02-10T00:00:00Z",
        "incident_date": "2026-02-13T00:00:00Z",
        "submission_date": "2026-02-14T00:00:00Z"
    })
    
    assert result["score"] > 0
    assert result["indicators"][0]["type"] == "EARLY_CLAIM"
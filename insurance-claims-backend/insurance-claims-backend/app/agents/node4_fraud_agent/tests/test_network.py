# tests/test_network.py

import pytest
import asyncio
from app.agents.node4_fraud_agent.network_analyzer import NetworkAnalyzer

@pytest.mark.asyncio
async def test_provider_volume():
    analyzer = NetworkAnalyzer()
    
    result = await analyzer.analyze({
        "provider_name": "High Volume Clinic",
        "claimant_name": "John Doe"
    })
    
    # This will need mock data in MongoDB
    assert "score" in result
    assert "indicators" in result
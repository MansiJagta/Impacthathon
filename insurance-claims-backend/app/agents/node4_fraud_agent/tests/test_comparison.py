# tests/test_comparison.py

import pytest
import asyncio
from app.agents.node4_fraud_agent.document_comparison import DocumentComparer

@pytest.mark.asyncio
async def test_name_mismatch():
    comparer = DocumentComparer()
    
    result = await comparer.compare({
        "documents": [
            {"type": "policy", "claimant_name": "John Smith"},
            {"type": "id_proof", "name": "Jon Smith"},
            {"type": "bill", "patient_name": "John A. Smith"}
        ]
    })
    
    assert result["score"] > 0
    assert any(i["type"] == "NAME_MISMATCH" for i in result["indicators"])
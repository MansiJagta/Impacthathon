# test_all_components.py
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.agents.node4_fraud_agent.anomaly_detector import AnomalyDetector
from app.agents.node4_fraud_agent.duplicate_detector import DuplicateDetector
from app.agents.node4_fraud_agent.network_analyzer import NetworkAnalyzer
import json

async def test_all():
    print("="*70)
    print("🧪 TESTING ALL FRAUD DETECTION COMPONENTS")
    print("="*70)
    
    # Test 1: Amount Anomaly
    print("\n📊 Testing Amount Anomaly Detector...")
    detector = AnomalyDetector()
    test_claim = {
        "claim_amount": 99000,
        "incident_date": "2026-02-15T00:00:00Z",
        "submission_date": "2026-02-16T00:00:00Z",
        "policy_start_date": "2026-01-01T00:00:00Z",
        "documents": [{"content": "test"}],
        "claimant_name": "Test User",
        "provider_name": "Test Provider"
    }
    
    result = await detector.detect(test_claim)
    print(json.dumps(result, indent=2))
    
    # Test 2: Duplicate Detector
    print("\n📊 Testing Duplicate Detector...")
    duplicate = DuplicateDetector()
    test_doc = {
        "claim_id": "TEST-001",
        "documents": [
            {
                "type": "bill",
                "filename": "invoice.pdf",
                "content": "Test invoice content for duplicate detection"
            }
        ]
    }
    result = await duplicate.detect(test_doc)
    print(json.dumps(result, indent=2))
    
    # Test 3: Network Analyzer
    print("\n📊 Testing Network Analyzer...")
    network = NetworkAnalyzer()
    test_entities = {
        "claim_id": "TEST-001",
        "claimant_name": "Test User",
        "claimant_id": "CUST-001",
        "provider_name": "Test Provider",
        "provider_id": "PROV-001",
        "phone": "123-456-7890",
        "email": "test@email.com",
        "address": "123 Test St",
        "incident_date": "2026-02-15T00:00:00Z",
        "submission_date": "2026-02-16T00:00:00Z"
    }
    result = await network.analyze(test_entities)
    print(json.dumps(result, indent=2))
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETED")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(test_all())
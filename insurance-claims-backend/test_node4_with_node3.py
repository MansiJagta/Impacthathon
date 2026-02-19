# test_node4_with_node3.py
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.agents.node3_policy_agent.agent import PolicyCoverageAgent
from app.agents.node4_fraud_agent.agent import FraudDetectionAgent
from app.database.mongodb import connect_to_mongo, close_mongo_connection
import json

async def test_full_pipeline():
    """Test Node 3 and Node 4 together"""
    
    print("="*70)
    print("🚀 TESTING FULL PIPELINE: NODE 3 → NODE 4")
    print("="*70)
    
    await connect_to_mongo()

    # Initialize agents
    policy_agent = PolicyCoverageAgent()
    fraud_agent = FraudDetectionAgent()
    
    # Test claims
    test_claims = [
        {
            "name": "Clean Motor Claim",
            "claim_id": "CL-123",
            "policy_number": "MOT-123456",
            "claim_amount": 75000,
            "incident_type": "accident",
            "incident_date": "2026-02-09T00:00:00Z",
            "submission_date": "2026-02-11T00:00:00Z",
            "policy_start_date": "2026-01-01T00:00:00Z",
            "claimant_name": "John Smith",
            "claimant_id": "CUST-78901",
            "provider_name": "City Hospital",
            "provider_id": "PROV-001",
            "documents": [
                {
                    "type": "bill",
                    "filename": "hospital_bill.pdf",
                    "content": "City Hospital bill for ₹75,000",
                    "metadata": {"page_count": 2}
                }
            ],
            "incident_description": "Car accident at junction",
            "policy_type": "motor",
            "incident_location": "Mumbai"
        },
        {
            "name": "Suspicious Motor Claim",
            "claim_id": "CL-456",
            "policy_number": "MOT-123456",
            "claim_amount": 99000,
            "incident_type": "accident",
            "incident_date": "2026-02-13T00:00:00Z",
            "submission_date": "2026-02-14T00:00:00Z",
            "policy_start_date": "2026-02-10T00:00:00Z",
            "claimant_name": "Jane Doe",
            "claimant_id": "CUST-78902",
            "provider_name": "Quick Fix Garage",
            "provider_id": "PROV-099",
            "documents": [
                {
                    "type": "bill",
                    "filename": "repair_estimate.pdf",
                    "content": "Quick Fix Garage repair estimate ₹99,000",
                    "metadata": {"page_count": 1}
                }
            ],
            "incident_description": "Accident while doing Uber delivery",
            "policy_type": "motor",
            "incident_location": "Mumbai"
        }
    ]
    
    try:
        for claim in test_claims:
            print(f"\n{'='*70}")
            print(f"📋 TESTING: {claim['name']}")
            print(f"{'='*70}")
            
            print(f"\n📝 Claim Details:")
            print(f"   ID: {claim['claim_id']}")
            print(f"   Amount: ₹{claim['claim_amount']}")
            print(f"   Policy: {claim['policy_number']}")
            
            # Run Node 3
            print(f"\n🟢 STEP 1: Running Node 3 (Policy Coverage)...")
            node3_result = await policy_agent.process(claim)
            
            if "policy_analysis" in node3_result:
                analysis = node3_result["policy_analysis"]
                print(f"\n✅ Node 3 Output:")
                print(f"   • Covered: {analysis.get('is_covered')}")
                print(f"   • Covered Amount: ₹{analysis.get('covered_amount')}")
                print(f"   • Deductible: ₹{analysis.get('deductible')}")
                print(f"   • Exclusions: {analysis.get('exclusions_triggered')}")
            
            # Combine for Node 4
            node4_input = {**claim, **node3_result}
            
            # Run Node 4
            print(f"\n🟢 STEP 2: Running Node 4 (Fraud Detection)...")
            node4_result = await fraud_agent.process(node4_input)
            
            print(f"\n✅ Node 4 Output:")
            if "fraud_analysis" in node4_result:
                fraud = node4_result["fraud_analysis"]
                print(f"   • Fraud Score: {fraud.get('fraud_score')}")
                print(f"   • Risk Level: {fraud.get('risk_level')}")
                print(f"   • Investigate: {fraud.get('requires_investigation')}")
                
                if fraud.get("fraud_indicators"):
                    print(f"\n   🚩 Fraud Indicators:")
                    for i, ind in enumerate(fraud["fraud_indicators"], 1):
                        print(f"      {i}. {ind.get('type')}: {ind.get('details')}")
        
        print("\n" + "="*70)
        print("✅ PIPELINE TEST COMPLETE!")
        print("="*70)
    finally:
        await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(test_full_pipeline())
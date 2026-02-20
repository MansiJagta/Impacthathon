"""Local agent testing script."""
#!/usr/bin/env python3
# scripts/test_agents.py

import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agents.node3_policy_agent.agent import PolicyCoverageAgent
from app.agents.node4_fraud_agent.agent import FraudDetectionAgent
from app.database.mongodb import connect_to_mongo, close_mongo_connection

async def test_node3():
    """Test Node 3: Policy Coverage Agent"""
    print("\n" + "="*50)
    print("TESTING NODE 3: POLICY COVERAGE AGENT")
    print("="*50)
    
    # Create agent
    agent = PolicyCoverageAgent()
    
    # Test state
    test_state = {
        "claim_id": "CL-123",
        "policy_number": "MOT-123456",
        "claim_amount": 75000,
        "incident_type": "accident",
        "incident_date": "2026-02-09T00:00:00Z",
        "incident_description": "Car accident at junction, vehicle damaged",
        "claimant_name": "John Smith",
        "documents": []
    }
    
    # Process
    result = await agent.process(test_state)
    
    # Print result
    print("\n✅ Node 3 Result:")
    import json
    print(json.dumps(result, indent=2))
    
    return result

async def test_node4():
    """Test Node 4: Fraud Detection Agent"""
    print("\n" + "="*50)
    print("TESTING NODE 4: FRAUD DETECTION AGENT")
    print("="*50)
    
    # Create agent
    agent = FraudDetectionAgent()
    
    # Test state
    test_state = {
        "claim_id": "CL-456",
        "claim_amount": 99999,
        "incident_date": "2026-02-15T00:00:00Z",
        "submission_date": "2026-02-16T00:00:00Z",
        "policy_start_date": "2026-02-10T00:00:00Z",
        "claimant_name": "John Smith",
        "provider_name": "City Hospital",
        "documents": []
    }
    
    # Process
    result = await agent.process(test_state)
    
    # Print result
    print("\n✅ Node 4 Result:")
    import json
    print(json.dumps(result, indent=2))
    
    return result

async def main():
    """Main test function"""
    print("🚀 Testing Insurance Claims AI Agents")
    print("="*50)
    
    # Connect to MongoDB
    await connect_to_mongo()
    
    try:
        # Test Node 3
        node3_result = await test_node3()
        
        # Test Node 4
        node4_result = await test_node4()
        
        print("\n" + "="*50)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
    
    finally:
        # Close MongoDB connection
        await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())
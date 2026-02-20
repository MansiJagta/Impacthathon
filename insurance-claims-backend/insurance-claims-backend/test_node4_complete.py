# test_node4_complete.py
import asyncio
import sys
from pathlib import Path
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.agents.node3_policy_agent.agent import PolicyCoverageAgent
from app.agents.node4_fraud_agent.agent import FraudDetectionAgent
from app.database.mongodb import connect_to_mongo, close_mongo_connection

async def test_full_pipeline():
    """Test Node 3 first, then feed output to Node 4"""
    
    print("="*70)
    print("🚀 TESTING FULL PIPELINE: NODE 3 → NODE 4")
    print("="*70)
    
    await connect_to_mongo()

    # Initialize agents
    policy_agent = PolicyCoverageAgent()
    fraud_agent = FraudDetectionAgent()
    
    # Test Claim 1: Clean Claim (should be approved, low fraud)
    clean_claim = {
        "claim_id": "CL-CLEAN-001",
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
                "content": "City Hospital bill for ₹75,000 - Patient John Smith",
                "metadata": {"page_count": 2}
            }
        ],
        "incident_description": "Car accident at junction, front bumper damaged",
        "policy_type": "motor",
        "incident_location": "Mumbai",
        "claimant_phone": "9876543210",
        "claimant_email": "john@email.com",
        "claimant_address": "123 Main St, Mumbai"
    }
    
    # Test Claim 2: Suspicious Claim (should trigger multiple detectors)
    suspicious_claim = {
        "claim_id": "CL-SUSPECT-002",
        "policy_number": "MOT-123456",
        "claim_amount": 99000,  # Just below 1L threshold
        "incident_type": "accident",
        "incident_date": "2026-02-13T00:00:00Z",
        "submission_date": "2026-02-14T00:00:00Z",
        "policy_start_date": "2026-02-10T00:00:00Z",  # Only 3 days old
        "claimant_name": "Jane Doe",
        "claimant_id": "CUST-78902",
        "provider_name": "Quick Fix Garage",  # Suspicious provider
        "provider_id": "PROV-099",
        "documents": [
            {
                "type": "bill",
                "filename": "repair_estimate.pdf",
                "content": "Quick Fix Garage repair estimate ₹99,000 for Jane Doe",
                "metadata": {"page_count": 1}
            },
            {
                "type": "report",
                "filename": "police_report.pdf", 
                "content": "Police report for accident involving Jane Doe on 2026-02-13",
                "metadata": {"page_count": 3}
            }
        ],
        "incident_description": "Accident while doing Uber delivery",  # Commercial use
        "policy_type": "motor",
        "incident_location": "Mumbai",
        "claimant_phone": "9876543211",
        "claimant_email": "jane@email.com",
        "claimant_address": "456 Park Ave, Mumbai"
    }
    
    # Test Claim 3: Fraud Ring Claim (should trigger network analysis)
    ring_claim = {
        "claim_id": "CL-RING-003",
        "policy_number": "HEALTH-456789",
        "claim_amount": 150000,
        "incident_type": "accident",
        "incident_date": "2026-02-15T00:00:00Z",
        "submission_date": "2026-02-16T00:00:00Z",
        "policy_start_date": "2026-01-15T00:00:00Z",
        "claimant_name": "Bob Wilson",
        "claimant_id": "CUST-78903",
        "provider_name": "Questionable Clinic",  # In fraud ring
        "provider_id": "PROV-888",
        "attorney_name": "Fraud Law Associates",  # Connected to fraud ring
        "documents": [
            {
                "type": "bill",
                "filename": "medical_bill.pdf",
                "content": "Medical treatment ₹150,000 for Bob Wilson at Questionable Clinic",
                "metadata": {"page_count": 3}
            },
            {
                "type": "prescription",
                "filename": "prescription.pdf",
                "content": "Various medications prescribed for Bob Wilson",
                "metadata": {"page_count": 1}
            }
        ],
        "incident_description": "Injury from slip and fall at shopping mall",
        "policy_type": "health",
        "incident_location": "Delhi",
        "claimant_phone": "9876543212",
        "claimant_email": "bob@email.com",
        "claimant_address": "789 Lake View, Bangalore"
    }
    
    # Test all claims
    test_claims = [
        ("CLEAN CLAIM", clean_claim),
        ("SUSPICIOUS CLAIM", suspicious_claim),
        ("FRAUD RING CLAIM", ring_claim)
    ]
    
    all_results = []
    
    try:
        for claim_name, claim_data in test_claims:
            print(f"\n{'='*70}")
            print(f"📋 TESTING: {claim_name}")
            print(f"{'='*70}")
            
            print(f"\n📝 Claim Details:")
            print(f"   ID: {claim_data['claim_id']}")
            print(f"   Policy: {claim_data['policy_number']}")
            print(f"   Amount: ₹{claim_data['claim_amount']}")
            print(f"   Claimant: {claim_data['claimant_name']}")
            print(f"   Provider: {claim_data['provider_name']}")
            print(f"   Description: {claim_data.get('incident_description', 'N/A')}")
            
            # ============================================================
            # STEP 1: RUN NODE 3 (POLICY COVERAGE)
            # ============================================================
            print(f"\n🟢 STEP 1: Running Node 3 - Policy Coverage Agent...")
            node3_result = await policy_agent.process(claim_data)
            
            if "policy_analysis" in node3_result:
                analysis = node3_result["policy_analysis"]
                print(f"\n✅ Node 3 Output:")
                print(f"   • Policy Number: {analysis.get('policy_number')}")
                print(f"   • Holder: {analysis.get('holder_name')}")
                print(f"   • Is Covered: {analysis.get('is_covered')}")
                print(f"   • Covered Amount: ₹{analysis.get('covered_amount')}")
                print(f"   • Deductible: ₹{analysis.get('deductible')}")
                print(f"   • Exclusions Triggered: {analysis.get('exclusions_triggered', [])}")
                print(f"   • Coverage Score: {analysis.get('coverage_score')}")
            
            # ============================================================
            # STEP 2: COMBINE OUTPUTS FOR NODE 4
            # ============================================================
            # Merge original claim data with Node 3 results
            node4_input = {**claim_data, **node3_result}
            
            # ============================================================
            # STEP 3: RUN NODE 4 (FRAUD DETECTION)
            # ============================================================
            print(f"\n🟢 STEP 2: Running Node 4 - Fraud Detection Agent...")
            node4_result = await fraud_agent.process(node4_input)
            
            # Display results
            print(f"\n📊 NODE 4 OUTPUT:")
            fraud = node4_result.get("fraud_analysis", {})
            print(f"   • Fraud Score: {fraud.get('fraud_score')}")
            print(f"   • Risk Level: {fraud.get('risk_level')}")
            print(f"   • Investigate: {fraud.get('requires_investigation')}")
            print(f"   • Processing Time: {fraud.get('processing_time_ms')}ms")
            print(f"   • Confidence: {fraud.get('confidence')}")
            
            # Show component scores
            components = fraud.get("components", {})
            if components:
                print(f"\n   📈 Component Scores:")
                for comp, score in components.items():
                    print(f"      • {comp}: {score}")
            
            # Show fraud indicators
            indicators = fraud.get("fraud_indicators", [])
            if indicators:
                print(f"\n   🚩 Fraud Indicators ({len(indicators)}):")
                for i, ind in enumerate(indicators, 1):
                    print(f"      {i}. {ind.get('type')}: {ind.get('details')}")
                    print(f"         Severity: {ind.get('severity')}, Impact: +{ind.get('score_impact')}")
            
            # ============================================================
            # STEP 4: COMBINED ANALYSIS
            # ============================================================
            print(f"\n📊 COMBINED ANALYSIS:")
            
            # Determine final recommendation
            is_covered = node3_result.get("policy_analysis", {}).get("is_covered", False)
            fraud_score = fraud.get("fraud_score", 0)
            risk_level = fraud.get("risk_level", "LOW")
            requires_investigation = fraud.get("requires_investigation", False)
            
            if not is_covered:
                final_status = "❌ REJECTED (Not Covered by Policy)"
            elif requires_investigation:
                final_status = "⚠️ MANUAL REVIEW (HITL Queue)"
            elif fraud_score > 0.7:
                final_status = "🔴 REJECTED (Critical Fraud Risk)"
            elif fraud_score > 0.5:
                final_status = "🟡 FLAGGED FOR REVIEW (High Fraud Risk)"
            elif fraud_score > 0.3:
                final_status = "⚠️ MANUAL REVIEW (Medium Fraud Risk)"
            else:
                final_status = "✅ AUTO-APPROVED (Low Fraud Risk)"
            
            print(f"   • Policy Coverage: {'✅ Covered' if is_covered else '❌ Not Covered'}")
            print(f"   • Fraud Risk: {risk_level} ({fraud_score:.3f})")
            print(f"   • Final Decision: {final_status}")
            
            # Store results
            all_results.append({
                "claim_name": claim_name,
                "claim_id": claim_data["claim_id"],
                "policy_analysis": node3_result.get("policy_analysis", {}),
                "fraud_analysis": fraud,
                "final_status": final_status
            })
            
            print("\n" + "-"*70)
        
        # ============================================================
        # FINAL SUMMARY
        # ============================================================
        print("\n" + "="*70)
        print("📊 PIPELINE TEST SUMMARY")
        print("="*70)
        
        for res in all_results:
            print(f"\n{res['claim_name']} ({res['claim_id']}):")
            print(f"   • Policy Covered: {res['policy_analysis'].get('is_covered', False)}")
            print(f"   • Fraud Score: {res['fraud_analysis'].get('fraud_score', 0)}")
            print(f"   • Risk Level: {res['fraud_analysis'].get('risk_level', 'N/A')}")
            print(f"   • Indicators: {len(res['fraud_analysis'].get('fraud_indicators', []))}")
            print(f"   • Final: {res['final_status']}")
        
        print("\n" + "="*70)
        print("✅ FULL PIPELINE TEST COMPLETE!")
        print("="*70)
        
        return all_results
    finally:
        await close_mongo_connection()

async def test_single_claim(claim_data: dict, claim_name: str):
    """Test a single claim through the pipeline"""
    
    print(f"\n{'='*70}")
    print(f"📋 TESTING SINGLE CLAIM: {claim_name}")
    print(f"{'='*70}")
    
    await connect_to_mongo()
    policy_agent = PolicyCoverageAgent()
    fraud_agent = FraudDetectionAgent()
    
    try:
        # Run Node 3
        print(f"\n🟢 Running Node 3...")
        node3_result = await policy_agent.process(claim_data)
        
        if "policy_analysis" in node3_result:
            analysis = node3_result["policy_analysis"]
            print(f"\n✅ Policy Analysis:")
            print(f"   Covered: {analysis.get('is_covered')}")
            print(f"   Amount: ₹{analysis.get('covered_amount')}")
        
        # Run Node 4
        print(f"\n🟢 Running Node 4...")
        node4_input = {**claim_data, **node3_result}
        node4_result = await fraud_agent.process(node4_input)
        
        print(f"\n📊 Fraud Analysis:")
        fraud = node4_result.get("fraud_analysis", {})
        print(json.dumps(fraud, indent=2))
        
        return node3_result, node4_result
    finally:
        await close_mongo_connection()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--single":
        # Test a single claim with custom data
        # You can modify this to test specific scenarios
        test_claim = {
            "claim_id": "CL-TEST-999",
            "policy_number": "MOT-123456",
            "claim_amount": 85000,
            "incident_type": "accident",
            "incident_date": "2026-02-18T00:00:00Z",
            "submission_date": "2026-02-19T00:00:00Z",
            "policy_start_date": "2026-01-01T00:00:00Z",
            "claimant_name": "Test User",
            "claimant_id": "CUST-999",
            "provider_name": "Test Provider",
            "provider_id": "PROV-999",
            "documents": [],
            "incident_description": "Test claim for single run",
            "policy_type": "motor"
        }
        asyncio.run(test_single_claim(test_claim, "CUSTOM TEST"))
    else:
        # Run full pipeline test
        asyncio.run(test_full_pipeline())
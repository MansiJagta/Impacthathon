# test_node3.py - Complete Node 3 Test File
# Run this to test your Policy Coverage Agent

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ConfigDict
from pymongo.errors import OperationFailure

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================
ROOT_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
TEST_ENV_PATH = Path(__file__).resolve().parent / ".env"

load_dotenv(ROOT_ENV_PATH)
load_dotenv(TEST_ENV_PATH, override=True)
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB") or os.getenv("MONGODB_DB_NAME") or "insurance_claiming_platform"

print(f"ℹ️ MongoDB target database: {DB_NAME}")


def _load_local_policies() -> List[Dict[str, Any]]:
    base_dir = Path(__file__).resolve().parents[1]
    policies_path = base_dir / "app" / "data" / "mock_data" / "policies.json"
    try:
        return json.loads(policies_path.read_text(encoding="utf-8"))
    except Exception:
        return []

# ============================================================
# DATA MODELS (Pydantic)
# ============================================================

class PolicyLimits(BaseModel):
    ownDamage: float
    thirdParty: str = "unlimited"
    personalAccident: float

class CoverageDetails(BaseModel):
    comprehensive: bool
    thirdParty: bool
    personalAccident: bool
    deductible: int
    limits: PolicyLimits

class PolicyModel(BaseModel):
    policyNumber: str
    policyType: str
    holderName: str
    holderId: str
    effectiveDate: str
    expiryDate: str
    sumInsured: float
    coverageDetails: CoverageDetails
    exclusions: List[str]
    
    model_config = ConfigDict(extra="ignore")

class CoverageAnalysis(BaseModel):
    policy_number: str
    is_covered: bool
    coverage_score: float = Field(ge=0, le=1)
    deductible: int
    policy_limit: float
    covered_amount: float
    exclusions_triggered: List[str]
    relevant_clauses: List[str]
    policy_type: str
    holder_name: str
    confidence: float = Field(ge=0, le=1)
    error: Optional[str] = None

# ============================================================
# COVERAGE CHECKER (Rule-based)
# ============================================================

class CoverageChecker:
    """Simple rule-based coverage checker"""
    
    def __init__(self):
        self.coverage_mapping = {
            "accident": "comprehensive",
            "collision": "comprehensive",
            "crash": "comprehensive",
            "theft": "comprehensive",
            "stolen": "comprehensive",
            "fire": "comprehensive",
            "third_party": "thirdParty",
            "liability": "thirdParty",
            "injury": "personalAccident",
            "hurt": "personalAccident"
        }
    
    def check_coverage(self, incident_type: str, coverage_details: dict) -> Tuple[bool, float]:
        incident_lower = incident_type.lower()
        
        # Find matching coverage category
        coverage_category = None
        for key, category in self.coverage_mapping.items():
            if key in incident_lower:
                coverage_category = category
                break
        
        if not coverage_category:
            return False, 0.1
        
        is_covered = coverage_details.get(coverage_category, False)
        
        if is_covered:
            return True, 1.0
        else:
            return False, 0.2

# ============================================================
# EXCLUSION CHECKER (Keyword-based)
# ============================================================

class ExclusionChecker:
    """Simple keyword-based exclusion checker"""
    
    def __init__(self):
        self.exclusion_keywords = {
            "Driving under influence": ["alcohol", "drunk", "intoxicated", "dwi", "dui"],
            "Commercial use": ["business", "delivery", "commercial", "uber", "ola", "taxi"],
            "Without valid license": ["no license", "unlicensed", "expired license"],
            "Wear and tear": ["maintenance", "old", "worn", "rusted"],
            "Intentional damage": ["intentional", "deliberate", "on purpose"],
            "Racing": ["race", "racing", "speed test"],
            "Tyres only": ["tyre", "tire", "tyres only"]
        }
    
    def check_exclusions(self, exclusions: List[str], incident_description: str) -> List[str]:
        triggered = []
        description_lower = incident_description.lower()
        
        for exclusion in exclusions:
            # Check direct match
            if exclusion.lower() in description_lower:
                triggered.append(exclusion)
                continue
            
            # Check keyword-based
            for key, keywords in self.exclusion_keywords.items():
                if key in exclusion:
                    for keyword in keywords:
                        if keyword in description_lower:
                            triggered.append(exclusion)
                            break
        
        return triggered

# ============================================================
# AMOUNT CALCULATOR
# ============================================================

class AmountCalculator:
    """Calculate covered amount after deductibles"""
    
    def calculate(self, claim_amount: float, policy_limit: float,
                  deductible: int, is_covered: bool,
                  exclusions_triggered: List[str]) -> float:
        if not is_covered or exclusions_triggered:
            return 0.0
        
        covered = min(claim_amount, policy_limit)
        covered = max(0, covered - deductible)
        return round(covered, 2)

# ============================================================
# CLAUSE EXTRACTOR (Template-based)
# ============================================================

class ClauseExtractor:
    """Extract relevant policy clauses"""
    
    def __init__(self):
        self.clause_mapping = {
            "motor": {
                "accident": ["Clause 4.2: Accident coverage - Loss or damage caused by accident"],
                "theft": ["Clause 5.1: Theft protection - Vehicle theft coverage"],
                "fire": ["Clause 4.3: Fire and explosion coverage"],
                "third_party": ["Section 2: Third Party Liability"],
                "default": ["General coverage provisions apply"]
            },
            "health": {
                "accident": ["Clause 3.1: Accident hospitalization"],
                "default": ["Standard health insurance coverage"]
            },
            "property": {
                "fire": ["Section 1: Fire and allied perils"],
                "theft": ["Section 2: Burglary and theft"],
                "default": ["Standard property insurance coverage"]
            }
        }
    
    def extract(self, incident_type: str, policy_type: str) -> List[str]:
        policy_clauses = self.clause_mapping.get(policy_type, {})
        
        for key, clauses in policy_clauses.items():
            if key in incident_type.lower():
                return clauses
        
        return policy_clauses.get("default", ["General coverage provisions"])

# ============================================================
# MAIN POLICY COVERAGE AGENT
# ============================================================

class PolicyCoverageAgent:
    """Node 3: Policy Coverage Agent"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.use_db = True
        self.local_policies: List[Dict[str, Any]] = []
        self.coverage_checker = CoverageChecker()
        self.exclusion_checker = ExclusionChecker()
        self.amount_calculator = AmountCalculator()
        self.clause_extractor = ClauseExtractor()
    
    async def connect(self):
        """Connect to MongoDB"""
        if not MONGO_URI:
            self.use_db = False
            self.local_policies = _load_local_policies()
            print("⚠️ MONGODB_URI not set, using local mock policies")
            return

        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[DB_NAME]

        try:
            await self.client.admin.command("ping")
            print("✅ Connected to MongoDB")
        except OperationFailure as exc:
            self.use_db = False
            self.local_policies = _load_local_policies()
            print(f"⚠️ MongoDB auth failed: {exc}. Using local mock policies")
        except Exception as exc:
            self.use_db = False
            self.local_policies = _load_local_policies()
            print(f"⚠️ MongoDB connection failed: {exc}. Using local mock policies")
    
    async def close(self):
        """Close MongoDB connection"""
        if self.client and self.use_db:
            self.client.close()
            print("🔌 Disconnected from MongoDB")
    
    async def fetch_policy(self, policy_number: str) -> Optional[Dict]:
        """Fetch policy from MongoDB"""
        if not self.use_db or self.db is None:
            return self._find_local_policy(policy_number)

        try:
            collection = self.db["policies"]
            return await collection.find_one({"policyNumber": policy_number})
        except OperationFailure:
            self.use_db = False
            self.local_policies = _load_local_policies()
            return self._find_local_policy(policy_number)
        except Exception:
            self.use_db = False
            self.local_policies = _load_local_policies()
            return self._find_local_policy(policy_number)

    def _find_local_policy(self, policy_number: str) -> Optional[Dict[str, Any]]:
        for policy in self.local_policies:
            if policy.get("policyNumber") == policy_number:
                return policy
        return None
    
    def _check_policy_validity(self, effective_date: str, expiry_date: str, 
                               incident_date: str) -> Tuple[bool, str]:
        """Check if policy was active on incident date"""
        try:
            effective = datetime.fromisoformat(effective_date.replace('Z', '+00:00'))
            expiry = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
            incident = datetime.fromisoformat(incident_date.replace('Z', '+00:00'))
            
            if incident < effective:
                return False, f"Policy not effective yet (starts {effective.date()})"
            elif incident > expiry:
                return False, f"Policy expired on {expiry.date()}"
            else:
                return True, "Policy active"
        except Exception as e:
            return False, f"Date validation error: {str(e)}"
    
    def _calculate_coverage_score(self, is_valid: bool, is_covered: bool,
                                  exclusions_count: int, within_limit: bool) -> float:
        score = 0.0
        if is_valid:
            score += 0.2
        if is_covered:
            score += 0.5
        if exclusions_count == 0:
            score += 0.2
        if within_limit:
            score += 0.1
        return min(score, 1.0)
    
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing function"""
        
        # Extract from state
        policy_number = state.get("policy_number")
        claim_amount = state.get("claim_amount", 0)
        incident_type = state.get("incident_type", "")
        incident_date = state.get("incident_date", "")
        incident_description = state.get("incident_description", "")
        
        print(f"\n📋 Processing Claim for Policy: {policy_number}")
        print(f"   Amount: ₹{claim_amount}, Type: {incident_type}")
        
        # Validate required fields
        if not policy_number:
            return {"policy_analysis": {"error": "Missing policy number", "is_covered": False}}
        
        # Fetch policy
        policy_data = await self.fetch_policy(policy_number)
        
        if not policy_data:
            return {"policy_analysis": {"error": f"Policy {policy_number} not found", "is_covered": False}}
        
        print(f"✅ Found policy for: {policy_data.get('holderName')}")
        
        # Convert to Pydantic model
        try:
            policy = PolicyModel(**policy_data)
        except Exception as e:
            return {"policy_analysis": {"error": f"Invalid policy data: {str(e)}", "is_covered": False}}
        
        # Check policy validity
        is_valid, validity_message = self._check_policy_validity(
            policy.effectiveDate, policy.expiryDate, incident_date
        )
        
        if not is_valid:
            return {"policy_analysis": {"error": validity_message, "is_covered": False}}
        
        print(f"✅ Policy active: {validity_message}")
        
        # Check coverage
        is_covered, coverage_confidence = self.coverage_checker.check_coverage(
            incident_type, policy.coverageDetails.model_dump()
        )
        print(f"✅ Coverage check: {'Covered' if is_covered else 'Not covered'}")
        
        # Check exclusions
        triggered_exclusions = self.exclusion_checker.check_exclusions(
            policy.exclusions, incident_description
        )
        if triggered_exclusions:
            print(f"⚠️ Exclusions triggered: {triggered_exclusions}")
        else:
            print("✅ No exclusions triggered")
        
        # Calculate amount
        covered_amount = self.amount_calculator.calculate(
            claim_amount, policy.sumInsured, policy.coverageDetails.deductible,
            is_covered, triggered_exclusions
        )
        print(f"💰 Covered amount: ₹{covered_amount}")
        
        # Calculate score
        coverage_score = self._calculate_coverage_score(
            is_valid, is_covered, len(triggered_exclusions),
            claim_amount <= policy.sumInsured
        )
        
        # Extract clauses
        relevant_clauses = self.clause_extractor.extract(incident_type, policy.policyType)
        
        # Prepare output
        analysis = CoverageAnalysis(
            policy_number=policy.policyNumber,
            is_covered=is_covered and len(triggered_exclusions) == 0,
            coverage_score=coverage_score,
            deductible=policy.coverageDetails.deductible,
            policy_limit=policy.sumInsured,
            covered_amount=covered_amount,
            exclusions_triggered=triggered_exclusions,
            relevant_clauses=relevant_clauses,
            policy_type=policy.policyType,
            holder_name=policy.holderName,
            confidence=0.99
        )
        
        return {"policy_analysis": analysis.model_dump()}

# ============================================================
# TEST FUNCTION
# ============================================================

async def test_node3():
    """Test Node 3 with multiple scenarios"""
    
    agent = PolicyCoverageAgent()
    await agent.connect()
    
    try:
        # Test Case 1: Valid claim (should be approved)
        print("\n" + "="*60)
        print("TEST CASE 1: Valid Motor Claim")
        print("="*60)
        
        state1 = {
            "policy_number": "MOT-123456",
            "claim_amount": 75000,
            "incident_type": "accident",
            "incident_date": "2026-02-09T00:00:00Z",
            "incident_description": "Car accident at junction, front bumper damaged",
            "claimant_name": "John Smith"
        }
        
        result1 = await agent.process(state1)
        print("\n📊 RESULT:")
        import json
        print(json.dumps(result1, indent=2))
        
        # Test Case 2: Claim with exclusion (commercial use)
        print("\n" + "="*60)
        print("TEST CASE 2: Commercial Use Exclusion")
        print("="*60)
        
        state2 = {
            "policy_number": "MOT-123456",
            "claim_amount": 50000,
            "incident_type": "accident",
            "incident_date": "2026-02-09T00:00:00Z",
            "incident_description": "Accident while doing Uber delivery",
            "claimant_name": "John Smith"
        }
        
        result2 = await agent.process(state2)
        print("\n📊 RESULT:")
        print(json.dumps(result2, indent=2))
        
        # Test Case 3: Policy not found
        print("\n" + "="*60)
        print("TEST CASE 3: Policy Not Found")
        print("="*60)
        
        state3 = {
            "policy_number": "MOT-999999",
            "claim_amount": 75000,
            "incident_type": "accident",
            "incident_date": "2026-02-09T00:00:00Z",
            "incident_description": "Test claim",
            "claimant_name": "Test User"
        }
        
        result3 = await agent.process(state3)
        print("\n📊 RESULT:")
        print(json.dumps(result3, indent=2))
        
        # Test Case 4: Health Insurance Claim
        print("\n" + "="*60)
        print("TEST CASE 4: Health Insurance Claim")
        print("="*60)
        
        state4 = {
            "policy_number": "HEALTH-456789",
            "claim_amount": 45000,
            "incident_type": "accident",
            "incident_date": "2026-02-09T00:00:00Z",
            "incident_description": "Hospitalization due to accident",
            "claimant_name": "Robert Johnson"
        }
        
        result4 = await agent.process(state4)
        print("\n📊 RESULT:")
        print(json.dumps(result4, indent=2))
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED")
        print("="*60)
        
    finally:
        await agent.close()

# ============================================================
# MAIN ENTRY POINT
# ============================================================

if __name__ == "__main__":
    print("🚀 NODE 3: POLICY COVERAGE AGENT TEST")
    print("="*60)
    asyncio.run(test_node3())

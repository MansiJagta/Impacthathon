# """Main Node 4 implementation."""
# # app/agents/node4_fraud_agent/agent.py

# import asyncio
# import time
# from typing import Dict, Any, List, Optional
# from datetime import datetime
# import numpy as np

# from .anomaly_detector import AnomalyDetector
# from .document_comparison import DocumentComparer
# from .duplicate_detector import DuplicateDetector
# from .network_analyzer import NetworkAnalyzer
# from .explainability import FraudExplainer
# from app.database.mongodb import get_collection

# class FraudDetectionAgent:
#     """
#     Node 4: Fraud Detection Agent
#     Runs 5 parallel checks with high-accuracy ML models
#     """
    
#     def __init__(self):
#         # Initialize all detectors
#         self.anomaly_detector = AnomalyDetector()
#         self.document_comparer = DocumentComparer()
#         self.duplicate_detector = DuplicateDetector()
#         self.network_analyzer = NetworkAnalyzer()
#         self.explainer = FraudExplainer()
        
#         # MongoDB collections (lazy-loaded)
#         self._claims_collection = None
#         self._fraud_patterns = None
        
#         # Performance tracking
#         self.processing_times = []
    
#     @property
#     def claims_collection(self):
#         """Lazy-load claims collection"""
#         if self._claims_collection is None:
#             self._claims_collection = get_collection("claims")
#         return self._claims_collection
    
#     @property
#     def fraud_patterns(self):
#         """Lazy-load fraud patterns collection"""
#         if self._fraud_patterns is None:
#             self._fraud_patterns = get_collection("fraud_patterns")
#         return self._fraud_patterns
    
#     async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
#         """
#         Main entry point - runs all checks in parallel for maximum speed
#         """
#         start_time = time.time()
        
#         # Extract data from state
#         claim_data = {
#             "claim_id": state.get("claim_id"),
#             "claim_amount": state.get("claim_amount", 0),
#             "incident_date": state.get("incident_date"),
#             "submission_date": state.get("submission_date"),
#             "policy_start_date": state.get("policy_start_date"),
#             "claimant_name": state.get("claimant_name", ""),
#             "claimant_id": state.get("claimant_id", ""),
#             "provider_name": state.get("provider_name", ""),
#             "provider_id": state.get("provider_id", ""),
#             "documents": state.get("documents", []),
#             "incident_type": state.get("incident_type", ""),
#             "incident_location": state.get("incident_location", ""),
#             "policy_type": state.get("policy_type", "")
#         }
        
#         # 🚀 RUN ALL 5 CHECKS IN PARALLEL for maximum speed
#         anomaly_task = self.anomaly_detector.detect(claim_data)
#         duplicate_task = self.duplicate_detector.detect(claim_data)
#         network_task = self.network_analyzer.analyze(claim_data)
#         document_task = self.document_comparer.compare(claim_data)
        
#         # Wait for all parallel tasks to complete
#         anomaly_result, duplicate_result, network_result, document_result = await asyncio.gather(
#             anomaly_task, duplicate_task, network_task, document_task
#         )
        
#         # Combine all fraud indicators
#         all_indicators = []
#         all_indicators.extend(anomaly_result.get("indicators", []))
#         all_indicators.extend(duplicate_result.get("indicators", []))
#         all_indicators.extend(network_result.get("indicators", []))
#         all_indicators.extend(document_result.get("indicators", []))
        
#         # Calculate weighted fraud score
#         fraud_score = (
#             anomaly_result.get("score", 0) * 0.3 +
#             duplicate_result.get("score", 0) * 0.25 +
#             network_result.get("score", 0) * 0.2 +
#             document_result.get("score", 0) * 0.25
#         )
        
#         # Cap at 1.0
#         fraud_score = min(fraud_score, 1.0)
        
#         # Generate explanations using SHAP
#         explanations = self.explainer.explain(
#             fraud_score=fraud_score,
#             indicators=all_indicators,
#             claim_data=claim_data
#         )
        
#         # Determine risk level
#         risk_level = self._get_risk_level(fraud_score)
        
#         # Track performance
#         processing_time = time.time() - start_time
#         self.processing_times.append(processing_time)
        
#         return {
#             "fraud_analysis": {
#                 "fraud_score": round(fraud_score, 3),
#                 "risk_level": risk_level,
#                 "requires_investigation": fraud_score > 0.5,
#                 "fraud_indicators": all_indicators,
#                 "explanations": explanations,
#                 "processing_time_ms": round(processing_time * 1000, 2),
#                 "confidence": self._calculate_confidence(all_indicators)
#             }
#         }
    
#     def _get_risk_level(self, score: float) -> str:
#         """Convert score to risk level"""
#         if score >= 0.7:
#             return "CRITICAL"
#         elif score >= 0.5:
#             return "HIGH"
#         elif score >= 0.3:
#             return "MEDIUM"
#         else:
#             return "LOW"
    
#     def _calculate_confidence(self, indicators: List) -> float:
#         """Calculate confidence based on number of indicators"""
#         if len(indicators) >= 3:
#             return 0.98
#         elif len(indicators) >= 1:
#             return 0.95
#         else:
#             return 0.90









"""Main Node 4 implementation."""
# app/agents/node4_fraud_agent/agent.py

import asyncio
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
import numpy as np

from .anomaly_detector import AnomalyDetector
from .document_comparison import DocumentComparer
from .duplicate_detector import DuplicateDetector
from .network_analyzer import NetworkAnalyzer
from .timing_analyzer import TimingAnalyzer
from .watchlist_checker import WatchlistChecker
from .explainability import FraudExplainer
from app.database.mongodb import get_collection, mongodb

class FraudDetectionAgent:
    """
    Node 4: Fraud Detection Agent
    Runs multiple parallel checks with high-accuracy ML models
    Now includes:
    - Anomaly Detection (ML + rule-based)
    - Document Comparison
    - Duplicate Detection (hashing + fuzzy)
    - Network Analysis (fraud rings)
    - Timing Analysis
    - Watchlist Checking
    - Explainable AI
    """
    
    def __init__(self):
        # Initialize all detectors
        self.anomaly_detector = AnomalyDetector()
        self.document_comparer = DocumentComparer()
        self.duplicate_detector = DuplicateDetector()
        self.network_analyzer = NetworkAnalyzer()
        self.timing_analyzer = TimingAnalyzer()
        self.watchlist_checker = WatchlistChecker()
        self.explainer = FraudExplainer()
        
        # MongoDB collections (lazy-loaded)
        self._claims_collection = None
        self._fraud_patterns = None
        self._hitl_collection = None

        # HITL thresholds
        self.manual_review_threshold = 0.20
        self.high_risk_threshold = 0.40
        self.critical_threshold = 0.70
        
        # Performance tracking
        self.processing_times = []
    
    @property
    def claims_collection(self):
        """Lazy-load claims collection"""
        if self._claims_collection is None:
            self._claims_collection = get_collection("claims")
        return self._claims_collection
    
    @property
    def fraud_patterns(self):
        """Lazy-load fraud patterns collection"""
        if self._fraud_patterns is None:
            self._fraud_patterns = get_collection("fraud_patterns")
        return self._fraud_patterns

    @property
    def hitl_collection(self):
        """Lazy-load HITL queue collection from dedicated HITL_db database."""
        if self._hitl_collection is None:
            if mongodb.client is None:
                raise RuntimeError("MongoDB client is not initialized. Call connect_to_mongo() first.")
            self._hitl_collection = mongodb.client["HITL_db"]["flagged_claims"]
        return self._hitl_collection
    
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point - runs all checks in parallel for maximum speed
        """
        start_time = time.time()
        
        # Extract data from state
        claim_data = {
            "claim_id": state.get("claim_id"),
            "claim_amount": state.get("claim_amount", 0),
            "incident_date": state.get("incident_date"),
            "submission_date": state.get("submission_date"),
            "policy_start_date": state.get("policy_start_date"),
            "claimant_name": state.get("claimant_name", ""),
            "claimant_id": state.get("claimant_id", ""),
            "provider_name": state.get("provider_name", ""),
            "provider_id": state.get("provider_id", ""),
            "attorney_name": state.get("attorney_name", ""),
            "attorney_id": state.get("attorney_id", ""),
            "documents": state.get("documents", []),
            "incident_type": state.get("incident_type", ""),
            "incident_location": state.get("incident_location", ""),
            "policy_type": state.get("policy_type", ""),
            "claimant_phone": state.get("claimant_phone", state.get("phone")),
            "claimant_email": state.get("claimant_email", state.get("email")),
            "claimant_address": state.get("claimant_address", state.get("address"))
        }
        
        # 🚀 RUN ALL CHECKS IN PARALLEL for maximum speed
        # 1. Anomaly Detection (ML + rule-based amount checks)
        anomaly_task = self.anomaly_detector.detect(claim_data)
        
        # 2. Document Comparison (cross-document consistency)
        document_task = self.document_comparer.compare(claim_data)
        
        # 3. Duplicate Detection (hash-based + fuzzy matching)
        duplicate_task = self.duplicate_detector.detect(claim_data)
        
        # 4. Network Analysis (fraud ring detection)
        network_task = self.network_analyzer.analyze(claim_data)
        
        # 5. Timing Analysis (early/late claim detection)
        timing_task = asyncio.to_thread(
            self.timing_analyzer.analyze_timing,
            claim_data.get("policy_start_date"),
            claim_data.get("incident_date"),
            claim_data.get("submission_date")
        )
        
        # 6. Watchlist Check (known fraudsters)
        watchlist_task = asyncio.to_thread(
            self.watchlist_checker.check_watchlist,
            claim_data.get("claimant_name", ""),
            claim_data.get("provider_name", "")
        )
        
        # Wait for all parallel tasks to complete
        anomaly_result, document_result, duplicate_result, network_result, timing_result, watchlist_result = await asyncio.gather(
            anomaly_task, document_task, duplicate_task, network_task, timing_task, watchlist_task,
            return_exceptions=True
        )
        
        # Handle any exceptions gracefully
        results = []
        for idx, result in enumerate([anomaly_result, document_result, duplicate_result, 
                                      network_result, timing_result, watchlist_result]):
            if isinstance(result, Exception):
                print(f"⚠️ Task {idx} failed: {result}")
                results.append({"score": 0.0, "indicators": []})
            else:
                results.append(result)
        
        anomaly_result, document_result, duplicate_result, network_result, timing_result, watchlist_result = results
        
        # Combine all fraud indicators
        all_indicators = []
        all_indicators.extend(anomaly_result.get("indicators", []))
        all_indicators.extend(document_result.get("indicators", []))
        all_indicators.extend(duplicate_result.get("indicators", []))
        all_indicators.extend(network_result.get("indicators", []))
        
        # Add timing indicators if present
        if timing_result and timing_result.get("is_suspicious"):
            all_indicators.append({
                "type": timing_result.get("type", "TIMING_ANOMALY"),
                "severity": timing_result.get("severity", "MEDIUM"),
                "details": timing_result.get("details", ""),
                "score_impact": timing_result.get("score_impact", 0),
                "confidence": timing_result.get("confidence", 0.9)
            })
        
        # Add watchlist indicators if present
        if watchlist_result and watchlist_result.get("on_watchlist"):
            all_indicators.append({
                "type": "WATCHLIST_MATCH",
                "severity": "CRITICAL",
                "details": watchlist_result.get("details", ""),
                "score_impact": watchlist_result.get("score_impact", 0.5),
                "confidence": 0.95
            })

        # Remove duplicate indicators from overlapping detectors
        all_indicators = self._deduplicate_indicators(all_indicators)
        
        # Calculate weighted fraud score
        fraud_score = (
            anomaly_result.get("score", 0) * 0.25 +
            document_result.get("score", 0) * 0.15 +
            duplicate_result.get("score", 0) * 0.20 +
            network_result.get("score", 0) * 0.15 +
            (timing_result.get("score_impact", 0) if timing_result and not isinstance(timing_result, Exception) else 0) * 0.15 +
            (watchlist_result.get("score_impact", 0) if watchlist_result and not isinstance(watchlist_result, Exception) else 0) * 0.10
        )
        
        # Cap at 1.0
        fraud_score = min(fraud_score, 1.0)
        
        # Generate explanations
        explanations = self.explainer.explain(
            fraud_score=fraud_score,
            indicators=all_indicators,
            claim_data=claim_data
        )
        
        # Determine risk level
        risk_level = self._get_risk_level(fraud_score)

        components = {
            "anomaly_score": anomaly_result.get("score", 0),
            "document_score": document_result.get("score", 0),
            "duplicate_score": duplicate_result.get("score", 0),
            "network_score": network_result.get("score", 0),
            "timing_detected": timing_result.get("is_suspicious", False) if timing_result and not isinstance(timing_result, Exception) else False,
            "watchlist_match": watchlist_result.get("on_watchlist", False) if watchlist_result and not isinstance(watchlist_result, Exception) else False
        }

        # Determine if claim needs manual investigation
        requires_investigation = self._should_flag_for_hitl(fraud_score, all_indicators)

        # Persist flagged claims to HITL queue
        if requires_investigation:
            await self._store_hitl_claim(
                state=state,
                fraud_score=fraud_score,
                risk_level=risk_level,
                indicators=all_indicators,
                explanations=explanations,
                components=components,
            )
        
        # Track performance
        processing_time = time.time() - start_time
        self.processing_times.append(processing_time)
        
        return {
            "fraud_analysis": {
                "fraud_score": round(fraud_score, 3),
                "risk_level": risk_level,
                "requires_investigation": requires_investigation,
                "fraud_indicators": all_indicators,
                "explanations": explanations,
                "processing_time_ms": round(processing_time * 1000, 2),
                "confidence": self._calculate_confidence(all_indicators),
                "components": components
            }
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Convert score to risk level"""
        if score >= self.critical_threshold:
            return "CRITICAL"
        elif score >= self.high_risk_threshold:
            return "HIGH"
        elif score >= self.manual_review_threshold:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_confidence(self, indicators: List) -> float:
        """Calculate confidence based on number of indicators"""
        if len(indicators) >= 3:
            return 0.98
        elif len(indicators) >= 1:
            return 0.95
        else:
            return 0.90

    def _should_flag_for_hitl(self, fraud_score: float, indicators: List[Dict[str, Any]]) -> bool:
        """Decide whether a claim must be sent to manual review (HITL)."""
        if fraud_score >= self.manual_review_threshold:
            return True

        high_priority_types = {"WATCHLIST_MATCH", "EXACT_DUPLICATE", "NETWORK_RING_DETECTED"}
        for indicator in indicators:
            if indicator.get("severity") in {"HIGH", "CRITICAL"}:
                return True
            if indicator.get("type") in high_priority_types:
                return True

        return False

    async def _store_hitl_claim(
        self,
        state: Dict[str, Any],
        fraud_score: float,
        risk_level: str,
        indicators: List[Dict[str, Any]],
        explanations: Any,
        components: Dict[str, Any],
    ) -> None:
        """Store flagged claim in HITL_db.flagged_claims for manual underwriter review."""
        try:
            claim_id = state.get("claim_id")
            if not claim_id:
                return

            indicator_breakdown = []
            for indicator in indicators:
                indicator_breakdown.append({
                    "type": indicator.get("type"),
                    "severity": indicator.get("severity", "MEDIUM"),
                    "details": indicator.get("details", ""),
                    "score_impact": indicator.get("score_impact", 0),
                    "confidence": indicator.get("confidence"),
                })

            hitl_triggers = []
            if fraud_score >= self.manual_review_threshold:
                hitl_triggers.append(
                    f"Fraud score {round(fraud_score, 3)} crossed manual review threshold {self.manual_review_threshold}"
                )

            for indicator in indicators:
                if indicator.get("severity") in {"HIGH", "CRITICAL"}:
                    hitl_triggers.append(
                        f"{indicator.get('severity')} severity indicator: {indicator.get('type')}"
                    )

            policy_analysis = state.get("policy_analysis", {})
            reasoning_summary = {
                "why_in_hitl": "Claim matched fraud-risk escalation rules and needs human verification.",
                "fraud_score_reason": f"Computed fraud score is {round(fraud_score, 3)} with risk level {risk_level}.",
                "policy_context": {
                    "is_covered": policy_analysis.get("is_covered"),
                    "coverage_score": policy_analysis.get("coverage_score"),
                    "exclusions_triggered": policy_analysis.get("exclusions_triggered", []),
                },
                "trigger_rules": hitl_triggers,
                "indicator_count": len(indicator_breakdown),
            }

            document = {
                "claim_id": claim_id,
                "policy_number": state.get("policy_number"),
                "claim_amount": state.get("claim_amount"),
                "claimant_name": state.get("claimant_name"),
                "provider_name": state.get("provider_name"),
                "fraud_score": round(fraud_score, 3),
                "risk_level": risk_level,
                "status": "PENDING_REVIEW",
                "flag_reason": "Automatic fraud threshold/indicator trigger",
                "fraud_indicators": indicators,
                "reasoning": {
                    "summary": reasoning_summary,
                    "indicator_breakdown": indicator_breakdown,
                    "component_scores": components,
                    "model_explanations": explanations,
                    "recommended_actions": [
                        "Verify claimant and provider identities",
                        "Review supporting documents for consistency",
                        "Confirm incident timeline with external records",
                        "Approve only after manual underwriter sign-off",
                    ],
                },
                "policy_analysis": state.get("policy_analysis", {}),
                "source": "node4_fraud_agent",
                "updated_at": datetime.utcnow().isoformat(),
            }

            await self.hitl_collection.update_one(
                {"claim_id": claim_id},
                {"$set": document, "$setOnInsert": {"created_at": datetime.utcnow().isoformat()}},
                upsert=True,
            )
        except Exception as exc:
            print(f"⚠️ Failed to store HITL claim: {exc}")

    def _deduplicate_indicators(self, indicators: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate indicators by type + details, keeping highest score impact."""
        deduped: Dict[tuple, Dict[str, Any]] = {}

        for indicator in indicators:
            key = (indicator.get("type"), indicator.get("details"))
            if key not in deduped:
                deduped[key] = indicator
                continue

            existing_impact = deduped[key].get("score_impact", 0)
            new_impact = indicator.get("score_impact", 0)
            if new_impact > existing_impact:
                deduped[key] = indicator

        return list(deduped.values())
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics"""
        if not self.processing_times:
            return {"avg_processing_time": 0, "min_time": 0, "max_time": 0, "total_processed": 0}
        
        return {
            "avg_processing_time": sum(self.processing_times) / len(self.processing_times),
            "min_time": min(self.processing_times),
            "max_time": max(self.processing_times),
            "total_processed": len(self.processing_times)
        }
"""Amount anomaly detection with enhanced rule-based checks."""
# app/agents/node4_fraud_agent/anomaly_detector.py

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import xgboost as xgb
import joblib
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
import os
from pathlib import Path

class AnomalyDetector:
    """
    High-accuracy anomaly detection using Isolation Forest + XGBoost + Rule-based
    Now includes enhanced amount anomaly detection
    """
    
    def __init__(self, model_path: Optional[str] = None):
        # Set default model path if not provided
        if model_path is None:
            base_dir = Path(__file__).parent
            self.multi_type_model_path = base_dir / "ml_models" / "fraud_model_multi_type.pkl"
            self.generic_model_path = base_dir / "ml_models" / "fraud_model.pkl"
            
            if self.multi_type_model_path.exists():
                self.model_path = str(self.multi_type_model_path)
                print(f"✅ Using multi-type fraud model: {self.multi_type_model_path}")
            elif self.generic_model_path.exists():
                self.model_path = str(self.generic_model_path)
                print(f"✅ Using generic fraud model: {self.generic_model_path}")
            else:
                self.model_path = None
                print("⚠️ No pre-trained model found. Using rule-based detection only.")
        else:
            self.model_path = model_path
        
        # Isolation Forest
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100,
            max_samples='auto',
            warm_start=True
        )
        
        # Load pre-trained XGBoost model
        self.xgboost_model = None
        self.model_features = None
        self.model_scaler = None
        self.label_encoders = None
        self.model_metadata = {}
        
        if self.model_path and os.path.exists(self.model_path):
            try:
                artifacts = joblib.load(self.model_path)
                
                if isinstance(artifacts, dict):
                    self.xgboost_model = artifacts.get('model')
                    self.model_features = artifacts.get('feature_names')
                    self.model_scaler = artifacts.get('scaler')
                    self.label_encoders = artifacts.get('label_encoders', {})
                    self.model_metadata = {
                        'training_date': artifacts.get('training_date', 'Unknown'),
                        'dataset': artifacts.get('dataset', 'Unknown'),
                        'metrics': artifacts.get('metrics', {})
                    }
                else:
                    self.xgboost_model = artifacts
                    self.model_features = None
                    self.model_scaler = None
                
                if self.xgboost_model:
                    print(f"✅ Loaded fraud detection model from {self.model_path}")
                    if 'metrics' in self.model_metadata:
                        metrics = self.model_metadata['metrics']
                        print(f"   Model ROC-AUC: {metrics.get('roc_auc', 'N/A')}")
            except Exception as e:
                print(f"⚠️ Could not load ML model: {e}")
                self.xgboost_model = None
        
        # ============================================================
        # ENHANCED AMOUNT ANOMALY THRESHOLDS
        # ============================================================
        self.amount_thresholds = {
            'low': [10000, 25000, 50000],
            'medium': [100000, 250000, 500000],
            'high': [1000000, 2500000, 5000000, 10000000]
        }
        
        # Percentage thresholds for amount comparison
        self.amount_variance_threshold = 0.20  # 20% variance allowed
        self.suspicious_rounding_threshold = 10000  # Round numbers above this
        
        # Benford's Law expected frequencies
        self.benford_expected = {
            1: 0.301, 2: 0.176, 3: 0.125, 4: 0.097,
            5: 0.079, 6: 0.067, 7: 0.058, 8: 0.051, 9: 0.046
        }
        
        # Timing thresholds
        self.early_claim_days = 7
        self.late_report_days = 30
        self.very_late_report_days = 90
        
        # Track state
        self.isolation_forest_fitted = False
        self.training_data_buffer = []
    
    async def detect(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect anomalies using multiple techniques
        """
        indicators = []
        score = 0.0
        
        # 1. ENHANCED AMOUNT ANOMALY DETECTION
        amount_score, amount_indicators = self._check_amount_anomalies(claim_data)
        score += amount_score
        indicators.extend(amount_indicators)
        
        # 2. Timing anomaly (existing)
        timing_score, timing_indicator = self._check_timing_anomaly(
            policy_start=claim_data.get("policy_start_date"),
            incident_date=claim_data.get("incident_date"),
            submission_date=claim_data.get("submission_date")
        )
        score += timing_score
        if timing_indicator:
            indicators.append(timing_indicator)
        
        # 3. ML-based anomaly detection
        if self.xgboost_model:
            ml_score, ml_indicator = await self._check_ml_anomaly(claim_data)
            score += ml_score
            if ml_indicator:
                indicators.append(ml_indicator)
        
        # 4. Benford's Law analysis
        benford_score, benford_indicator = self._check_benford_law(claim_data)
        score += benford_score
        if benford_indicator:
            indicators.append(benford_indicator)
        
        # 5. Isolation Forest
        if len(self.training_data_buffer) > 10:
            iso_score, iso_indicator = self._check_isolation_forest(claim_data)
            score += iso_score * 0.2
            if iso_indicator:
                indicators.append(iso_indicator)
        
        # Add to training buffer
        self._add_to_training_buffer(claim_data)
        
        return {
            "score": min(score, 0.5),
            "indicators": indicators
        }
    
    # ============================================================
    # ENHANCED AMOUNT ANOMALY DETECTION
    # ============================================================
    
    def _check_amount_anomalies(self, claim_data: Dict) -> Tuple[float, List[Dict]]:
        """
        Comprehensive amount anomaly detection
        Checks multiple patterns:
        1. Amounts just below thresholds
        2. Round number anomalies
        3. Amount variance in documents
        4. Unusual first digits (Benford's Law)
        """
        indicators = []
        total_score = 0.0
        
        claim_amount = claim_data.get("claim_amount", 0)
        
        if claim_amount <= 0:
            return 0.0, []
        
        # 1. Check for amounts just below common thresholds
        threshold_score, threshold_indicator = self._check_threshold_anomaly(claim_amount)
        total_score += threshold_score
        if threshold_indicator:
            indicators.append(threshold_indicator)
        
        # 2. Check for suspicious round numbers
        round_score, round_indicator = self._check_round_number_anomaly(claim_amount)
        total_score += round_score
        if round_indicator:
            indicators.append(round_indicator)
        
        # 3. Check for amount consistency across documents
        doc_score, doc_indicator = self._check_document_amount_consistency(claim_data)
        total_score += doc_score
        if doc_indicator:
            indicators.append(doc_indicator)
        
        # 4. Check for unusual first digit (Benford's Law)
        benford_score, benford_indicator = self._check_single_amount_benford(claim_amount)
        total_score += benford_score
        if benford_indicator:
            indicators.append(benford_indicator)
        
        return total_score, indicators
    
    def _check_threshold_anomaly(self, amount: float) -> Tuple[float, Optional[Dict]]:
        """Check if amount is suspiciously just below common thresholds"""
        for level, thresholds in self.amount_thresholds.items():
            for threshold in thresholds:
                # Check if amount is within 2% below threshold
                if threshold * 0.98 < amount < threshold:
                    severity = "HIGH" if level == "high" else "MEDIUM" if level == "medium" else "LOW"
                    score_impact = 0.25 if level == "high" else 0.2 if level == "medium" else 0.15
                    
                    return score_impact, {
                        "type": "THRESHOLD_ANOMALY",
                        "severity": severity,
                        "details": f"Amount ₹{amount:,.0f} is suspiciously close to ₹{threshold:,.0f} {level.upper()} limit",
                        "confidence": 0.95,
                        "score_impact": score_impact,
                        "threshold": threshold,
                        "level": level
                    }
        
        return 0.0, None
    
    def _check_round_number_anomaly(self, amount: float) -> Tuple[float, Optional[Dict]]:
        """Check for suspicious round numbers"""
        if amount > self.suspicious_rounding_threshold:
            # Check if amount is a round number (ends with 000, 0000)
            if amount % 1000 == 0:
                return 0.15, {
                    "type": "ROUND_NUMBER_ANOMALY",
                    "severity": "MEDIUM",
                    "details": f"Round number amount ₹{amount:,.0f} may indicate padding",
                    "confidence": 0.80,
                    "score_impact": 0.15,
                    "rounding_factor": 1000
                }
            elif amount % 10000 == 0:
                return 0.2, {
                    "type": "ROUND_NUMBER_ANOMALY",
                    "severity": "HIGH",
                    "details": f"Large round number amount ₹{amount:,.0f} strongly indicates padding",
                    "confidence": 0.90,
                    "score_impact": 0.2,
                    "rounding_factor": 10000
                }
        
        return 0.0, None
    
    def _check_document_amount_consistency(self, claim_data: Dict) -> Tuple[float, Optional[Dict]]:
        """Check if amounts across documents are consistent"""
        claim_amount = claim_data.get("claim_amount", 0)
        documents = claim_data.get("documents", [])
        
        if not documents or claim_amount == 0:
            return 0.0, None
        
        doc_amounts = []
        for doc in documents:
            # Try to extract amount from document content (simplified)
            content = doc.get("content", "")
            # Look for amount patterns (simplified - in production use regex)
            if "₹" in content:
                # Very simplified - would need proper parsing in production
                doc_amounts.append(claim_amount * 0.9)  # Mock for demo
        
        if doc_amounts:
            avg_doc_amount = sum(doc_amounts) / len(doc_amounts)
            variance = abs(claim_amount - avg_doc_amount) / avg_doc_amount
            
            if variance > self.amount_variance_threshold:
                return 0.2, {
                    "type": "AMOUNT_INCONSISTENCY",
                    "severity": "HIGH",
                    "details": f"Claim amount ₹{claim_amount:,.0f} differs from document average ₹{avg_doc_amount:,.0f} by {variance:.1%}",
                    "confidence": 0.85,
                    "score_impact": 0.2,
                    "variance": variance
                }
        
        return 0.0, None
    
    def _check_single_amount_benford(self, amount: float) -> Tuple[float, Optional[Dict]]:
        """Apply Benford's Law to single amount"""
        if amount <= 0:
            return 0.0, None
        
        # Get first digit
        first_digit = int(str(abs(int(amount)))[0])
        
        # Check if first digit is statistically rare
        if first_digit in [8, 9] and self.benford_expected[first_digit] < 0.06:
            return 0.15, {
                "type": "BENFORD_ANOMALY",
                "severity": "MEDIUM",
                "details": f"Amount starts with digit {first_digit} which is statistically rare ({self.benford_expected[first_digit]*100:.1f}% expected)",
                "confidence": 0.75,
                "score_impact": 0.15,
                "first_digit": first_digit,
                "expected_frequency": self.benford_expected[first_digit]
            }
        
        return 0.0, None
    
    def _check_benford_law(self, claim_data: Dict) -> Tuple[float, Optional[Dict]]:
        """Check multiple amounts using Benford's Law (if available)"""
        # Simplified - would need historical amounts in production
        return 0.0, None
    
    # ============================================================
    # EXISTING METHODS (keep as is)
    # ============================================================
    
    def _check_timing_anomaly(self, policy_start: Optional[str], 
                              incident_date: Optional[str], 
                              submission_date: Optional[str]) -> Tuple[float, Optional[Dict]]:
        """Detect suspicious timing patterns in claims"""
        if not all([policy_start, incident_date, submission_date]):
            return 0.0, None
        
        try:
            policy = self._parse_date(policy_start)
            incident = self._parse_date(incident_date)
            submission = self._parse_date(submission_date)
            
            if not all([policy, incident, submission]):
                return 0.0, None
            
            days_since_policy = (incident - policy).days
            days_to_report = (submission - incident).days
            
            # Early claim (within 7 days of policy)
            if days_since_policy < self.early_claim_days:
                return 0.25, {
                    "type": "EARLY_CLAIM",
                    "severity": "HIGH",
                    "details": f"Claim filed {days_since_policy} days after policy start",
                    "confidence": 0.98,
                    "score_impact": 0.25,
                    "days": days_since_policy
                }
            
            # Late reporting (30-90 days)
            if self.late_report_days < days_to_report <= self.very_late_report_days:
                return 0.15, {
                    "type": "LATE_REPORTING",
                    "severity": "MEDIUM",
                    "details": f"Claim reported {days_to_report} days after incident",
                    "confidence": 0.90,
                    "score_impact": 0.15,
                    "days": days_to_report
                }
            
            # Very late reporting (>90 days)
            if days_to_report > self.very_late_report_days:
                return 0.25, {
                    "type": "VERY_LATE_REPORTING",
                    "severity": "HIGH",
                    "details": f"Claim reported {days_to_report} days after incident (extremely late)",
                    "confidence": 0.95,
                    "score_impact": 0.25,
                    "days": days_to_report
                }
            
            return 0.0, None
            
        except Exception as e:
            print(f"⚠️ Timing analysis error: {e}")
            return 0.0, None
    
    def _parse_date(self, date_str: str):
        """Parse date string in various formats"""
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            try:
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
                    try:
                        return datetime.strptime(date_str, fmt)
                    except:
                        continue
            except:
                pass
        return None
    
    async def _check_ml_anomaly(self, claim_data: Dict) -> Tuple[float, Optional[Dict]]:
        """Use XGBoost model for fraud prediction"""
        if not self.xgboost_model:
            return 0.0, None
        
        try:
            features = self._extract_ml_features(claim_data)
            
            if features is None:
                return 0.0, None
            
            if hasattr(self.xgboost_model, 'predict_proba'):
                proba = self.xgboost_model.predict_proba([features])[0]
                fraud_prob = proba[1] if len(proba) > 1 else proba[0]
            else:
                pred = self.xgboost_model.predict([features])[0]
                fraud_prob = float(pred)
            
            if fraud_prob > 0.8:
                return 0.3, {
                    "type": "ML_HIGH_RISK",
                    "severity": "CRITICAL",
                    "details": f"ML model predicts {fraud_prob:.1%} fraud probability",
                    "confidence": fraud_prob,
                    "score_impact": 0.3
                }
            elif fraud_prob > 0.5:
                return 0.2, {
                    "type": "ML_MEDIUM_RISK",
                    "severity": "HIGH",
                    "details": f"ML model predicts {fraud_prob:.1%} fraud probability",
                    "confidence": fraud_prob,
                    "score_impact": 0.2
                }
            
            return 0.0, None
            
        except Exception as e:
            print(f"⚠️ ML prediction failed: {e}")
            return 0.0, None
    
    def _extract_ml_features(self, claim_data: Dict) -> Optional[List]:
        """Extract features for ML model"""
        if self.model_features:
            features = []
            for feature_name in self.model_features:
                value = self._get_feature_value(claim_data, feature_name)
                features.append(value)
            return features
        else:
            return self._extract_generic_features(claim_data)
    
    def _get_feature_value(self, claim_data: Dict, feature_name: str) -> float:
        """Extract a specific feature value"""
        feature_mappings = {
            'claim_amount': lambda d: d.get('claim_amount', 0),
            'days_since_policy': lambda d: self._calculate_days_since_policy(d),
            'days_to_report': lambda d: self._calculate_days_to_report(d),
            'document_count': lambda d: len(d.get('documents', [])),
            'round_amount_flag': lambda d: 1 if d.get('claim_amount', 0) % 10000 == 0 else 0,
            'provider_volume': lambda d: 0,
            'claimant_history': lambda d: 0,
            'network_density': lambda d: 0,
            'exclusions_count': lambda d: 0,
            'deductible': lambda d: d.get('deductible', 0),
            'policy_type_encoded': lambda d: self._encode_policy_type(d.get('policy_type', '')),
        }
        
        extractor = feature_mappings.get(feature_name, lambda d: 0)
        try:
            return float(extractor(claim_data))
        except:
            return 0.0
    
    def _calculate_days_since_policy(self, claim_data: Dict) -> float:
        try:
            policy_start = self._parse_date(claim_data.get('policy_start_date', ''))
            incident_date = self._parse_date(claim_data.get('incident_date', ''))
            
            if policy_start and incident_date:
                days = (incident_date - policy_start).days
                return min(max(days, 0), 365) / 365
        except:
            pass
        return 0.5
    
    def _calculate_days_to_report(self, claim_data: Dict) -> float:
        try:
            incident_date = self._parse_date(claim_data.get('incident_date', ''))
            submission_date = self._parse_date(claim_data.get('submission_date', ''))
            
            if incident_date and submission_date:
                days = (submission_date - incident_date).days
                return min(max(days, 0), 365) / 365
        except:
            pass
        return 0.5
    
    def _encode_policy_type(self, policy_type: str) -> float:
        type_mapping = {
            'motor': 0, 'auto': 0, 'car': 0, 'vehicle': 0,
            'health': 1, 'medical': 1,
            'property': 2, 'home': 2, 'house': 2,
            'life': 3, 'travel': 4, 'pet': 5, 'business': 6, 'cyber': 7
        }
        
        policy_lower = policy_type.lower() if policy_type else ''
        for key, value in type_mapping.items():
            if key in policy_lower:
                return value
        return 0
    
    def _extract_generic_features(self, claim_data: Dict) -> List:
        features = []
        
        amount = claim_data.get("claim_amount", 0)
        features.append(amount / 100000)
        features.append(1 if amount % 10000 == 0 else 0)
        
        try:
            incident = datetime.fromisoformat(claim_data.get("incident_date", "").replace('Z', '+00:00'))
            submission = datetime.fromisoformat(claim_data.get("submission_date", "").replace('Z', '+00:00'))
            policy = datetime.fromisoformat(claim_data.get("policy_start_date", "").replace('Z', '+00:00'))
            
            days_to_report = (submission - incident).days
            days_since_policy = (incident - policy).days
            
            features.append(min(days_to_report, 365) / 365)
            features.append(min(days_since_policy, 365) / 365)
        except:
            features.append(0.5)
            features.append(0.5)
        
        doc_count = len(claim_data.get("documents", []))
        features.append(min(doc_count, 20) / 20)
        
        policy_type = claim_data.get("policy_type", "")
        features.append(self._encode_policy_type(policy_type) / 7)
        
        return features
    
    def _check_isolation_forest(self, claim_data: Dict) -> Tuple[float, Optional[Dict]]:
        features = self._extract_generic_features(claim_data)
        X = np.array([features])
        
        self.training_data_buffer.append(features)
        if len(self.training_data_buffer) > 1000:
            self.training_data_buffer = self.training_data_buffer[-1000:]
        
        if len(self.training_data_buffer) >= 50 and not self.isolation_forest_fitted:
            X_train = np.array(self.training_data_buffer)
            self.isolation_forest.fit(X_train)
            self.isolation_forest_fitted = True
        
        if not self.isolation_forest_fitted:
            return 0.0, None
        
        try:
            pred = self.isolation_forest.predict(X)
            
            if pred[0] == -1:
                return 0.15, {
                    "type": "ISOLATION_FOREST_ANOMALY",
                    "severity": "HIGH",
                    "details": "Statistical outlier detected by Isolation Forest",
                    "confidence": 0.85,
                    "score_impact": 0.15
                }
        except:
            pass
        
        return 0.0, None
    
    def _add_to_training_buffer(self, claim_data: Dict):
        features = self._extract_generic_features(claim_data)
        self.training_data_buffer.append(features)
        if len(self.training_data_buffer) > 1000:
            self.training_data_buffer = self.training_data_buffer[-1000:]
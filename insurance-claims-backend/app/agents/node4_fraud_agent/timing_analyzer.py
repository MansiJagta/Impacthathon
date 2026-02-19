"""Suspicious timing detection."""
"""Timing analysis for fraud detection."""
# app/agents/node4_fraud_agent/timing_analyzer.py

from datetime import datetime
from typing import Dict, Tuple, Optional

class TimingAnalyzer:
    """
    Analyzes claim timing patterns for fraud indicators
    Detects:
    - Early claims (filed too soon after policy start)
    - Late reporting (filed too long after incident)
    - Holiday/weekend claims
    - Unusual timing patterns
    """
    
    def __init__(self):
        # Thresholds in days
        self.early_claim_days = 7
        self.late_report_days = 30
        self.very_late_report_days = 90
        
        # Suspicious hours (10 PM - 5 AM)
        self.suspicious_hours = list(range(22, 24)) + list(range(0, 5))
    
    def analyze_timing(self, policy_start: Optional[str], 
                       incident_date: Optional[str], 
                       submission_date: Optional[str]) -> Dict:
        """
        Analyze timing patterns for fraud indicators
        
        Args:
            policy_start: Policy start date (ISO format)
            incident_date: Date of incident (ISO format)
            submission_date: Date claim was filed (ISO format)
            
        Returns:
            Dict with is_suspicious flag, severity, and details
        """
        result = {
            "is_suspicious": False,
            "severity": "LOW",
            "score_impact": 0.0,
            "details": "",
            "type": None,
            "confidence": 0.0
        }
        
        if not all([policy_start, incident_date, submission_date]):
            return result
        
        try:
            # Parse dates
            policy = self._parse_date(policy_start)
            incident = self._parse_date(incident_date)
            submission = self._parse_date(submission_date)
            
            if not all([policy, incident, submission]):
                return result
            
            # Calculate differences
            days_since_policy = (incident - policy).days
            days_to_report = (submission - incident).days
            report_hour = submission.hour
            
            # Check 1: Early claim (within 7 days of policy)
            if days_since_policy < self.early_claim_days:
                result.update({
                    "is_suspicious": True,
                    "severity": "HIGH",
                    "score_impact": 0.25,
                    "type": "EARLY_CLAIM",
                    "details": f"Claim filed {days_since_policy} days after policy start",
                    "confidence": 0.98,
                    "days": days_since_policy
                })
                return result
            
            # Check 2: Late reporting (30-90 days)
            if self.late_report_days < days_to_report <= self.very_late_report_days:
                result.update({
                    "is_suspicious": True,
                    "severity": "MEDIUM",
                    "score_impact": 0.15,
                    "type": "LATE_REPORTING",
                    "details": f"Claim reported {days_to_report} days after incident",
                    "confidence": 0.90,
                    "days": days_to_report
                })
                return result
            
            # Check 3: Very late reporting (>90 days)
            if days_to_report > self.very_late_report_days:
                result.update({
                    "is_suspicious": True,
                    "severity": "HIGH",
                    "score_impact": 0.25,
                    "type": "VERY_LATE_REPORTING",
                    "details": f"Claim reported {days_to_report} days after incident (extremely late)",
                    "confidence": 0.95,
                    "days": days_to_report
                })
                return result
            
            # Check 4: Suspicious hour (late night/early morning)
            if report_hour in self.suspicious_hours:
                result.update({
                    "is_suspicious": True,
                    "severity": "MEDIUM",
                    "score_impact": 0.1,
                    "type": "SUSPICIOUS_HOUR",
                    "details": f"Claim filed at {report_hour}:00 - unusual hour",
                    "confidence": 0.70,
                    "hour": report_hour
                })
                return result
            
            # Check 5: Weekend claim (Saturday/Sunday)
            if submission.weekday() >= 5:  # 5=Saturday, 6=Sunday
                result.update({
                    "is_suspicious": True,
                    "severity": "LOW",
                    "score_impact": 0.05,
                    "type": "WEEKEND_CLAIM",
                    "details": f"Claim filed on {submission.strftime('%A')}",
                    "confidence": 0.60,
                    "day": submission.strftime('%A')
                })
                return result
            
        except Exception as e:
            print(f"⚠️ Timing analysis error: {e}")
        
        return result
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string in various formats"""
        try:
            # Try ISO format first
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            try:
                # Try common formats
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%dT%H:%M:%S']:
                    try:
                        return datetime.strptime(date_str, fmt)
                    except:
                        continue
            except:
                pass
        return None
    
    def get_timing_score(self, days_since_policy: int, days_to_report: int) -> float:
        """Calculate a normalized timing score (0-1)"""
        score = 0.0
        
        # Early claims get higher scores
        if days_since_policy < 7:
            score += 0.3 * (1 - days_since_policy/7)
        
        # Late claims get higher scores
        if days_to_report > 30:
            score += min(0.3, (days_to_report - 30) / 200)
        
        return min(score, 0.5)
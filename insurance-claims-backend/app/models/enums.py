from enum import Enum


class Status(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

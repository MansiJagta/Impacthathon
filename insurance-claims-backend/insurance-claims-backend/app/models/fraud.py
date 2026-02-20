from pydantic import BaseModel


class FraudResult(BaseModel):
    risk_score: float
    reasons: list[str] = []

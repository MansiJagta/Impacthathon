from pydantic import BaseModel


class Claim(BaseModel):
    claim_id: str
    policy_id: str
    amount: float

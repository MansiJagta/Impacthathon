from sklearn.ensemble import RandomForestRegressor
import numpy as np
from database import historical_claims


def train_model():
    data = list(historical_claims.find({}))

    if not data:
        print("No training data found. Using dummy model.")
        # Fallback to a dummy model if database is empty
        X = [[100000, 500, 0.1], [200000, 1000, 0.5]]
        y = [50000, 150000]
    else:
        X = []
        y = []
        for claim in data:
            X.append(
                [
                    claim.get("policy_limit", 0),
                    claim.get("deductible", 0),
                    claim.get("fraud_score", 0),
                ]
            )
            y.append(claim.get("final_cost", 0))

    model = RandomForestRegressor()
    model.fit(X, y)
    return model

import os
from pathlib import Path

import joblib
import numpy as np


MODEL_PATH_ENV = "FRAUD_MODEL_PATH"


def _default_model_path():
    return Path(__file__).resolve().parents[2] / "models" / "fraud_model.pkl"


def _resolve_model_path():
    configured_path = os.getenv(MODEL_PATH_ENV)
    if configured_path:
        return Path(configured_path)
    return _default_model_path()


def _load_model():
    model_path = _resolve_model_path()
    if not model_path.exists() or model_path.stat().st_size == 0:
        return None
    try:
        return joblib.load(model_path)
    except Exception:
        return None


def anomaly_score(amount, days_since_policy):
    model = _load_model()
    if model is None:
        return 0

    features = np.array([[amount, days_since_policy]], dtype=float)
    prediction = model.predict(features)
    return 1 if int(prediction[0]) == -1 else 0
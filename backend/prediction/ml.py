"""
Loads the trained scikit-learn pipelines and exposes a clean predict_* API
for the DRF views to call. Models are loaded once per process (module-level
cache) to avoid disk I/O on every request.
"""

import os
import joblib
import pandas as pd

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "ml_models")

_cache = {}


def _load(filename):
    if filename not in _cache:
        path = os.path.join(MODEL_DIR, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Model file '{filename}' not found. Run `python prediction/train_models.py` first."
            )
        _cache[filename] = joblib.load(path)
    return _cache[filename]


def _risk_label(score: float) -> str:
    if score < 0.3:
        return "Low"
    if score < 0.6:
        return "Moderate"
    return "High"


def predict_diabetes(data: dict) -> dict:
    bundle = _load("diabetes_model.joblib")
    pipeline, features = bundle["pipeline"], bundle["features"]
    row = pd.DataFrame([[data[f] for f in features]], columns=features)
    score = float(pipeline.predict_proba(row)[0][1])
    return {"risk_score": round(score, 4), "risk_label": _risk_label(score), "features_used": features}


def predict_heart_disease(data: dict) -> dict:
    bundle = _load("heart_disease_model.joblib")
    pipeline, features = bundle["pipeline"], bundle["features"]
    row = pd.DataFrame([[data[f] for f in features]], columns=features)
    score = float(pipeline.predict_proba(row)[0][1])
    return {"risk_score": round(score, 4), "risk_label": _risk_label(score), "features_used": features}

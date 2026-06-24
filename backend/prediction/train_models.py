"""
Trains small, real scikit-learn classifiers for diabetes and heart-disease
risk, on synthetic-but-medically-plausible data, and saves them as .joblib
files. Run this once via `python prediction/train_models.py` (or wire it
into a management command) to generate the model artifacts used by
prediction/ml.py.

IMPORTANT: These are demo models trained on synthetic data for scaffolding
purposes only. Replace with models trained on real, properly licensed
clinical datasets (e.g. Pima Indians Diabetes, UCI Heart Disease) before
using this for anything beyond a prototype.
"""

import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

MODEL_DIR = os.path.join(os.path.dirname(__file__), "ml_models")
os.makedirs(MODEL_DIR, exist_ok=True)

RNG = np.random.RandomState(42)


def _make_diabetes_dataset(n=1500):
    age = RNG.randint(18, 85, n)
    bmi = RNG.normal(27, 5, n).clip(15, 50)
    glucose = RNG.normal(110, 30, n).clip(60, 300)
    blood_pressure = RNG.normal(75, 12, n).clip(40, 130)
    family_history = RNG.binomial(1, 0.3, n)

    # Logistic combination -> probability -> binary label (synthetic ground truth)
    z = (
        -8
        + 0.03 * age
        + 0.12 * bmi
        + 0.045 * glucose
        + 0.02 * blood_pressure
        + 1.1 * family_history
    )
    prob = 1 / (1 + np.exp(-z))
    label = RNG.binomial(1, prob)

    return pd.DataFrame({
        "age": age, "bmi": bmi, "glucose": glucose,
        "blood_pressure": blood_pressure, "family_history": family_history,
        "label": label,
    })


def _make_heart_dataset(n=1500):
    age = RNG.randint(25, 85, n)
    cholesterol = RNG.normal(200, 35, n).clip(120, 350)
    resting_bp = RNG.normal(125, 15, n).clip(90, 200)
    max_heart_rate = RNG.normal(150, 20, n).clip(80, 210)
    smoker = RNG.binomial(1, 0.25, n)
    diabetic = RNG.binomial(1, 0.15, n)

    z = (
        -9
        + 0.045 * age
        + 0.02 * cholesterol
        + 0.03 * resting_bp
        - 0.02 * max_heart_rate
        + 1.3 * smoker
        + 0.9 * diabetic
    )
    prob = 1 / (1 + np.exp(-z))
    label = RNG.binomial(1, prob)

    return pd.DataFrame({
        "age": age, "cholesterol": cholesterol, "resting_bp": resting_bp,
        "max_heart_rate": max_heart_rate, "smoker": smoker, "diabetic": diabetic,
        "label": label,
    })


def train_and_save(df, feature_cols, filename):
    X = df[feature_cols]
    y = df["label"]
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000)),
    ])
    pipeline.fit(X, y)
    path = os.path.join(MODEL_DIR, filename)
    joblib.dump({"pipeline": pipeline, "features": feature_cols}, path)
    print(f"Saved {filename} (train accuracy: {pipeline.score(X, y):.3f})")
    return pipeline


if __name__ == "__main__":
    diabetes_df = _make_diabetes_dataset()
    train_and_save(
        diabetes_df,
        ["age", "bmi", "glucose", "blood_pressure", "family_history"],
        "diabetes_model.joblib",
    )

    heart_df = _make_heart_dataset()
    train_and_save(
        heart_df,
        ["age", "cholesterol", "resting_bp", "max_heart_rate", "smoker", "diabetic"],
        "heart_disease_model.joblib",
    )

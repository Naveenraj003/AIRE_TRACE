"""
AIRE-Trace Tabular Logistic Regression Baseline (M1)
Logistic Regression over normalized Category A baseline features.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

class LogisticBaseline:
    def __init__(
        self,
        model_id: str = "M1",
        feature_cols: List[str] = None,
        C: float = 1.0,
        random_state: int = 42
    ):
        self.model_id = model_id
        self.feature_cols = feature_cols
        self.C = C
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.model = LogisticRegression(
            C=self.C,
            solver="lbfgs",
            max_iter=1000,
            random_state=self.random_state
        )
        self.is_fitted = False

    def fit(self, df_train: pd.DataFrame, y_train: np.ndarray, sample_weight: np.ndarray = None):
        """Fits scaler and LogisticRegression model on TRAIN data only."""
        if self.feature_cols is None:
            self.feature_cols = [c for c in df_train.columns if c.startswith("feat_")]

        X_train = df_train[self.feature_cols].values
        X_train_scaled = self.scaler.fit_transform(X_train)

        self.model.fit(X_train_scaled, y_train, sample_weight=sample_weight)
        self.is_fitted = True

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        """Returns predicted probability of eventual failure (class 1)."""
        assert self.is_fitted, "Model must be fitted on TRAIN before calling predict_proba."
        X = df[self.feature_cols].values
        X_scaled = self.scaler.transform(X)
        probs = self.model.predict_proba(X_scaled)[:, 1]
        return np.clip(probs, 0.0, 1.0)

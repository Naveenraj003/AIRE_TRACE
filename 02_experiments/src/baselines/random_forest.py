"""
AIRE-Trace Tabular Random Forest Baseline (S1)
Random Forest Classifier over Category A baseline features.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any
from sklearn.ensemble import RandomForestClassifier

class RandomForestBaseline:
    def __init__(
        self,
        model_id: str = "S1",
        feature_cols: List[str] = None,
        n_estimators: int = 100,
        max_depth: int = 6,
        random_state: int = 42
    ):
        self.model_id = model_id
        self.feature_cols = feature_cols
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.model = RandomForestClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            min_samples_split=5,
            random_state=self.random_state,
            n_jobs=-1
        )
        self.is_fitted = False

    def fit(self, df_train: pd.DataFrame, y_train: np.ndarray, sample_weight: np.ndarray = None):
        """Fits Random Forest model on TRAIN data only."""
        if self.feature_cols is None:
            self.feature_cols = [c for c in df_train.columns if c.startswith("feat_")]

        X_train = df_train[self.feature_cols].values
        self.model.fit(X_train, y_train, sample_weight=sample_weight)
        self.is_fitted = True

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        """Returns predicted probability of eventual failure (class 1)."""
        assert self.is_fitted, "Model must be fitted on TRAIN before calling predict_proba."
        X = df[self.feature_cols].values
        probs = self.model.predict_proba(X)[:, 1]
        return np.clip(probs, 0.0, 1.0)

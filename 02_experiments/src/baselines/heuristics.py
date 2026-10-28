"""
AIRE-Trace Heuristic Baseline Monitors (H1, H2, H3, H4)
Training-free, deterministic rule-based monitoring scores computed from prefix features.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List

class HeuristicMonitor:
    def __init__(self, model_id: str, target_feature: str):
        self.model_id = model_id
        self.target_feature = target_feature
        self.is_fitted = True

    def fit(self, df_train: pd.DataFrame, y_train: np.ndarray):
        # Heuristics are training-free. No parameter fitting.
        pass

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        """Returns risk scores in range [0, 1]."""
        vals = df[self.target_feature].values.astype(float)
        # Min-max scale or sigmoid scale for probability-like output
        max_val = np.max(vals) if len(vals) > 0 and np.max(vals) > 0 else 1.0
        scores = vals / max_val
        return np.clip(scores, 0.0, 1.0)


class CombinedHeuristicMonitor:
    def __init__(self, model_id: str = "H4", features: List[str] = None):
        self.model_id = model_id
        self.features = features or ["feat_tool_error_count", "feat_retry_count", "feat_repeated_action_last2"]
        self.means = {}
        self.stds = {}
        self.is_fitted = False

    def fit(self, df_train: pd.DataFrame, y_train: np.ndarray = None):
        """Fit z-score normalization parameters on TRAIN only."""
        for f in self.features:
            vals = df_train[f].values.astype(float)
            self.means[f] = float(np.mean(vals))
            std = float(np.std(vals))
            self.stds[f] = std if std > 1e-6 else 1.0
        self.is_fitted = True

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        """Returns average normalized z-score mapped to [0, 1] via sigmoid."""
        z_scores = np.zeros(len(df))
        for f in self.features:
            vals = df[f].values.astype(float)
            m = self.means.get(f, 0.0)
            s = self.stds.get(f, 1.0)
            z_scores += (vals - m) / s

        z_avg = z_scores / len(self.features)
        # Sigmoid mapping: 1 / (1 + exp(-z_avg))
        probs = 1.0 / (1.0 + np.exp(-z_avg))
        return np.clip(probs, 0.0, 1.0)

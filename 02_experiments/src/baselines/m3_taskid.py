import numpy as np
import pandas as pd
from typing import List
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

class M3TaskidBaseline:
    def __init__(
        self,
        model_id: str = "M3",
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
        self.task_failure_rates = {}
        self.global_failure_rate = 0.0

    def _extract_features(self, df: pd.DataFrame, is_fit: bool) -> np.ndarray:
        if self.feature_cols is None:
            self.feature_cols = [c for c in df.columns if str(c).startswith("feat_")]
            
        X_num = df[self.feature_cols].values
        
        # Target encode task_id
        task_id_col = df['task_id'].values
        
        encoded_task = np.zeros(len(df))
        for i, tid in enumerate(task_id_col):
            # Apply learned failure rate; fallback to global failure rate if unseen
            encoded_task[i] = self.task_failure_rates.get(tid, self.global_failure_rate)
            
        X_task = encoded_task.reshape(-1, 1)
        
        X_combined = np.hstack([X_num, X_task])
        
        if is_fit:
            X_scaled = self.scaler.fit_transform(X_combined)
        else:
            X_scaled = self.scaler.transform(X_combined)
            
        return X_scaled

    def fit(self, df_train: pd.DataFrame, y_train: np.ndarray, sample_weight: np.ndarray = None):
        # Calculate task failure rates on TRAIN episodes
        ep_df = df_train[['episode_id', 'task_id', 'eventual_outcome']].drop_duplicates()
        
        self.global_failure_rate = ep_df['eventual_outcome'].mean()
        
        task_stats = ep_df.groupby('task_id')['eventual_outcome'].agg(['mean'])
        self.task_failure_rates = task_stats['mean'].to_dict()
        
        X = self._extract_features(df_train, is_fit=True)
        self.model.fit(X, y_train, sample_weight=sample_weight)
        self.is_fitted = True

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        assert self.is_fitted
        X = self._extract_features(df, is_fit=False)
        probs = self.model.predict_proba(X)[:, 1]
        return np.clip(probs, 0.0, 1.0)

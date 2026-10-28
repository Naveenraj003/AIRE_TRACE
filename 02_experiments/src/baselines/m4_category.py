import numpy as np
import pandas as pd
from typing import List
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from datasets import load_dataset

class M4CategoryBaseline:
    def __init__(
        self,
        model_id: str = "M4",
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
        
        self.cat_failure_rates = {}
        self.diff_failure_rates = {}
        self.global_failure_rate = 0.0
        
        # Load raw dataset to get category and difficulty mapping
        ds = load_dataset("Contextbench/Tracebench", split="full")
        self.meta_map = {row["traj_id"]: {"category": row["category"], "difficulty": row["difficulty"]} for row in ds}

    def _extract_features(self, df: pd.DataFrame, is_fit: bool) -> np.ndarray:
        if self.feature_cols is None:
            self.feature_cols = [c for c in df.columns if str(c).startswith("feat_")]
            
        X_num = df[self.feature_cols].values
        
        episodes = df['episode_id'].values
        
        cat_encoded = np.zeros(len(df))
        diff_encoded = np.zeros(len(df))
        
        for i, ep in enumerate(episodes):
            meta = self.meta_map.get(ep, {"category": "unknown", "difficulty": "unknown"})
            cat_encoded[i] = self.cat_failure_rates.get(meta["category"], self.global_failure_rate)
            diff_encoded[i] = self.diff_failure_rates.get(meta["difficulty"], self.global_failure_rate)
            
        X_cat = cat_encoded.reshape(-1, 1)
        X_diff = diff_encoded.reshape(-1, 1)
        
        X_combined = np.hstack([X_num, X_cat, X_diff])
        
        if is_fit:
            X_scaled = self.scaler.fit_transform(X_combined)
        else:
            X_scaled = self.scaler.transform(X_combined)
            
        return X_scaled

    def fit(self, df_train: pd.DataFrame, y_train: np.ndarray, sample_weight: np.ndarray = None):
        ep_df = df_train[['episode_id', 'eventual_outcome']].drop_duplicates().copy()
        
        ep_df['category'] = ep_df['episode_id'].apply(lambda ep: self.meta_map.get(ep, {}).get("category", "unknown"))
        ep_df['difficulty'] = ep_df['episode_id'].apply(lambda ep: self.meta_map.get(ep, {}).get("difficulty", "unknown"))
        
        self.global_failure_rate = ep_df['eventual_outcome'].mean()
        
        cat_stats = ep_df.groupby('category')['eventual_outcome'].mean()
        diff_stats = ep_df.groupby('difficulty')['eventual_outcome'].mean()
        
        self.cat_failure_rates = cat_stats.to_dict()
        self.diff_failure_rates = diff_stats.to_dict()
        
        X = self._extract_features(df_train, is_fit=True)
        self.model.fit(X, y_train, sample_weight=sample_weight)
        self.is_fitted = True

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        assert self.is_fitted
        X = self._extract_features(df, is_fit=False)
        probs = self.model.predict_proba(X)[:, 1]
        return np.clip(probs, 0.0, 1.0)

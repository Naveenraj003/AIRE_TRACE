import numpy as np
import pandas as pd
from typing import List
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

class M2SemanticBaseline:
    def __init__(
        self,
        model_id: str = "M2",
        feature_cols: List[str] = None,
        C: float = 1.0,
        random_state: int = 42
    ):
        self.model_id = model_id
        self.feature_cols = feature_cols
        self.C = C
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.vectorizer = TfidfVectorizer(max_features=50, stop_words="english")
        self.model = LogisticRegression(
            C=self.C,
            solver="lbfgs",
            max_iter=1000,
            random_state=self.random_state
        )
        self.is_fitted = False
        self.instructions_df = pd.read_parquet("results/research_extension/episode_task_instructions.parquet")

    def _extract_features(self, df: pd.DataFrame, is_fit: bool) -> np.ndarray:
        if self.feature_cols is None:
            self.feature_cols = [c for c in df.columns if str(c).startswith("feat_")]
            
        X_num = df[self.feature_cols].values
        
        merged = df.merge(self.instructions_df, on="episode_id", how="left")
        text_data = merged["task_instruction"].fillna("").astype(str).tolist()
        
        if is_fit:
            X_num_scaled = self.scaler.fit_transform(X_num)
            X_text = self.vectorizer.fit_transform(text_data).toarray()
        else:
            X_num_scaled = self.scaler.transform(X_num)
            X_text = self.vectorizer.transform(text_data).toarray()
            
        return np.hstack([X_num_scaled, X_text])

    def fit(self, df_train: pd.DataFrame, y_train: np.ndarray, sample_weight: np.ndarray = None):
        X = self._extract_features(df_train, is_fit=True)
        self.model.fit(X, y_train, sample_weight=sample_weight)
        self.is_fitted = True

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        assert self.is_fitted
        X = self._extract_features(df, is_fit=False)
        probs = self.model.predict_proba(X)[:, 1]
        return np.clip(probs, 0.0, 1.0)
        
    def extract_raw_features_for_duplicate_check(self, df: pd.DataFrame) -> np.ndarray:
        assert self.is_fitted
        return self._extract_features(df, is_fit=False)

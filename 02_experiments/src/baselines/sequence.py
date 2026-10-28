"""
AIRE-Trace Sequence Baseline Model (S2)
Implements a PyTorch GRU sequence model over normalized prefix features.
Preserves duck-typed baseline interface (fit, predict_proba) expected by MasterEvaluator.
"""

import os
from typing import List, Optional
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler


class _GRUNet(nn.Module):
    """Internal PyTorch GRU neural network for temporal prefix modeling."""

    def __init__(self, input_dim: int, hidden_dim: int = 64, num_layers: int = 1):
        super().__init__()
        self.gru = nn.GRU(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True
        )
        self.fc = nn.Linear(hidden_dim, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.
        Args:
            x: Input tensor of shape [batch_size, seq_len, input_dim]
        Returns:
            Logits tensor of shape [batch_size, seq_len]
        """
        out, _ = self.gru(x)
        logits = self.fc(out).squeeze(-1)
        return logits


class SequenceBaseline:
    """
    SequenceBaseline (S2) baseline monitor.
    Uses a GRU to process variable-length temporal prefix sequences for failure risk prediction.
    """

    def __init__(
        self,
        feature_cols: Optional[List[str]] = None,
        model_id: str = "S2",
        hidden_dim: int = 64,
        num_layers: int = 1,
        lr: float = 1e-3,
        epochs: int = 10,
        batch_size: int = 128,
        device: str = "cpu",
        random_seed: int = 42
    ):
        self.model_id = model_id
        self.feature_cols = feature_cols
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.lr = lr
        self.epochs = epochs
        self.batch_size = batch_size
        self.device = device
        self.random_seed = random_seed
        self.rng = np.random.RandomState(self.random_seed)
        self.scaler = StandardScaler()
        self.model: Optional[_GRUNet] = None
        self.is_fitted = False

    def fit(self, df_train: pd.DataFrame, y_train: np.ndarray) -> None:
        """
        Fits StandardScaler and Sequence (GRU) model on TRAIN data only.
        Computes episode-balanced sample weights (w_i = 1 / T_i) internally per Rule 11.
        """
        if self.feature_cols is None:
            self.feature_cols = [c for c in df_train.columns if c.startswith("feat_")]

        X_train = df_train[self.feature_cols].values
        X_train_scaled = self.scaler.fit_transform(X_train)

        df_work = df_train[["episode_id", "prefix_len"]].copy()
        df_work["_orig_idx"] = np.arange(len(df_train))
        df_work["_y"] = y_train

        grouped = df_work.groupby("episode_id", sort=False)
        episodes_x = []
        episodes_y = []
        episodes_w = []

        for ep_id, group in grouped:
            sorted_group = group.sort_values("prefix_len")
            indices = sorted_group["_orig_idx"].values
            t_len = len(indices)
            ep_x = X_train_scaled[indices]
            ep_y = sorted_group["_y"].values.astype(np.float32)
            # Rule 11: episode-balanced weight = 1 / T_i
            ep_w = np.full(t_len, 1.0 / max(t_len, 1), dtype=np.float32)

            episodes_x.append(ep_x)
            episodes_y.append(ep_y)
            episodes_w.append(ep_w)

        num_episodes = len(episodes_x)
        num_features = len(self.feature_cols)

        torch.manual_seed(self.random_seed)
        self.model = _GRUNet(
            input_dim=num_features,
            hidden_dim=self.hidden_dim,
            num_layers=self.num_layers
        ).to(self.device)

        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        criterion = nn.BCEWithLogitsLoss(reduction="none")

        self.model.train()
        for epoch in range(self.epochs):
            perm = self.rng.permutation(num_episodes)
            for i in range(0, num_episodes, self.batch_size):
                batch_indices = perm[i : i + self.batch_size]
                b_size = len(batch_indices)

                b_max_len = max(len(episodes_x[idx]) for idx in batch_indices)

                X_batch = np.zeros((b_size, b_max_len, num_features), dtype=np.float32)
                y_batch = np.zeros((b_size, b_max_len), dtype=np.float32)
                w_batch = np.zeros((b_size, b_max_len), dtype=np.float32)
                mask_batch = np.zeros((b_size, b_max_len), dtype=np.float32)

                for b_idx, ep_idx in enumerate(batch_indices):
                    ep_x = episodes_x[ep_idx]
                    ep_y = episodes_y[ep_idx]
                    ep_w = episodes_w[ep_idx]
                    seq_l = len(ep_x)

                    X_batch[b_idx, :seq_l, :] = ep_x
                    y_batch[b_idx, :seq_l] = ep_y
                    w_batch[b_idx, :seq_l] = ep_w
                    mask_batch[b_idx, :seq_l] = 1.0

                t_X = torch.tensor(X_batch, dtype=torch.float32, device=self.device)
                t_y = torch.tensor(y_batch, dtype=torch.float32, device=self.device)
                t_w = torch.tensor(w_batch, dtype=torch.float32, device=self.device)
                t_mask = torch.tensor(mask_batch, dtype=torch.float32, device=self.device)

                optimizer.zero_grad()
                logits = self.model(t_X)
                loss_raw = criterion(logits, t_y)

                weighted_loss = loss_raw * t_mask * t_w
                denom = (t_mask * t_w).sum()
                if denom > 0:
                    loss = weighted_loss.sum() / denom
                else:
                    loss = weighted_loss.sum()

                loss.backward()
                optimizer.step()

        self.is_fitted = True

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        """
        Returns failure probabilities for each row in input DataFrame.
        Guarantees that returned array is parallel to input df.index order.
        """
        assert self.is_fitted, "Model must be fitted on TRAIN before calling predict_proba."
        assert self.model is not None, "Model instance is uninitialized."

        if self.feature_cols is None:
            self.feature_cols = [c for c in df.columns if c.startswith("feat_")]

        X_input = df[self.feature_cols].values
        X_scaled = self.scaler.transform(X_input)

        df_work = df[["episode_id", "prefix_len"]].copy()
        df_work["_orig_idx"] = np.arange(len(df))

        grouped = df_work.groupby("episode_id", sort=False)

        out_probs = np.zeros(len(df), dtype=np.float64)

        self.model.eval()
        with torch.no_grad():
            for ep_id, group in grouped:
                sorted_group = group.sort_values("prefix_len")
                orig_indices = sorted_group["_orig_idx"].values
                t_len = len(orig_indices)

                ep_x = X_scaled[orig_indices]
                X_tensor = torch.tensor(ep_x, dtype=torch.float32, device=self.device).unsqueeze(0)

                logits = self.model(X_tensor)
                probs = torch.sigmoid(logits).squeeze(0).cpu().numpy()

                if t_len == 1:
                    probs = np.array([probs.item()])

                out_probs[orig_indices] = probs

        return np.clip(out_probs, 0.0, 1.0)

    def save(self, filepath: str) -> None:
        """Serializes complete model state to disk via torch.save."""
        assert self.is_fitted, "Cannot save an unfitted model."
        assert self.model is not None, "Model is uninitialized."

        payload = {
            "model_id": self.model_id,
            "state_dict": self.model.state_dict(),
            "hyperparams": {
                "hidden_dim": self.hidden_dim,
                "num_layers": self.num_layers,
                "lr": self.lr,
                "epochs": self.epochs,
                "batch_size": self.batch_size,
                "device": self.device
            },
            "feature_cols": self.feature_cols,
            "scaler": self.scaler,
            "is_fitted": self.is_fitted
        }
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        torch.save(payload, filepath)

    def load(self, filepath: str) -> None:
        """Loads model state from disk via torch.load."""
        payload = torch.load(filepath, map_location=self.device, weights_only=False)
        self.model_id = payload["model_id"]
        hyperparams = payload["hyperparams"]
        self.hidden_dim = hyperparams["hidden_dim"]
        self.num_layers = hyperparams["num_layers"]
        self.lr = hyperparams["lr"]
        self.epochs = hyperparams["epochs"]
        self.batch_size = hyperparams["batch_size"]
        self.feature_cols = payload["feature_cols"]
        self.scaler = payload["scaler"]
        self.is_fitted = payload["is_fitted"]

        num_features = len(self.feature_cols)
        self.model = _GRUNet(
            input_dim=num_features,
            hidden_dim=self.hidden_dim,
            num_layers=self.num_layers
        ).to(self.device)
        self.model.load_state_dict(payload["state_dict"])

# Gate 4.0.3: Blocking Interface Reconciliation

**Date:** 2026-08-04  
**Status:** BLOCKING ISSUES RESOLVED  
**Purpose:** Reconcile the four blocking integration flaws identified in `reports/gate4_design_freeze_final.md` to ensure protocol compliance prior to implementation.

---

## 1. MasterEvaluator ↔ SequenceBaseline interface
**(sample_weight compatibility and Protocol Rule 11)**

- **Root Cause:** `MasterEvaluator` invokes `model.fit(df_train, y_train)` directly and does not compute or pass a `sample_weight` argument. The previous V2 design erroneously expected `sample_weight` in the signature.
- **Frozen Interface Contract:** `def fit(self, df_train: pd.DataFrame, y_train: np.ndarray) -> None:`
- **Required Invariant:** `SequenceBaseline` MUST compute the episode-balanced sample weights ($w_i = 1 / \min(T_i, 30)$) internally during `fit()` using the `df_train` `episode_id` and `prefix_len` columns, prior to computing the PyTorch loss.
- **Required Assertions:** `assert "sample_weight" not in inspect.signature(self.fit).parameters` to guarantee signature matching. Assert weight tensors exactly balance variable-length episodes.
- **Verification Procedure:** Unit test verifying that an episode of length 5 and an episode of length 30 exert identical total gradient magnitude across the epoch.

## 2. BaselineRegistry integration
**(registration, constructor, hyperparameter propagation)**

- **Root Cause:** `BaselineRegistry.get_baseline_models(feature_cols=...)` instantiates all models uniformly without custom kwargs or positional `model_id`s.
- **Frozen Interface Contract:** `def __init__(self, feature_cols: List[str], model_id: str = "S2", **kwargs):`
- **Required Invariant:** The constructor MUST encapsulate all PyTorch architectural hyperparameter defaults (e.g., `hidden_dim=64`, `num_layers=1`, `lr=1e-3`, `epochs=10`, `batch_size=128`, `device="cpu"`). Calling the constructor with only `feature_cols` must successfully configure the complete network.
- **Required Assertions:** `assert hasattr(self, 'hidden_dim')` and `assert self.model_id == "S2"` when invoked cleanly.
- **Verification Procedure:** Call `SequenceBaseline(feature_cols=['feat_1'])` and verify successful instantiation of the PyTorch `nn.Module` with default architecture.

## 3. Serialization contract
**(state_dict, scaler, feature metadata, architecture, fitted state)**

- **Root Cause:** A naive `torch.save(model.state_dict())` discards the data scaler, feature column names, fitted boolean flags, and architectural dimensions needed to reconstruct the network before loading weights.
- **Frozen Interface Contract:** `def save(self, filepath: str) -> None:` and `def load(self, filepath: str) -> None:`
- **Required Invariant:** `save()` MUST serialize a single comprehensive dictionary dictionary containing `{'state_dict': ..., 'hyperparams': ..., 'feature_cols': ..., 'scaler': ..., 'is_fitted': ...}`. `load()` MUST instantiate the PyTorch architecture from `hyperparams` before applying `state_dict`.
- **Required Assertions:** `assert self.is_fitted is True` and `assert self.scaler is not None` upon successful `load()`.
- **Verification Procedure:** Assert `np.allclose(pred_before_save, pred_after_load)` evaluating against a static validation dataframe.

## 4. Prediction ordering
**(exact mapping between temporal tensors and flat dataframe rows)**

- **Root Cause:** Extracting tensors via `groupby` or unique sets destroys the strict row iteration order $r \in [0, N-1]$ of the input DataFrame slice, creating a fatal misalignment when the flat `N` array is returned.
- **Frozen Interface Contract:** `def predict_proba(self, df: pd.DataFrame) -> np.ndarray:` returns a flat array perfectly parallel to `df`.
- **Required Invariant:** Sequence extraction MUST create an auxiliary 2D integer mapping array of shape `[B, K]` storing the positional row indices $r$. Output extraction MUST strictly scatter the logits via `out_flat[index_map[b, k]] = pred_tensor[b, k, 0]` for all valid attention mask entries.
- **Required Assertions:** `assert len(out_flat) == len(df)` and `assert np.isnan(out_flat).sum() == 0`.
- **Verification Procedure:** Integration test running sequential sequences through `predict_proba()` and verifying that the extracted output perfectly correlates with dummy input row indices.

---

## 5. Classification of Remaining Findings from gate4_design_freeze_final.md

No new issues introduced. All remaining items from the final review represent PyTorch coding mechanics and are classified as **Implementation Details (handled during Gate 4.1)**:

- **BCEWithLogitsLoss vs BCELoss (Numerical Instability):** Implementation detail. (Compute loss on logits, apply sigmoid only for output).
- **Target Label Data Type Mismatch (.float() casting):** Implementation detail.
- **Padded Weight Tensor Definition (Zero padding):** Implementation detail.
- **Missing Training Horizon & Optimization Parameters:** Implementation detail.
- **Device Placement Ambiguity (.to(device)):** Implementation detail.
- **Validation & Protocol Guard Restrictions (No early stopping via test/calib):** Implementation detail.
- **Exception Class Ambiguities (AssertionError usage):** Implementation detail.

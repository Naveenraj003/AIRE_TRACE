# Gate 4: SequenceBaseline Implementation Contract

**Date:** 2026-08-04  
**Status:** DEFINITIVE INTERFACE SPECIFICATION

This document represents the definitive implementation contract for the `SequenceBaseline` class (the AIRE-Trace Sequence model). It eliminates all design ambiguity and specifies the exact invariants required to interoperate with the frozen Gate 3 `MasterEvaluator`.

---

## 1. Public Class Interface & Registry Integration

**Class Name:** `SequenceBaseline`  
**Location:** `src/baselines/sequence.py`

### Registry Interface
The class must be instantiated identically to `LogisticBaseline` and `RandomForestBaseline` by `BaselineRegistry.get_baseline_models()`.

**Signature:**
```python
def __init__(self, model_id: str, feature_cols: List[str], **kwargs):
    """
    Args:
        model_id: Identifier for the model (e.g., "S2")
        feature_cols: List of column names used as input features
        **kwargs: Optional hyperparameters (hidden_dim, num_layers, lr, batch_size, max_seq_len=30, etc.)
    """
```

---

## 2. Method Signatures

### A. Training Method (`fit`)
**Signature:**
```python
def fit(self, df_train: pd.DataFrame, y_train: np.ndarray, sample_weight: np.ndarray = None) -> None:
```
- **Required Inputs:**
  - `df_train`: Flat DataFrame containing `N` rows (prefixes). Must include `episode_id` and `prefix_len`.
  - `y_train`: Flat 1D numpy array of length `N` containing binary labels `{0, 1}`.
  - `sample_weight`: Flat 1D numpy array of length `N` containing float weights (e.g., $1/\min(T_i, 30)$).
- **Required Outputs:** `None`. Sets `self.is_fitted = True`.

### B. Inference Method (`predict_proba`)
**Signature:**
```python
def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
```
- **Required Inputs:**
  - `df`: Flat DataFrame containing `N` rows. Must include `episode_id` and `prefix_len`.
- **Required Outputs:**
  - Flat 1D numpy array of length `N` containing float probabilities $[0.0, 1.0]$.

### C. Serialization Methods (`save` & `load`)
**Signature:**
```python
def save(self, filepath: str) -> None:
def load(self, filepath: str) -> None:
```
- **Required Inputs:** String file path.
- **Required Outputs:** `None`.
- **Serialization Format:** Must use `torch.save(self.model.state_dict(), filepath)` and `self.model.load_state_dict(torch.load(filepath))`. **Cannot** use `joblib.dump` for the PyTorch module.

---

## 3. Data Schema & Tensor Dimensions

### DataFrame Schema Constraints
The input `df` is guaranteed to contain:
- `episode_id` (str or int): Unique identifier for the agent trajectory.
- `prefix_len` (int): 1-indexed step count $t$. Guaranteed to be contiguous $1 \dots k_i$ up to $\min(T_i, K)$.
- Features specified in `self.feature_cols`.

### Tensor Dimensions
Let:
- $N$ = total number of flat rows in `df`.
- $B$ = number of unique `episode_id`s.
- $K$ = `max(prefix_len)` (typically 30).
- $F$ = `len(self.feature_cols)`.

Internal conversions **MUST** yield the following PyTorch tensor shapes:
1. **Features:** `[B, K, F]` (Padded with `0.0` at steps $> k_i$).
2. **Labels:** `[B, K, 1]` (Values broadcasted from flat `y_train`).
3. **Weights:** `[B, K, 1]` (Values broadcasted from flat `sample_weight`).
4. **Attention Mask:** `[B, K, 1]` (Boolean or float: `1.0` if step $\le k_i$, else `0.0`).
5. **Model Forward Output:** `[B, K, 1]` (A probability for *every* timestep).

---

## 4. Ordering & Alignment Guarantees

### A. Episode and Prefix Ordering
Inside `predict_proba()`, when collapsing the `[B, K, 1]` prediction tensor back to a flat `[N]` array:
- **The output array MUST mirror the exact row order of the input `df`.**
- Since `groupby` operations alter the iteration order, `SequenceBaseline` MUST track the original row index (e.g., via `np.arange(N)`) during sequence construction.
- The `[B, K]` output predictions must be scattered back into an `[N]` array using the tracked indices.

### B. Batch Ordering
- During `predict_proba()`, PyTorch `DataLoader` **MUST** be instantiated with `shuffle=False` to preserve batch predictability.

---

## 5. Loss Calculation Semantics

The model optimizes binary cross-entropy (BCE). 
- **Attention Masking:** The loss function must explicitly multiply by the attention mask to ignore padded timesteps.
- **Sample Weighting:** The loss function must multiply by `sample_weight` to enforce Protocol Rule 11 (episode balancing).
- **Calculation:** `loss = (F.binary_cross_entropy(pred, y, reduction='none') * mask * weight).sum() / mask.sum()`

---

## 6. Failure Conditions & Exceptions

The implementation MUST raise exceptions under the following conditions:
1. `AssertionError`: If `predict_proba()` attempts to return an array where `len(output) != len(df)`.
2. `ValueError`: If `fit()` or `predict_proba()` receives a `df` missing `episode_id` or `prefix_len`.
3. `RuntimeError`: If `load()` is called on a file that does not contain a valid PyTorch state dict.
4. `NotFittedError`: If `predict_proba()` is called before `fit()` or `load()`.

---

## 7. Implementation Invariants (Summary)

To perfectly mimic tabular baselines (M1/S1) while running temporal reasoning internally:
1. **No External Evaluation Changes:** `MasterEvaluator` must not know it is calling a sequence model. It passes a flat `df` and receives a flat `[N]` array.
2. **No Flattened Outputs:** `model.forward()` cannot return `[B, 1]`. It must return predictions for the entire sequence history `[B, K, 1]` to score every prefix row.
3. **Zero-Leakage Padding:** Right-padding only. Future timesteps cannot influence past timesteps (e.g., no bidirectional RNNs).
4. **Deterministic Inference:** All `predict_proba()` calls on identical DataFrames must yield bit-for-bit identical probability arrays.

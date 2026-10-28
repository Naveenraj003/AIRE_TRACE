# Independent Technical Review & Final Verdict: Gate 4 Sequence Interface Specification

**Target Document:** `reports/gate4_sequence_interface_spec.md`  
**Review Date:** 2026-08-04  
**Status:** REJECTED — UNRESOLVED AMBIGUITIES & INCOMPATIBILITIES DETECTED  

---

## Executive Summary

An independent, zero-assumption review of [`reports/gate4_sequence_interface_spec.md`](file:///p:/AIRE-TRACE/reports/gate4_sequence_interface_spec.md) was conducted against the AIRE-Trace codebase ([`src/evaluation/evaluator.py`](file:///p:/AIRE-TRACE/src/evaluation/evaluator.py), [`src/baselines/registry.py`](file:///p:/AIRE-TRACE/src/baselines/registry.py), [`src/baselines/logistic.py`](file:///p:/AIRE-TRACE/src/baselines/logistic.py)), the frozen protocol (`AIRE-Trace_Frozen_Protocol_and_Plan.md`), and standard PyTorch execution dynamics.

The certification **"Gate 4 Design is Frozen and implementation-ready" CANNOT BE ISSUED at this time.**

Significant ambiguities, tensor inconsistencies, serialization defects, and runtime incompatibilities with `MasterEvaluator` were identified. Below is the precise itemization of all detected issues that must be addressed prior to code implementation.

---

## 1. Precise Itemization of Identified Defects & Ambiguities

### A. MasterEvaluator Incompatibilities (Critical)
1. **Missing `sample_weight` in `fit()` Call Site:**
   - **Issue:** Section 2.A and Section 5 of the spec require `fit()` to compute weighted binary cross-entropy using `sample_weight`: `loss = (F.binary_cross_entropy(pred, y, reduction='none') * mask * weight).sum() / mask.sum()`.
   - **Conflict:** In [`src/evaluation/evaluator.py`](file:///p:/AIRE-TRACE/src/evaluation/evaluator.py#L76), `MasterEvaluator` invokes `model.fit(df_train, y_train)` with only two arguments. `sample_weight` is NOT computed or passed by `MasterEvaluator`.
   - **Consequence:** Calling `fit()` under `MasterEvaluator` will result in `sample_weight=None`. If the loss function directly multiplies by `weight` without internal auto-computation or `None`-checking, PyTorch will throw `TypeError: unsupported operand type(s) for *: 'Tensor' and 'NoneType'`. Furthermore, if `sample_weight` is completely omitted, Protocol Rule 11 (episode balancing) is violated.

### B. Registry Incompatibilities
1. **Instantiation Signature Mismatch:**
   - **Issue:** Section 1 specifies `def __init__(self, model_id: str, feature_cols: List[str], **kwargs):` without default parameter values for `model_id`.
   - **Conflict:** In [`src/baselines/registry.py`](file:///p:/AIRE-TRACE/src/baselines/registry.py#L13-L24), `BaselineRegistry.get_baseline_models(feature_cols=feature_cols)` instantiates models via keyword argument `feature_cols`. Standard baselines (e.g. `LogisticBaseline`) provide default values for `model_id` (e.g., `model_id="M1"`).
   - **Consequence:** Instantiating `SequenceBaseline` without a default `model_id="S2"` will cause `TypeError: __init__() missing 1 required positional argument: 'model_id'`.
2. **Hyperparameter Propagation Defect:**
   - **Issue:** `SequenceBaseline` requires sequence-specific hyperparameters (`hidden_dim`, `num_layers`, `lr`, `batch_size`, `epochs`, `device`).
   - **Conflict:** `MasterEvaluator` and `BaselineRegistry` currently provide no mechanism to pass custom `**kwargs` to baseline constructors during `get_baseline_models()`.
   - **Consequence:** `SequenceBaseline` MUST define complete, sensible default values for all architectural and training hyperparameters inside `__init__`.

### C. Serialization Ambiguities & Data Loss Defect
1. **Incomplete Persisted State:**
   - **Issue:** Section 2.C mandates using `torch.save(self.model.state_dict(), filepath)` and `self.model.load_state_dict(torch.load(filepath))`.
   - **Defect:** `state_dict()` ONLY saves PyTorch network weights. It DOES NOT save:
     - `self.feature_cols` (list of feature column names)
     - `self.scaler` (fitted `StandardScaler` parameters for input feature normalization)
     - `self.is_fitted` (fitted status boolean flag)
     - Network architectural dimensions (`input_dim`, `hidden_dim`, `num_layers`) required to instantiate `self.model` prior to calling `load_state_dict`.
   - **Consequence:** Invoking `load()` on an uninitialized or freshly instantiated `SequenceBaseline` will fail because `self.model` will either not exist or have mismatched layer dimensions, and `self.scaler` will remain un-fitted, causing invalid inference or `NotFittedError`.

### D. Tensor Inconsistencies & Loss Function Deficiencies
1. **Numerical Instability in Loss Function:**
   - **Issue:** Section 5 specifies `F.binary_cross_entropy(pred, y, reduction='none')` where `pred` is a probability in $[0.0, 1.0]$.
   - **Defect:** In PyTorch, calling `binary_cross_entropy` directly on probabilities near $0.0$ or $1.0$ (without logit-space computation or epsilon clamping e.g., `1e-7`) produces `NaN` or `-inf` gradients during backpropagation.
   - **Required Fix:** Model `forward()` should output un-sigmoided logits for loss calculation using `F.binary_cross_entropy_with_logits`, and apply `torch.sigmoid` during `predict_proba()`.
2. **Target Label Data Type Mismatch:**
   - **Issue:** `MasterEvaluator` creates `y_train` via `df_train["eventual_outcome"].values.astype(int)` (64-bit integer array).
   - **Defect:** PyTorch `binary_cross_entropy` requires target tensors to be `torch.float32`.
   - **Consequence:** Passing `y_train` directly as a PyTorch `LongTensor` without explicit `.float()` conversion causes `RuntimeError: Expected object of scalar type Float but got scalar type Long for argument #2 'target'`.
3. **Padded Weight Tensor Definition:**
   - **Issue:** Section 3 specifies `sample_weight` as shape `[B, K, 1]`.
   - **Defect:** The spec does not define the padding value for `sample_weight` at timesteps $k > k_i$. While multiplying by `mask` zeros out padded loss terms, uninitialized or `NaN` values in padded weights can cause gradient corruption or scalar sum errors.

### E. Ordering & Indexing Ambiguities
1. **Loose Row Index Scattering Specification:**
   - **Issue:** Section 4.A states that outputs must be scattered back to flat `[N]` using tracked indices "(e.g., via `np.arange(N)`)".
   - **Defect:** DataFrames passed to `predict_proba()` (such as `df_calib` or `df_test` sliced from a larger DataFrame) may have non-contiguous, non-zero-indexed `df.index` labels (e.g. `[2, 5, 11, ...]`).
   - **Required Specification:** The spec must explicitly mandate a 2D integer mapping array of shape `[B, K]` storing positional row indices $r \in [0, N-1]$, ensuring that `pred_tensor[b, k, 0]` maps strictly to `out_flat[index_map[b, k]]` for all valid mask entries `mask[b, k] == 1`.

### F. Hidden Assumptions in Training Execution
1. **Missing Training Horizon & Optimization Parameters:**
   - **Issue:** The spec omits `epochs` (or `n_epochs`), optimizer class (`Adam`/`AdamW`), learning rate scheduler, and gradient clipping threshold.
2. **Device Placement Ambiguity:**
   - **Issue:** The spec makes no mention of `self.device` (`cpu`, `cuda`, `mps`). Creating PyTorch tensors from pandas DataFrames on CPU while `self.model` resides on GPU will cause `RuntimeError: Expected all tensors to be on the same device`.
3. **Validation & Protocol Guard Restrictions:**
   - **Issue:** The spec does not specify if internal validation / early stopping is permitted. Per Protocol Rule 8, under no circumstance may CALIBRATION or TEST splits be touched during `fit()`. Any early stopping must use an internal train-val split of `df_train`.

### G. Exception Class Ambiguities
1. **Unspecified Exception Module:**
   - **Issue:** Section 6 mandates raising `NotFittedError` if `predict_proba()` is called before `fit()`.
   - **Defect:** It does not specify whether `NotFittedError` must be imported from `sklearn.exceptions` or defined as a custom class. Standard tabular baselines in the repository currently use `AssertionError`.

---

## 2. Summary Verdict

The `SequenceBaseline` contract in `reports/gate4_sequence_interface_spec.md` provides a solid high-level blueprint for shape reconciliation, but contains critical implementation gaps that will cause runtime crashes or protocol non-compliance.

**Certification Status:** REJECTED  
**Required Action:** Amend `reports/gate4_sequence_interface_spec.md` to resolve all 7 defect areas detailed above before initiating Gate 4 implementation.

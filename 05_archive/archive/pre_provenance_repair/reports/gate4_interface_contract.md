# Gate 4 Interface Contract & Verification

**Date:** 2026-08-04  
**Target:** `gate4_architecture_v2.md`  
**Status:** **INTERFACE MISMATCHES DETECTED**

This report verifies every interface and interaction point between the proposed `SequenceBaseline` (S2) and the existing `MasterEvaluator` / `BaselineRegistry`.

---

## 1. Interface Verification Summary

Can AIRE-Trace (the Sequence model) replace any baseline inside the registry without changing evaluation code?
**NO. There are critical interface mismatches that will cause silent failures, tensor shape errors, or index misalignment during evaluation.**

### Verified as CORRECT:
- **Registry Integration:** Adding `S2: SequenceBaseline` to the dictionary is correct.
- **MasterEvaluator Integration:** Exposing `fit` and `predict_proba` aligns with the evaluator's expected orchestration.
- **Threshold Interface:** Returning a flat 1D `np.ndarray` of probabilities allows `select_calibration_threshold()` to work without modification.
- **Probability Output:** Values bounded to $[0,1]$ via Sigmoid match expectations.
- **Feature Ordering:** Grouping by `episode_id` and ordering by `prefix_len` correctly reconstructs the temporal sequence for the GRU/1D-CNN.
- **Manifest Loading:** The model properly accepts `df` dataframes and delegates manifest loading to the runner.

### Detected MISMATCHES:
- **`predict_proba()` row ordering (BLOCKING)**
- **Expected tensor shapes in `forward()` (BLOCKING)**
- **Loss computation tensor shapes (HIGH)**
- **Missing `save()` and `load()` interfaces (MEDIUM)**

---

## 2. Detailed Mismatch Identification

### Mismatch 1: Forward Tensor Shape [BLOCKING]
**Issue:** Section 6 specifies `model.forward(padded_sequences) → torch.Tensor [B, 1]`.
**Why it fails:** The input DataFrame contains $N$ rows, representing multiple prefixes per episode (e.g., $t=1, t=2, \dots, t=\min(T_i, 30)$). `MasterEvaluator` evaluates the risk at *every* prefix row. If the model only outputs `[B, 1]`, it is only predicting the final timestep of each episode.
**Resolution:** `model.forward()` MUST return `[B, K, 1]` (or `[B, K]`). The sequence model must generate a prediction at every timestep $t \le K$ so that these predictions can be mapped back to the multiple prefix rows for that episode.

### Mismatch 2: Row Index Preservation in `predict_proba()` [BLOCKING]
**Issue:** `predict_proba(df)` must return an `np.ndarray [N]` that aligns **exactly** with the row order of the input `df`.
**Why it fails:** Section 6 states: `2. _group_by_episode(features, df) -> episode sequences`, then pads, predicts, and expands. Grouping by `episode_id` using hash maps or `groupby` typically destroys the original row order of the DataFrame. If the predictions are flattened back into an `[N]` array without explicitly tracking and restoring the original row indices, `MasterEvaluator` will assign the wrong probabilities to the wrong prefixes/episodes, completely invalidating the metrics.
**Resolution:** `_extract_feature_matrix` and `_group_by_episode` MUST track the original `df.index` or integer row positions, and `predict_proba` MUST scatter the `[B, K]` predictions back into an `[N]` array using those tracked indices to guarantee perfect alignment with `df`.

### Mismatch 3: Loss Computation Tensor Shapes [HIGH]
**Issue:** `fit(df_train, y_train, sample_weight)` receives `y_train` and `sample_weight` as flat `[N]` arrays.
**Why it fails:** Section 6 specifies: "forward pass → BCE loss (weighted by sample_weight)". The forward pass (once fixed) will output `[B, K, 1]`. You cannot compute BCE loss against a flat `[N]` array. 
**Resolution:** `_group_by_episode` and `_pad_sequences` must also be applied to `y_train` and `sample_weight`, transforming them into `[B, K]` tensors with appropriate padding masks so the BCE loss is calculated correctly per-timestep.

### Mismatch 4: Missing `save()` and `load()` Interfaces [MEDIUM]
**Issue:** The class diagram and method table omit `save()` and `load()`.
**Why it fails:** If `MasterEvaluator` or `run_experiments.py` orchestrates saving models to disk (as is standard for reproducibility), PyTorch models (`S2`) require `torch.save(model.state_dict())`, which is entirely different from `joblib.dump` used by `M1` and `S1`. 
**Resolution:** `SequenceBaseline` must explicitly expose `save(filepath)` and `load(filepath)` to encapsulate PyTorch-specific serialization, ensuring the runner does not need to know it is handling a neural network.

---

## 3. Conclusion

The V2 architecture correctly abandons the duplicate evaluation pipeline, but the internal tensor mechanics of the `SequenceBaseline` are incompatible with the flat `DataFrame` contract expected by `MasterEvaluator`. 

To safely replace any baseline inside the registry without changing the evaluation code, the `SequenceBaseline` must act as a perfect bridge: it must disassemble the flat `[N]` inputs into `[B, K]` sequences for PyTorch, and precisely reassemble the `[B, K]` outputs back into the exact `[N]` flat ordering expected by the evaluator.

# Gate 4.0.2: SequenceBaseline Interface Reconciliation

**Date:** 2026-08-04  
**Status:** DESIGN RECONCILIATION COMPLETE

This document resolves the interface mismatches identified in `reports/gate4_interface_contract.md`. It defines the exact invariants required for `SequenceBaseline` to seamlessly interoperate with `MasterEvaluator` while preserving the frozen scientific protocol.

---

## 1. DataFrame → Temporal Sequence Conversion
- **Root Cause:** Flat `[N, F]` DataFrame rows do not explicitly encode temporal adjacency; a PyTorch RNN/CNN requires `[B, K, F]`.
- **Scientific Impact:** Incorrect grouping merges prefixes from different episodes or scrambles their causal temporal order, destroying the ability to learn trajectories.
- **Interface Contract:** `_extract_sequences(df, y, sample_weight) -> Tensor, Tensor, Tensor, List[Index]`
- **Required Invariant:** Grouping must be strictly partitioned by `episode_id` and ordered ascending by `prefix_len` (equivalent to checkpoint $t$).
- **Verification Procedure:** Unit tests asserting `diff(prefix_len) > 0` for every constructed sequence before tensor conversion.

## 2. Temporal Tensor → Probability Vector Conversion
- **Root Cause:** A sequence model naturally predicts a probability for a sequence, but `MasterEvaluator` requires a probability for every prefix row independently.
- **Scientific Impact:** Returning only the final step's prediction (`[B, 1]`) fails to provide risk scores for earlier checkpoints, invalidating prefix-level scoring.
- **Interface Contract:** The PyTorch model `forward()` MUST return `[B, K, 1]` (predictions at every timestep).
- **Required Invariant:** Every valid non-padded timestep $1 \dots k_i$ in the tensor must produce a valid probability mapped to its corresponding DataFrame row.
- **Verification Procedure:** Assert `output.shape == (B, K, 1)` in PyTorch tests.

## 3. Episode Ordering Preservation
- **Root Cause:** Group-by operations (e.g., hash maps) alter the iteration order compared to the original DataFrame row order.
- **Scientific Impact:** Reassembling predictions without tracking original row indices assigns episode $A$'s predictions to episode $B$, causing catastrophic evaluation failure.
- **Interface Contract:** The sequence extraction must return an auxiliary array `original_indices` mapping tensor elements back to `df.index`.
- **Required Invariant:** `len(predictions) == len(df)` AND `np.all(predictions[original_indices] == reconstructed_flat_predictions)`.
- **Verification Procedure:** Integration test asserting `np.array_equal(reconstructed_indices, df.index)`.

## 4. Prefix Ordering Preservation
- **Root Cause:** A DataFrame might have missing checkpoints (though Gate 2 guarantees $1 \dots \min(T_i, 30)$ continuously).
- **Scientific Impact:** Missing steps misalign the GRU hidden state relative to actual agent time.
- **Interface Contract:** The tensor time dimension $k$ must strictly map to `prefix_len`.
- **Required Invariant:** `tensor[b, k]` corresponds exactly to the prefix where `prefix_len == k+1`.
- **Verification Procedure:** Assert `prefix_len.max() <= K`.

## 5. Batch Ordering
- **Root Cause:** PyTorch DataLoaders often shuffle batches during training.
- **Scientific Impact:** Shuffling is necessary for gradient stability but destroys the `df.index` mapping if used during `predict_proba`.
- **Interface Contract:** `DataLoader(shuffle=False)` MUST be strictly enforced inside `predict_proba()`.
- **Required Invariant:** Inference batches must be processed deterministically.
- **Verification Procedure:** Unit test verifying `DataLoader` configuration in inference mode.

## 6. Manifest Ordering
- **Root Cause:** `MasterEvaluator` assumes `predict_proba()` returns an array exactly parallel to the manifest rows.
- **Scientific Impact:** Violation causes metric calculations (e.g., AUROC, FAR) to correlate incorrect predictions with true labels.
- **Interface Contract:** Output of `predict_proba(df)` is `np.ndarray` of shape `[len(df)]`.
- **Required Invariant:** The output array must exactly mirror the sequential order of `df` rows, overriding any internal PyTorch batching/grouping order.
- **Verification Procedure:** Assert `len(predictions) == len(df)` and validate against a dummy dataset with known target values.

## 7. Tensor Dimensions
- **Root Cause:** BCE loss requires labels to match prediction dimensions.
- **Scientific Impact:** A flat `y_train` array `[N]` cannot be broadcast against a sequence output `[B, K, 1]`.
- **Interface Contract:** `y_train` and `sample_weight` must be grouped, padded, and shaped to `[B, K]` tensors identically to the features.
- **Required Invariant:** `y_tensor.shape == output.shape` and `weight_tensor.shape == output.shape`.
- **Verification Procedure:** Assert tensor dimension equivalence before loss calculation.

## 8. Padding Strategy
- **Root Cause:** Episodes have variable lengths $k_i \le K$.
- **Scientific Impact:** Computing gradients or predictions on padded (non-existent) timesteps corrupts both the learned weights and the evaluation output.
- **Interface Contract:** Zero-padding applied to right-side of sequences (post-$k_i$).
- **Required Invariant:** Padded features must equal `0.0`.
- **Verification Procedure:** Assert `tensor[b, k_i:] == 0.0`.

## 9. Attention Mask Semantics
- **Root Cause:** Loss calculation and prediction extraction must ignore padded timesteps.
- **Scientific Impact:** Including padding in the BCE loss artificially inflates confidence on zero-vectors.
- **Interface Contract:** `mask` tensor of shape `[B, K]` where `1` indicates valid data and `0` indicates padding.
- **Required Invariant:** `loss = (bce(pred, y) * mask * weight).sum() / mask.sum()`.
- **Verification Procedure:** Assert loss is strictly 0 for all indices where `mask == 0`.

## 10. Serialization Format
- **Root Cause:** `joblib.dump` (used for M1/S1) fails or is inefficient for PyTorch neural networks.
- **Scientific Impact:** Model state cannot be faithfully preserved across runs, breaking reproducibility.
- **Interface Contract:** `SequenceBaseline` implements `save(filepath)` using `torch.save(model.state_dict())` and `load(filepath)` using `model.load_state_dict()`.
- **Required Invariant:** Reloading a saved model yields bit-for-bit identical predictions on `df_test`.
- **Verification Procedure:** Assert `np.allclose(pred_before_save, pred_after_load)`.

## 11. Registry Compatibility
- **Root Cause:** The registry requires instantiation via a consistent factory signature.
- **Scientific Impact:** Evaluator crashes if S2 requires specialized instantiation arguments not provided to H1/M1.
- **Interface Contract:** `__init__(model_id: str, feature_cols: List[str])` must match exactly. Any S2-specific hyperparams (hidden_dim, lr) must be encapsulated as default kwargs.
- **Required Invariant:** `BaselineRegistry.get_baseline_models()` seamlessly instantiates `SequenceBaseline`.
- **Verification Procedure:** Assert successful instantiation loop in `registry.py`.

## 12. MasterEvaluator Compatibility
- **Root Cause:** `MasterEvaluator` expects tabular duck-typing.
- **Scientific Impact:** Strict adherence guarantees Gate 3's identical-evaluation protocol is upheld.
- **Interface Contract:** 
  - `fit(df_train: pd.DataFrame, y_train: np.ndarray, sample_weight: np.ndarray = None)`
  - `predict_proba(df: pd.DataFrame) -> np.ndarray`
- **Required Invariant:** The sequence abstraction is completely hidden; data goes in flat, predictions come out flat.
- **Verification Procedure:** Execute `MasterEvaluator.run_evaluation()` with S2 using dummy data; it must complete end-to-end without shape errors.

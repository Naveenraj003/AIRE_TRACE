# Gate 4: Validation Plan

## 1. Unit Tests
- **Module Validations:** Ensure `encoder.py`, `temporal_model.py`, and `prediction_head.py` function correctly in isolation. 
- **Interface Compliance:** Validate that all method families (H, M, S, L) adhere strictly to the `AbstractMonitor` interface (e.g., `predict_proba()` always returns [0, 1] bounded arrays of matching dimensions).
- **In-Memory Assertions:** Verify that the sequence padder correctly aligns time-series features without data loss, and that the PyTorch tensors allocate within the 4GB VRAM constraint.

## 2. Integration Tests
- **Pipeline Execution:** Ensure the data flow from `TRAIN Parquet -> encoder -> trainer -> predict -> evaluate` executes without failure for the Sequence (S) model.
- **Leakage Guards:** Leverage existing `assert_no_feature_leakage` and `assert_no_split_leakage` guards to ensure the sequence model does not inadvertently consume future data during batched sequence processing.
- **Rule 8 Enforcment:** Programmatically verify that $t > t_{\text{onset}}$ prefixes are dropped during the training loop for failed episodes.

## 3. Scientific Validation
- **Methodology Consistency:** Confirm that the sequence model (S) receives identically constructed observation windows as the classical ML (M) and Heuristic (H) models.
- **Weight Consistency:** Validate that the episode-balanced sample weights ($w_{i,t} = 1 / \min(T_i, 30)$) are being actively utilized by the optimizer during backpropagation.
- **Cost Accounting:** Accurately measure wall-clock latency, peak CPU/GPU memory, and throughput (prefixes/second) for the newly implemented sequence model.

## 4. Benchmark Comparison
- **Mode A (TerminalBench):** Evaluate the complete set of H, M, and S models. Compute AUROC, AUPRC, Recall@FAR (5%), ECE, and Lead Time.
- **Mode B (τ²-Bench):** Apply the frozen thresholds to evaluate H, M, and S on the generalization dataset. Compute AUROC, AUPRC, Recall, and Alert Burden.
- **Statistical Stability:** Execute the $B=100$ episode-cluster bootstrap and generate the Pairwise Direction Consistency (PDC) ranking.

## 5. Ablation Studies
- **Metric-Sensitivity (Gate 7 precursor):** Evaluate how model rankings shift across multiple False Alarm Rate (FAR) tolerance targets (e.g., 1%, 5%, 10%).
- **Feature Ablation (Optional):** Compare the primary common-feature model against a richer TerminalBench-only diagnostic variant to quantify the impact of cross-dataset feature constraints.

## 6. Failure Testing
- **Out of Memory (OOM):** Stress-test the sequence model with maximum sequence lengths and maximum batch sizes to identify the breaking point on the RTX 2050 GPU.
- **Missing Data Handling:** Ensure the model pipeline gracefully handles episodes with $0$ actionable steps or unexpected `NaN` values, falling back or rejecting them cleanly without pipeline collapse.

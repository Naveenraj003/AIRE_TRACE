# Gate 4: Implementation Roadmap

## Gate 4.1: Project Skeleton
- **Objective:** Establish the `src/aire_trace` Python package and internal module structure.
- **Deliverables:** Empty module files (`encoder.py`, `temporal_model.py`, `trainer.py`, etc.) and the `AbstractMonitor` base class definition.
- **Validation:** Linter passes, imports resolve successfully.
- **Stop Condition:** `src/aire_trace` directory structure is committed.

## Gate 4.2: Feature Encoder & Sequence Padding
- **Objective:** Convert flat Parquet manifests into ordered temporal sequences suitable for S/L models.
- **Deliverables:** `encoder.py` capable of standardizing numeric columns and padding variable-length histories.
- **Validation:** Unit tests confirm sequence tensors have dimensions `(batch_size, sequence_length, feature_dim)` without information loss.
- **Stop Condition:** Output tensors are ready for model ingestion.

## Gate 4.3: Temporal Reasoning Model (S)
- **Objective:** Implement the primary Sequence model (1D-CNN or GRU).
- **Deliverables:** `temporal_model.py` and `prediction_head.py` in PyTorch.
- **Validation:** Forward pass runs successfully on a dummy batch without crashing.
- **Stop Condition:** Model architecture is finalized and parameters are initialized.

## Gate 4.4: Semantic / LLM Extension (L) (Optional)
- **Objective:** Attempt to implement the optional local open-weight model integration.
- **Deliverables:** `llm_monitor.py` adapter.
- **Validation:** Hardware VRAM constraint check (must run in <4GB).
- **Stop Condition:** If hardware check fails, safely abort Gate 4.4 and gracefully fall back to H/M/S.

## Gate 4.5: Training Pipeline
- **Objective:** Implement the training loop, strictly enforcing Protocol Rules 8 and 11.
- **Deliverables:** `trainer.py` handling backpropagation, batching, and episode-balanced sample weights.
- **Validation:** Loss decreases over epochs; post-onset filtering is demonstrably enforced.
- **Stop Condition:** Model successfully fits on the TRAIN partition and serializes to disk.

## Gate 4.6: Evaluation & Threshold Calibration
- **Objective:** Integrate the trained models with the threshold calibration and evaluation suite.
- **Deliverables:** `confidence.py` and `inference.py` handling prediction and metric generation.
- **Validation:** Thresholds selected on CALIBRATION yield $\le 5\%$ FAR on CALIBRATION.
- **Stop Condition:** Final binary predictions and probability scores are generated for TEST and τ²-Bench.

## Gate 4.7: Metric Sensitivity & Ablation
- **Objective:** Run PDC analysis and alternative FAR targets.
- **Deliverables:** Raw pairwise-direction tables and PDC statistics.
- **Validation:** PDC is correctly computed using informative pairs (W+L > 0) with documented coverage.
- **Stop Condition:** All statistical artifacts are generated.

## Gate 4.8: Final Comparison & Logging
- **Objective:** Consolidate Gate 4 outputs for Gate 5.
- **Deliverables:** Final canonical JSON/CSV result objects.
- **Validation:** Sanity check final metrics against Gate 3.4 baseline proxy metrics.
- **Stop Condition:** AIRE-Trace implementation is declared complete and ready for formal experiments.

# Gate 4.0: Independent Design Review

**Date:** 2026-08-04  
**Reviewer Role:** External Research Reviewer  
**Status:** **IMPLEMENTATION NOT APPROVED**

---

## 1. Executive Summary

The proposed Gate 4 design contains **BLOCKING** architectural flaws. While the scientific objectives and validation strategies are sound, the structural design introduces severe duplication of the evaluation framework. Specifically, the design proposes building a new, isolated package (`src/aire_trace/`) containing its own training loop (`trainer.py`), inference pipeline (`inference.py`), and calibration logic (`confidence.py`) for the Sequence model. 

Because Gate 3 already implemented the universal evaluation framework (`MasterEvaluator`, `src/evaluation/`), routing the Sequence model through a separate pipeline destroys the core methodological claim of the paper: that all methods are evaluated under *strictly identical* programmatic constraints. If S uses a different inference and calibration codebase than H and M, the comparative claims are scientifically void.

---

## 2. Answers to Specific Questions

**1. Is the proposed architecture internally consistent?**  
**FALSE.** It contradicts the existing repository structure defined in `TECHNICAL_DESIGN.md`. It invents a new `src/aire_trace/` directory instead of utilizing the existing `src/methods/` (or `src/baselines/`) and `src/evaluation/` structure.

**2. Are module responsibilities well separated?**  
**FALSE.** The proposed `confidence.py` overlaps directly with the already-implemented threshold calibration in `src/evaluation/`. `inference.py` overlaps with the existing evaluation harness.

**3. Does the implementation roadmap contain hidden dependencies?**  
**TRUE.** By proposing a new evaluation pipeline (Gates 4.6 and 4.7), the roadmap depends on either rewriting the Gate 3 baselines to use the new pipeline, or dangerously running two separate evaluation pipelines side-by-side and attempting to merge their outputs.

**4. Could any module be simplified?**  
**TRUE.** The entire `src/aire_trace/` package should be abandoned. The Sequence model should simply be a class (e.g., `SequenceMonitor`) located in `src/baselines/sequence.py` (or `src/methods/sequence.py`). 

**5. Is any module unnecessary?**  
**TRUE.** `inference.py`, `confidence.py`, `trainer.py` (as a standalone script), and `registry.py` are redundant. PyTorch training loops should be encapsulated entirely within the `fit()` method of the Sequence model adapter.

**6. Does the design accidentally duplicate baseline functionality?**  
**TRUE.** It duplicates threshold calibration, metrics generation, and inference orchestration, all of which were successfully executed and frozen in Gate 3 for H and M models.

**7. Does the design preserve fair comparison with frozen baselines?**  
**FALSE.** A separate inference and calibration pipeline for S introduces the risk of subtle programmatic divergence from H and M, invalidating the "common protocol" claim.

**8. Is the validation plan sufficient for publication?**  
**TRUE.** The scientific validation, PDC analysis, and failure testing are rigorous, provided they are executed using the unified Gate 3 evaluator.

**9. Are any protocol amendments required before implementation?**  
**TRUE.** The Gate 4 design contract itself must be amended to remove the redundant `src/aire_trace` infrastructure and restrict the scope purely to implementing the `SequenceMonitor` adapter.

**10. Would you approve implementation?**  
**FALSE.** Implementation is BLOCKED until the architectural duplication is resolved.

---

## 3. Classification of Findings

### BLOCKING
- **Evaluation Pipeline Duplication:** The design creates `inference.py` and `confidence.py` for the Sequence model, bypassing the `MasterEvaluator` used for Gate 3. This violates the core requirement that all models be evaluated through identical code paths. The comparison would no longer be strictly fair.

### HIGH
- **Architectural Fragmentation:** Proposing `src/aire_trace/` as a monolithic package ignores the existing separation of concerns (`src/baselines/` and `src/evaluation/`).

### MEDIUM
- **Adapter Interface Mismatch:** The proposed `AbstractMonitor.fit(X: np.ndarray)` assumes a unified input shape. As noted in `TECHNICAL_DESIGN.md`, H/M consume flattened vectors while S requires padded sequence tensors. The interface must explicitly handle this abstraction (e.g., passing a sequence abstraction that the adapter reshapes).
- **Roadmap Bloat:** Sub-gates 4.6 (Evaluation), 4.7 (Ablation), and 4.8 (Final Comparison) are actually Gates 5, 7, and 9. Gate 4 should strictly be the model implementation.

### LOW
- *None.*

### INFORMATIONAL
- The risk assessment correctly identifies VRAM constraints and post-onset masking as the primary implementation risks for the Sequence model.

---

## 4. Required Design Amendments

Before Gate 4.1 can begin, the design must be revised to:
1. **Scrap `src/aire_trace/`:** Restrict the implementation to `src/baselines/sequence.py` (or `src/methods/sequence.py`).
2. **Encapsulate Training:** Place the PyTorch GRU/1D-CNN definition, data loader, and backpropagation loop entirely inside the `SequenceMonitor.fit()` method.
3. **Reuse the Harness:** Rely exclusively on the existing Gate 3 evaluation harness to call `fit()`, `predict_proba()`, and compute calibration thresholds and metrics.
4. **Update the Roadmap:** Remove evaluation and ablation from Gate 4's scope, as they belong to subsequent gates.

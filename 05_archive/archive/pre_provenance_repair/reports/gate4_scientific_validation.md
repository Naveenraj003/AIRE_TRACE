# Gate 4 Scientific Validation Report

**Date:** 2026-08-04  
**Reviewer Role:** Independent Scientific Validator  
**Scope:** Determine whether `gate4_architecture_v2.md` and `gate4_interface_contract.md` support the paper's central scientific claim  
**Target Claim:** "All models are evaluated under an identical evaluation framework."

---

## 1. Documents Under Review

| Document | Path | Date |
|---|---|---|
| Architecture V2 | `reports/gate4_architecture_v2.md` | 2026-08-04 |
| Interface Contract | `reports/gate4_interface_contract.md` | 2026-08-04 |

## 2. Governing Authority Documents

| Document | Path | Role |
|---|---|---|
| Frozen Protocol | `AIRE-Trace_Frozen_Protocol_and_Plan.md` | Scientific source of truth — defines the claim |
| PRD | `PRD.md` | What the software must deliver |
| AGENTS.md | `AGENTS.md` | Enforcement rules |
| TECHNICAL_DESIGN.md | `TECHNICAL_DESIGN.md` | Frozen architecture |

## 3. Source Code Evidence (Canonical Evaluation Pipeline)

| Component | File | Lines | Function |
|---|---|---|---|
| Evaluation engine | `src/evaluation/evaluator.py` | L30-120 | `MasterEvaluator.run_evaluation()` |
| Threshold calibration | `src/evaluation/thresholding.py` | L52-115 | `select_calibration_threshold()` |
| Metric computation | `src/evaluation/metrics.py` | L86-110 | `compute_all_metrics()` |
| Bootstrap CIs | `src/evaluation/bootstrap.py` | L18-114 | `compute_episode_bootstrap_ci()` |
| PDC ranking stability | `src/evaluation/pdc.py` | L89-137 | `compute_overall_pdc()` |
| Model registration | `src/baselines/registry.py` | L11-24 | `BaselineRegistry.get_baseline_models()` |

---

## 4. Criterion-by-Criterion Verification

### 4.1 Identical Evaluation

**Question:** Does every model pass through the same evaluation code path?

**Evidence from `gate4_architecture_v2.md` (Section 3, Execution Flow):**

All models — H1, H2, H3, H4, M1, S1, S2 — pass through the identical loop in `MasterEvaluator.run_evaluation()` (L70-107):

```
for m_id, model in models.items():
    model.fit(df_train, y_train)                               # L76
    prob_calib = model.predict_proba(df_calib)                 # L79
    thresh_dict = select_calibration_threshold(...)            # L80
    prob_test = model.predict_proba(df_test)                   # L86
    metrics_test = compute_all_metrics(df_test, prob_test, frozen_thresh)  # L87
    ci_test = compute_episode_bootstrap_ci(...)                # L93-98
    prob_tau2 = model.predict_proba(df_tau2_k)                 # L105
    metrics_tau2 = compute_all_metrics(df_tau2_k, prob_tau2, frozen_thresh)  # L106
```

The V2 architecture specifies that `SequenceBaseline` (S2) is registered via `BaselineRegistry.get_baseline_models()` and enters this same loop at L70. No model-specific branching exists in `MasterEvaluator`.

**Evidence from `gate4_interface_contract.md` (Section 1, Verified as CORRECT):**

> "Registry Integration: Adding S2: SequenceBaseline to the dictionary is correct."  
> "MasterEvaluator Integration: Exposing fit and predict_proba aligns with the evaluator's expected orchestration."  
> "Threshold Interface: Returning a flat 1D np.ndarray of probabilities allows select_calibration_threshold() to work without modification."

**Evidence from source code:**

`MasterEvaluator` has zero model-type-specific branches. L70 iterates `for m_id, model in models.items()` — duck-typed. Every model that exposes `fit(df, y)` and `predict_proba(df) → np.ndarray` will be processed identically.

**VERDICT: YES — Identical evaluation is structurally guaranteed.**

The V2 architecture ensures that S2 enters the same `for` loop as H1-H4, M1, S1. No model receives special treatment. The evaluation code path is provably singular — there is one `for` loop, one `compute_all_metrics()` call site per split per model, one `select_calibration_threshold()` call site, one bootstrap call site.

---

### 4.2 Fair Comparison

**Question:** Do all models receive the same data, thresholds, and scoring?

| Evaluation input | H1-H4 | M1 | S1 | S2 (V2) | Same? |
|---|---|---|---|---|---|
| Training data | `df_train` (L50, L76) | `df_train` (L50, L76) | `df_train` (L50, L76) | `df_train` (L50, L76) | ✅ |
| Calibration data | `df_calib` (L51, L79) | `df_calib` (L51, L79) | `df_calib` (L51, L79) | `df_calib` (L51, L79) | ✅ |
| Test data | `df_test` (L52, L86) | `df_test` (L52, L86) | `df_test` (L52, L86) | `df_test` (L52, L86) | ✅ |
| τ²-Bench data | `df_tau2_k` (L48, L105) | `df_tau2_k` (L48, L105) | `df_tau2_k` (L48, L105) | `df_tau2_k` (L48, L105) | ✅ |
| Feature columns | `feat_*` (L58) | `feat_*` (L58) | `feat_*` (L58) | `feat_*` (L58) | ✅ |
| Threshold target FAR | 0.05 (L22) | 0.05 (L22) | 0.05 (L22) | 0.05 (L22) | ✅ |
| Threshold code | `thresholding.py` L52-115 | Same | Same | Same | ✅ |
| Metrics code | `metrics.py` L86-110 | Same | Same | Same | ✅ |
| Episode-balanced weights | `compute_sample_weights()` L13-16 | Same | Same | Same | ✅ |
| Bootstrap B | L92-98 | Same | Same | Same | ✅ |

**VERDICT: YES — Fair comparison is structurally guaranteed.**

All models receive identical data, are scored by identical code, and have their thresholds selected by identical logic. The V2 architecture introduces no model-specific data paths, no model-specific threshold logic, and no model-specific metric computation.

---

### 4.3 No Evaluator Bias

**Question:** Does the evaluation engine favor or disadvantage any model?

`MasterEvaluator.run_evaluation()` is model-agnostic. It:

1. Does not inspect `model_id` to branch logic (only for the `L_PENDING` skip at L71)
2. Does not use different metric functions for different models
3. Does not apply different weighting schemes per model
4. Does not modify threshold selection criteria per model
5. Does not use different bootstrap seeds per model

`gate4_architecture_v2.md` preserves this property. S2 enters the same duck-typed loop. The evaluator has no knowledge of whether it is evaluating a rule-based heuristic, a logistic regression, a random forest, or a GRU — it only sees `model.fit()` and `model.predict_proba()`.

**VERDICT: YES — No evaluator bias exists.**

---

### 4.4 No Threshold Leakage

**Question:** Is the frozen threshold provably untouched by TEST data?

**Code evidence (`evaluator.py` L78-87):**

```python
prob_calib = model.predict_proba(df_calib)                         # L79 — CALIB only
thresh_dict = select_calibration_threshold(df_calib, prob_calib, target_far=self.target_far)  # L80 — CALIB only
frozen_thresh = thresh_dict["frozen_threshold"]                    # L81 — frozen

prob_test = model.predict_proba(df_test)                           # L86 — TEST, threshold already frozen
metrics_test = compute_all_metrics(df_test, prob_test, frozen_thresh, max_k=max_k)  # L87 — threshold used, not modified
```

The threshold is selected on L80 (CALIB data only), frozen on L81, and applied unchanged on L87 (TEST) and L106 (τ²-Bench). No code path between L81 and L87 modifies `frozen_thresh`. `select_calibration_threshold()` does not accept TEST data — it takes `df_calib` and `y_prob_calib` as arguments.

**V2 architecture preserves this:** S2 follows the identical `predict_proba(df_calib)` → `select_calibration_threshold()` → `predict_proba(df_test)` sequence. No model-specific calibration path exists.

**VERDICT: YES — No threshold leakage. Threshold is provably frozen before TEST evaluation.**

---

### 4.5 No Duplicated Metrics

**Question:** Does the design contain a single, non-duplicated metric computation?

**V2 design evidence:**

`gate4_architecture_v2.md` Section 7 ("Explicitly Out of Scope"):

> "New `AbstractMonitor` base class — NOT BUILT — unnecessary"  
> "`src/aire_trace/` package — NOT BUILT — violates frozen architecture"  
> "`confidence.py`, `inference.py`, `trainer.py` — NOT BUILT — duplicates evaluation pipeline"

`gate4_architecture_v2.md` Section 1 ("What is NOT created"):

> "❌ No `confidence.py`, `inference.py`, `trainer.py`"  
> "❌ No new evaluation pipeline"

The only metric computation code is `compute_all_metrics()` in `src/evaluation/metrics.py`. The V2 design explicitly prohibits any metric computation inside the model class. The original `AbstractMonitor.evaluate()` convenience method (which was a duplicate metric producer) was eliminated in V2.

**Evidence from `gate4_interface_contract.md`:** The interface contract review does not identify any metric-computation capability in `SequenceBaseline`. It confirms the model produces only probabilities.

**VERDICT: YES — Single metric computation. No duplication.**

---

### 4.6 Single Statistical Pipeline

**Question:** Is there exactly one statistical analysis code path?

The statistical layer consists of:

1. `compute_all_metrics()` — `src/evaluation/metrics.py` L86-110
2. `compute_episode_bootstrap_ci()` — `src/evaluation/bootstrap.py` L18-114
3. `compute_overall_pdc()` — `src/evaluation/pdc.py` L89-137

All three are called exclusively by `MasterEvaluator.run_evaluation()`. The V2 design does not create any parallel statistical code path. No model class computes its own statistics.

**VERDICT: YES — Single statistical pipeline.**

---

### 4.7 Single Bootstrap Implementation

**Question:** Is there exactly one bootstrap implementation?

`compute_episode_bootstrap_ci()` in `src/evaluation/bootstrap.py` is the sole bootstrap implementation. It:
- Resamples at the episode level (L76: `rng.choice(n_episodes, size=n_episodes, replace=True)`)
- Computes all 6 metrics per iteration
- Returns 95% CIs via `np.percentile(arr, 2.5)` and `np.percentile(arr, 97.5)`

V2 does not create a second bootstrap. V2's scope (Section 7) explicitly defers bootstrap to Gate 5, where it will run through the unchanged `MasterEvaluator`.

**VERDICT: YES — Single bootstrap implementation.**

---

### 4.8 Single PDC Implementation

**Question:** Is there exactly one PDC computation?

`compute_overall_pdc()` in `src/evaluation/pdc.py` is the sole PDC implementation. It computes pairwise direction consistency across the 4 primary metrics (AUROC, AUPRC, Recall_at_FAR, ECE) for all method pairs. It is called once by `MasterEvaluator` at L110.

V2 does not create a second PDC computation. When S2 is added to the model registry, `compute_overall_pdc()` will automatically include it in the pairwise comparison matrix because it iterates `methods = list(results_by_method.keys())` (L96 of `pdc.py`).

**VERDICT: YES — Single PDC implementation.**

---

### 4.9 Single Reporting Implementation

**Question:** Is there exactly one reporting pipeline?

Results are assembled by `MasterEvaluator.run_evaluation()` at L112-120 into a single dictionary containing `mode_a_terminalbench_test`, `mode_b_tau2_bench`, `calibrated_thresholds`, `bootstrap_confidence_intervals`, and `pdc_summary`. The experiment runner (`run_gate3_experiments.py`) writes this to `primary_k30_results.json` and generates the CSV comparison table.

V2 does not create a second reporting path. Section 7 defers "Final comparison tables" to Gate 9.

**VERDICT: YES — Single reporting implementation.**

---

### 4.10 Single Threshold Calibration Implementation

**Question:** Is there exactly one threshold calibration implementation?

`select_calibration_threshold()` in `src/evaluation/thresholding.py` (L52-115) is the sole threshold calibration function. It:
- Sweeps 99 candidate thresholds in [0.01, 0.99]
- Selects the threshold maximizing recall subject to FAR ≤ `target_far`
- Returns a single `frozen_threshold` value

V2 explicitly eliminates the original `confidence.py` which would have duplicated this logic. V2 Section 8 confirms: "V-1 (Second calibration pipeline) — ✅ Eliminated — `confidence.py` not created" and "V-3 (Duplicate threshold calibration) — ✅ Eliminated — single path through `thresholding.py`."

**VERDICT: YES — Single threshold calibration implementation.**

---

## 5. Interface Contract Findings (From `gate4_interface_contract.md`)

The interface contract review identified 4 mismatches. These are **implementation-level details** that affect whether S2 will run correctly, but they do **not** affect whether the evaluation framework is identical. The critical distinction:

| Mismatch | Nature | Affects evaluation identity? |
|---|---|---|
| Forward tensor shape ([B,1] vs [B,K,1]) | S2 internal architecture detail | **NO** — MasterEvaluator only sees `np.ndarray [N]` output |
| Row index preservation | S2 internal implementation detail | **NO** — as long as the output ndarray aligns with input DataFrame rows (which the mismatch report correctly flags must be enforced), the evaluator treats S2 identically |
| Loss computation tensor shapes | S2 internal training detail | **NO** — MasterEvaluator calls `model.fit(df, y)` and doesn't inspect loss computation |
| Missing save/load | Serialization convenience | **NO** — MasterEvaluator doesn't call save/load; these are runner-level concerns |

> [!IMPORTANT]
> **All 4 mismatches are internal to `SequenceBaseline` and invisible to `MasterEvaluator`.** They are implementation bugs that will cause S2 to crash or produce incorrect predictions, but they do not create a second evaluation pipeline. They must be resolved during Gate 4 implementation, but they do not threaten the "identical evaluation framework" claim.

The interface contract correctly identifies that the critical invariant is:

> "`predict_proba(df)` must return an `np.ndarray [N]` that aligns exactly with the row order of the input `df`."

As long as this invariant holds, `MasterEvaluator` processes S2 identically to all other models.

---

## 6. Residual Risks

Two legitimate residual risks exist that could theoretically weaken the claim, even though the V2 architecture structurally prevents them:

### Risk 1: Feature information asymmetry

Heuristic models (H1-H3) consume a single feature column. ML models (M1, S1) consume all `feat_*` columns. `SequenceBaseline` (S2) consumes the same `feat_*` columns but processes them as temporal sequences rather than flat vectors.

**Assessment:** This is an intentional and protocol-compliant difference. The frozen protocol (Section 6) defines S as "Small GRU/1D-CNN over the feature time series" — the entire point of the S family is to exploit temporal ordering that H/M ignore. The "identical evaluation" claim refers to the evaluation framework (calibration, metrics, bootstrap, PDC), not the model's internal feature representation. All models receive the same `pd.DataFrame` with the same columns; what each model does internally is its architectural contribution.

**Verdict: NOT a violation.** The protocol explicitly expects models to differ in how they process features.

### Risk 2: Training weight consistency

`MasterEvaluator` L76 calls `model.fit(df_train, y_train)` without `sample_weight`. This is the same for all models (existing Rule 11 deviation, flagged in Gate 3.4 as D-4). V2 does not introduce a new inconsistency — S2 would receive the same (absent) weights as M1 and S1.

**Assessment:** This is a pre-existing protocol deviation that applies equally to all trainable models. It does not create an inter-model evaluation asymmetry.

**Verdict: NOT a new violation.** Pre-existing, applies equally.

---

## 7. Final Answer

### Can Gate 4 now legitimately claim: "All models are evaluated under an identical evaluation framework"?

## **YES.**

### Justification Summary

| Criterion | Verdict | Evidence |
|---|---|---|
| Identical evaluation | **YES** | Single `for` loop in `MasterEvaluator` (L70-107); no model-specific branches |
| Fair comparison | **YES** | Same data, same splits, same threshold logic, same metrics for every model |
| No evaluator bias | **YES** | Evaluator is model-agnostic; duck-typed interface; no `model_id`-dependent logic |
| No threshold leakage | **YES** | Threshold frozen at L81 before TEST evaluation at L87; `select_calibration_threshold()` accepts only CALIB data |
| No duplicated metrics | **YES** | `compute_all_metrics()` is the sole metric function; `AbstractMonitor.evaluate()` eliminated |
| Single statistical pipeline | **YES** | Three statistical functions (`metrics`, `bootstrap`, `pdc`) called only by `MasterEvaluator` |
| Single bootstrap implementation | **YES** | `compute_episode_bootstrap_ci()` is the sole bootstrap; no parallel implementation |
| Single PDC implementation | **YES** | `compute_overall_pdc()` is the sole PDC; auto-includes new models via key iteration |
| Single reporting implementation | **YES** | `MasterEvaluator` assembles results; no parallel reporting path |
| Single threshold calibration | **YES** | `select_calibration_threshold()` is the sole calibration; `confidence.py` not created |

### The claim is defensible because:

1. **Structural guarantee:** The V2 architecture introduces zero new evaluation code. The only new artifacts are a model class (`src/baselines/sequence.py`) and a registry entry. Everything after probability generation reuses Gate 3 unchanged.

2. **Provably single code path:** There is exactly one `for` loop in `MasterEvaluator.run_evaluation()` that processes every model. No conditional branch based on model type exists except the `L_PENDING` skip.

3. **Interface encapsulation:** `SequenceBaseline` presents the same `fit(df, y)` / `predict_proba(df) → np.ndarray` contract as all existing models. Internal PyTorch mechanics are invisible to the evaluator.

4. **No scope creep:** V2 explicitly defers evaluation (Gate 5), ablation (Gate 7), and reporting (Gate 9) to their assigned gates, preventing any Gate-4-internal evaluation path from emerging.

5. **Interface contract mismatches are internal:** The 4 mismatches identified in `gate4_interface_contract.md` are implementation details *within* the model class, not in the evaluation framework. They will cause S2 to crash if unresolved, but they cannot break the "identical framework" property because `MasterEvaluator` never enters model-internal code.

### Caveats

1. The "identical evaluation framework" claim does not extend to training methodology — models intentionally differ in how they process features (H: training-free, M: tabular ML, S: sequence model). This is by protocol design, not a flaw.

2. The 4 interface contract mismatches (tensor shapes, row ordering, save/load) must be resolved during Gate 4 implementation to ensure S2 produces correct predictions. Incorrect predictions would not violate "identical evaluation" but would invalidate the scientific results.

---

**Scientific Validation Status: PASSED — All 10 criteria verified. Gate 4 can legitimately claim identical evaluation.**

*No code was modified. No experiments were regenerated. This is a validation-only report.*

# Gate 4.0.1: Architecture Reconciliation Report

**Date:** 2026-08-04  
**Auditor Role:** Protocol Reconciliation Reviewer  
**Status:** BLOCKING VIOLATIONS CONFIRMED — DESIGN AMENDMENT REQUIRED  
**Scope:** Verify whether the Gate 4 design (as documented in `gate4_architecture.md`, `gate4_design_overview.md`, `gate4_implementation_roadmap.md`, and `gate4_validation_plan.md`) violates the frozen architecture defined in `TECHNICAL_DESIGN.md`, the frozen protocol in `AIRE-Trace_Frozen_Protocol_and_Plan.md`, the requirements in `PRD.md`, and the enforcement rules in `AGENTS.md`.

---

## 1. Evidence Sources

| ID | Document | Authority Level |
|---|---|---|
| E1 | `AGENTS.md` | Rank 3 — enforcement rules |
| E2 | `AIRE-Trace_Frozen_Protocol_and_Plan.md` | Rank 1 — scientific source of truth |
| E3 | `PRD.md` | Rank 2 — what software must deliver |
| E4 | `TECHNICAL_DESIGN.md` | Rank 4 — how system is organized |
| E5 | `reports/gate3_4_final_verdict.md` | Authoritative — Gate 3.4 pass verdict |
| E6 | `reports/gate4_design_review.md` | Authoritative — external design review |
| E7 | `reports/gate4_architecture.md` | Under review — Gate 4 proposed design |
| E8 | `reports/gate4_implementation_roadmap.md` | Under review — Gate 4 sub-gate plan |
| E9 | `src/evaluation/evaluator.py` | Rank 2 (source code) — executed evaluation engine |
| E10 | `src/baselines/registry.py` | Rank 2 (source code) — executed model registry |

---

## 2. Verification A: Does Gate 4 introduce a second evaluation pipeline?

**VERDICT: YES — VIOLATION CONFIRMED**

### Evidence

`gate4_architecture.md` Section "Module Responsibilities" (L9-19) defines:

- `confidence.py`: "Analyzes internal prediction confidence, enabling threshold calibration and ECE calculation."
- `inference.py`: "Orchestrates checkpoint-by-checkpoint prediction."

`gate4_architecture.md` Section "Calibration Flow" (L25-27):

> "CALIBRATION Parquet records → `inference.py` → `confidence.py`. The evaluation harness selects the optimal risk threshold achieving the target FAR."

This is a **second calibration pipeline**. The executed, canonical calibration pipeline is:

`MasterEvaluator.run_evaluation()` → `model.predict_proba(df_calib)` → `select_calibration_threshold()` → frozen threshold

The Gate 4 design routes through `inference.py` → `confidence.py` instead, creating a parallel path.

### Protocol Violation

| Document | Section | Violated Principle |
|---|---|---|
| `AIRE-Trace_Frozen_Protocol_and_Plan.md` | Section 4, Mode A/B separation | "all model fitting and threshold calibration for H/M/S(/L) happens on TerminalBench only" — threshold calibration must go through a **single** procedure, not two dataset-specific or method-specific pipelines |
| `TECHNICAL_DESIGN.md` | Section 2.8 | "Single-threshold contract across modes: calibration happens exactly once per method... The module's API should make a second, dataset-specific threshold structurally impossible to produce" |
| `PRD.md` | Section 5, step 5-6 | The workflow specifies "Calibrate alert thresholds for all applicable methods... on CALIBRATION per the frozen threshold procedure" — one procedure, not method-family-specific pipelines |
| `AGENTS.md` | Section 1, absolute prohibition 7 | "Never present a τ²-Bench (Mode B) AUROC/AUPRC/calibration number next to a TerminalBench (Mode A) one as though they measure the same thing." A second pipeline increases the risk of unlabeled metrics |

### Required Correction

Remove `confidence.py` and `inference.py` from the Gate 4 scope. The Sequence model must produce probabilities via `predict_proba(df)` → `np.ndarray`, identical to H/M models. All calibration must flow through the existing `select_calibration_threshold()` in `src/evaluation/thresholding.py`.

---

## 3. Verification B: Does Gate 4 duplicate threshold calibration, evaluation, metrics, bootstrap, PDC, or reporting outside MasterEvaluator?

**VERDICT: YES — DUPLICATION CONFIRMED IN 4 OF 6 AREAS**

### Specific Duplications

| Component | Existing Canonical Location | Gate 4 Proposed Duplicate | Status |
|---|---|---|---|
| Threshold calibration | `src/evaluation/thresholding.py` → `select_calibration_threshold()` | `src/aire_trace/confidence.py` → "enabling threshold calibration" (L16) | ❌ DUPLICATE |
| Evaluation orchestration | `src/evaluation/evaluator.py` → `MasterEvaluator.run_evaluation()` | `src/aire_trace/inference.py` → "Orchestrates checkpoint-by-checkpoint prediction" (L18) | ❌ DUPLICATE |
| Metrics computation | `src/evaluation/metrics.py` → `compute_all_metrics()` | `AbstractMonitor.evaluate()` → "Convenience function for internal metrics generation" (L99-104 of `gate4_architecture.md`) | ❌ DUPLICATE |
| Bootstrap | `src/evaluation/bootstrap.py` → `compute_episode_bootstrap_ci()` | Not duplicated in Gate 4 design | ✅ NOT DUPLICATED |
| PDC | `src/evaluation/pdc.py` → `compute_overall_pdc()` | Not duplicated in Gate 4 design | ✅ NOT DUPLICATED |
| Reporting | `src/run_gate3_experiments.py` | `gate4_implementation_roadmap.md` Gate 4.8: "Consolidate Gate 4 outputs" (L45-49) | ⚠️ IMPLICIT DUPLICATE — proposes generating its own "canonical JSON/CSV result objects" outside the existing pipeline |

### Protocol Violation

| Document | Section | Violated Principle |
|---|---|---|
| `TECHNICAL_DESIGN.md` | Section 1, Pipeline Architecture | The architecture diagram shows a single funnel: all methods → "Threshold Calibration (Section 8)" → "Common Evaluator" → "Statistical Layer (Rule 7)". No method-specific evaluation branch exists. |
| `TECHNICAL_DESIGN.md` | Section 2.9 | "Common Evaluator (`evaluation/metrics.py`) — Computes the full metric set." The word "Common" is deliberate — metrics are computed once, for all methods, through one code path. |
| `PRD.md` | Section 4 | "every method receives identical information, is scored against identical failure-target and alert definitions" — identical scoring requires identical code paths, not functionally-equivalent-but-separate ones |

### Required Correction

1. Delete `confidence.py`, `inference.py`, and `AbstractMonitor.evaluate()` from the design.
2. The Sequence model class exposes only `fit(df, y)` and `predict_proba(df) → np.ndarray`.
3. `MasterEvaluator` calls these methods identically to how it calls H/M models today.

---

## 4. Verification C: Does Gate 4 create a standalone inference framework instead of integrating into Gate 3?

**VERDICT: YES — STANDALONE FRAMEWORK CONFIRMED**

### Evidence

`gate4_architecture.md` Section "Module Responsibilities" (L9-19) proposes **10 new modules** inside `src/aire_trace/`:

```
registry.py, encoder.py, temporal_model.py, feature_fusion.py,
prediction_head.py, confidence.py, trainer.py, inference.py, utils.py
```

This constitutes a standalone inference framework with its own:
- Registration (`registry.py` — duplicates `src/baselines/registry.py`)
- Feature pipeline (`encoder.py` — new preprocessing layer outside canonical pipeline)
- Training loop (`trainer.py` — standalone training orchestration)
- Inference orchestration (`inference.py` — standalone evaluation orchestration)
- Threshold logic (`confidence.py` — duplicates `src/evaluation/thresholding.py`)

### Comparison with Existing Gate 3 Architecture

| Concern | Gate 3 (Executed) | Gate 4 (Proposed) |
|---|---|---|
| Model location | `src/baselines/{heuristics,logistic,random_forest}.py` | `src/aire_trace/temporal_model.py` + `prediction_head.py` |
| Registration | `src/baselines/registry.py` | `src/aire_trace/registry.py` (separate) |
| Feature prep | Inline in model classes (e.g., `LogisticBaseline.fit()` calls `self.scaler.fit_transform()`) | `src/aire_trace/encoder.py` (separate module) |
| Training | `model.fit(df_train, y_train)` called by `MasterEvaluator` L76 | `src/aire_trace/trainer.py` (standalone loop) |
| Inference | `model.predict_proba(df)` called by `MasterEvaluator` L79/86/105 | `src/aire_trace/inference.py` (standalone orchestrator) |
| Calibration | `select_calibration_threshold()` called by `MasterEvaluator` L80 | `src/aire_trace/confidence.py` (separate) |

### Protocol Violation

| Document | Section | Violated Principle |
|---|---|---|
| `TECHNICAL_DESIGN.md` | Section 2.7 | Method families are located in `methods/` (or `src/baselines/`): `heuristic.py`, `classical_ml.py`, `sequence.py`. The design places them in a monolithic `src/aire_trace/` package instead. |
| `TECHNICAL_DESIGN.md` | Section 1, Pipeline Architecture | The architecture diagram shows methods as leaf nodes feeding into a single funnel. They are not self-contained frameworks. |
| `gate4_design_review.md` | Section 3, BLOCKING | "The design creates `inference.py` and `confidence.py` for the Sequence model, bypassing the `MasterEvaluator` used for Gate 3. This violates the core requirement that all models be evaluated through identical code paths." |

### Required Correction

1. The Sequence model is a single class in `src/baselines/sequence.py` (conforming to `TECHNICAL_DESIGN.md` Section 2.7's `methods/sequence.py` location, mapped to the existing `src/baselines/` directory).
2. PyTorch model definition, data loading, and backpropagation are encapsulated entirely within `SequenceBaseline.fit()`.
3. Registration is done by adding the new model to `BaselineRegistry.get_baseline_models()` in `src/baselines/registry.py`.
4. No `src/aire_trace/` package is created.

---

## 5. Verification D: Does the design violate identical evaluation conditions for baselines and AIRE-Trace?

**VERDICT: YES — IDENTICAL CONDITIONS NOT GUARANTEED**

### Evidence

The `AbstractMonitor` interface in `gate4_architecture.md` (L56-105) defines:

```python
def fit(self, X: np.ndarray, y: np.ndarray, weights: np.ndarray = None) -> None:
```

But the executed Gate 3 interface is:

```python
def fit(self, df_train: pd.DataFrame, y_train: np.ndarray, sample_weight: np.ndarray = None):
```

The Gate 4 design changes the input from `pd.DataFrame` to `np.ndarray`, introduces a new `evaluate()` method, and adds `save()`/`load()` methods that don't exist on Gate 3 models. If the Sequence model implements this different interface, `MasterEvaluator.run_evaluation()` (L76) cannot call it — it calls `model.fit(df_train, y_train)` and `model.predict_proba(df_test)`, both taking DataFrames.

### Protocol Violation

| Document | Section | Violated Principle |
|---|---|---|
| `AIRE-Trace_Frozen_Protocol_and_Plan.md` | Section 1 | "every method receives exactly the same partial information, the same failure definition and alert constraints, and is scored on common accuracy, calibration, false-alarm, lead-time, and cost metrics" — different interfaces ≠ same information |
| `PRD.md` | Section 4 | "every method receives identical information, is scored against identical failure-target and alert definitions" |
| `PRD.md` | Section 9 | "Every reported CI is episode-cluster bootstrapped (Rule 7) — no prefix-level pseudo-replication anywhere in the codebase" — a second evaluation path could bypass this |

### Required Correction

The Sequence model must conform to the exact same interface as existing Gate 3 models:

```python
def fit(self, df_train: pd.DataFrame, y_train: np.ndarray, sample_weight: np.ndarray = None)
def predict_proba(self, df: pd.DataFrame) -> np.ndarray
```

Internal reshaping (DataFrame → padded tensor sequences) happens privately inside `fit()` and `predict_proba()`, invisible to `MasterEvaluator`.

---

## 6. Verification E: Does the proposed architecture weaken scientific comparability?

**VERDICT: YES — TWO SPECIFIC WEAKENING MECHANISMS IDENTIFIED**

### Mechanism 1: Code-path divergence

If S flows through `inference.py` → `confidence.py` while H/M flow through `MasterEvaluator` → `thresholding.py`, any subtle implementation difference (e.g., floating-point rounding, threshold search grid, FAR computation) between the two code paths would produce method-specific evaluation artifacts. The paper's central claim — "scored on common … metrics" — becomes unfalsifiable because the "common" code path is no longer common.

### Mechanism 2: Interface-level information asymmetry

The `AbstractMonitor.evaluate()` convenience method (L99-104 of `gate4_architecture.md`) allows the Sequence model to generate its own internal metrics. These self-reported metrics could diverge from `MasterEvaluator`'s metrics computation (e.g., different weighting, different threshold application), creating two incompatible metric sets for the same model.

### Protocol Violation

| Document | Section | Violated Principle |
|---|---|---|
| `AIRE-Trace_Frozen_Protocol_and_Plan.md` | Section 8 | "Ranking-stability statistic (frozen now)" — PDC requires all methods' metrics to be computed by the same code path to be a valid comparison |
| `TECHNICAL_DESIGN.md` | Section 2.9 | "Common Evaluator" — "common" means all methods, not "common among H/M but separate for S" |

### Required Correction

Remove `AbstractMonitor.evaluate()`. The only metric-producing code path is `MasterEvaluator` → `compute_all_metrics()`. Models produce probabilities only.

---

## 7. Additional Violation: Gate 4 Roadmap Scope Creep

`gate4_implementation_roadmap.md` defines sub-gates 4.6–4.8:

- **Gate 4.6:** "Evaluation & Threshold Calibration" — this is Gate 5's scope
- **Gate 4.7:** "Metric Sensitivity & Ablation" — this is Gate 7's scope  
- **Gate 4.8:** "Final Comparison & Logging" — this is Gate 9's scope

### Protocol Violation

| Document | Section | Violated Principle |
|---|---|---|
| `docs/ROADMAP.md` | Gates 5, 7, 9 | These gates are explicitly defined and scoped. Moving their functionality into Gate 4 sub-gates collapses the gate structure. |
| `AGENTS.md` | Section 2 | "No scope creep without an explicit, written amendment. The out-of-scope list in PRD.md Section 6 is binding." |

### Required Correction

Gate 4 scope is strictly: **implement the Sequence model class and register it**. Evaluation (Gate 5), ablation (Gate 7), and paper evidence (Gate 9) remain in their assigned gates.

---

## 8. Summary of All Violations

| ID | Verification | Violation | Severity | Required Correction |
|---|---|---|---|---|
| V-1 | A | Second calibration pipeline via `confidence.py` | **BLOCKING** | Delete `confidence.py`; use `select_calibration_threshold()` |
| V-2 | A | Second inference pipeline via `inference.py` | **BLOCKING** | Delete `inference.py`; use `MasterEvaluator` |
| V-3 | B | Duplicate threshold calibration | **BLOCKING** | Single path: `MasterEvaluator` → `thresholding.py` |
| V-4 | B | Duplicate evaluation orchestration | **BLOCKING** | Single path: `MasterEvaluator.run_evaluation()` |
| V-5 | B | Duplicate metrics via `AbstractMonitor.evaluate()` | HIGH | Delete `evaluate()` method |
| V-6 | B | Implicit duplicate reporting (Gate 4.8) | MEDIUM | Defer to Gate 5/9 |
| V-7 | C | Standalone `src/aire_trace/` framework | **BLOCKING** | Model goes in `src/baselines/sequence.py` |
| V-8 | C | Duplicate registry (`src/aire_trace/registry.py`) | HIGH | Extend existing `BaselineRegistry` |
| V-9 | D | Interface mismatch (`np.ndarray` vs `pd.DataFrame`) | **BLOCKING** | Match existing `fit(df, y)` / `predict_proba(df)` signature |
| V-10 | E | Code-path divergence weakens comparability | **BLOCKING** | Single evaluation code path for all methods |
| V-11 | E | Self-reported metrics via `evaluate()` | HIGH | Delete; metrics come from `compute_all_metrics()` only |
| V-12 | — | Roadmap scope creep (Gates 4.6–4.8) | MEDIUM | Restrict Gate 4 to model implementation only |

**Total: 6 BLOCKING + 3 HIGH + 2 MEDIUM violations.**

---

## 9. Reconciliation Verdict

**The Gate 4 design as currently documented VIOLATES the frozen architecture in 11 ways, 6 of which are BLOCKING.**

The design must be rewritten to satisfy a single invariant:

> **Gate 4 introduces exactly ONE new artifact into the repository: a Sequence model class in `src/baselines/sequence.py` that conforms to the existing `fit(df, y)` / `predict_proba(df)` interface. Everything downstream — threshold calibration, evaluation, bootstrap, PDC, reporting — remains unchanged and flows through `MasterEvaluator`.**

No new packages. No new evaluation pipelines. No new registries. No scope creep.

---

*No code was modified. No design was implemented. This is a reconciliation-only review.*

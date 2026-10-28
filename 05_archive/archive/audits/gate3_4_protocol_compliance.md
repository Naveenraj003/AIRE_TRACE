# Gate 3.4 Protocol Compliance Audit

**Date:** 2026-08-04  
**Auditor Role:** Independent Scientific Auditor  
**Status:** COMPLETE — DEVIATIONS CATALOGUED  
**Scope:** Comparison of implemented repository against all governing protocol documents.

---

## 1. Governing Documents Examined

| Document | Path | Role per AGENTS.md precedence |
|---|---|---|
| Frozen Protocol | `AIRE-Trace_Frozen_Protocol_and_Plan.md` | Scientific source of truth (Rank 1) |
| PRD | `PRD.md` | What the software must deliver (Rank 2) |
| AGENTS.md | `AGENTS.md` | What must never be violated (Rank 3) |
| Technical Design | `TECHNICAL_DESIGN.md` | How the system is organized (Rank 4) |
| Research Log | `RESEARCH_LOG.md` | What real data forced us to decide (Rank 5) |
| Roadmap | `docs/ROADMAP.md` | Gate tracking |
| Project Control | `docs/PROJECT_CONTROL.md` | Project state |
| Decision Log | `docs/DECISION_LOG.md` | Frozen decisions |

---

## 2. Verification Matrix

### 2.1 Dataset Count

| Item | Protocol Specification | Implemented Reality | Status |
|---|---|---|---|
| Number of datasets | 2 primary (TerminalBench + τ²-Bench), Tracebench for onset annotations | 3 datasets ingested (TerminalBench, Tracebench, τ²-Bench) | ✅ Compliant |
| TerminalBench episodes (raw) | Confirmed at Gate 1: 52,104 | `dataset_manifest.json`: 52,104 | ✅ Compliant |
| τ²-Bench episodes | Confirmed at Gate 1: 1,980 | `dataset_manifest.json`: 1,980 | ✅ Compliant |
| Tracebench episodes | Confirmed at Gate 1: 3,316 | `dataset_manifest.json`: 3,316 | ✅ Compliant |

**Classification: No deviation.**

### 2.2 Split Policy

| Item | Protocol Specification | Implemented Reality | Status | Classification |
|---|---|---|---|---|
| Split method | Episode-level, task-group disjoint (Rule 3, Section 4) | `src/preprocessing/splitter.py`: Task-group disjoint split with zero overlap assertions | ✅ Compliant | — |
| Split ratios | 53/18/18 tasks (TRAIN/CALIB/TEST) | `configs/data.yaml`: 53/18/18 | ✅ Compliant | — |
| τ²-Bench split | Evaluation-only, no split (Section 4) | `src/preprocessing/normalizer.py` L142: `split="eval_only"` | ✅ Compliant | — |
| Seed | 42 | `splitter.py` default, `configs/data.yaml`, `run_gate3_experiments.py` L39: seed=42 | ✅ Compliant | — |

**Classification: No deviation.**

### 2.3 Episode Definition

| Item | Protocol Specification | Implemented Reality | Status | Classification |
|---|---|---|---|---|
| Episode = complete agent trajectory | Each episode is one full agent run on one task | `src/schemas/canonical.py`: EpisodeRecord contains `episode_id`, `task_id`, `total_steps`, `eventual_outcome` | ✅ Compliant | — |
| Empty episodes filtered | Not explicitly specified in protocol | Gate 3.2 confirmed: 17,642 empty episodes filtered (0 steps). 34,462 non-empty retained | ⚠️ Unresolved question | Documentation wording |

> [!NOTE]
> **D-1 (Documentation wording):** The frozen protocol does not explicitly address empty trajectories (episodes with 0 steps). The project filters them out during preprocessing, which is defensible (no prefix features can be computed from 0 steps), but this filtering is not documented as a protocol decision. It was retroactively justified in Gate 3.2 as "non-actionable," but a formal protocol amendment was never written per AGENTS.md Section 2's requirement.

### 2.4 Task Definition

| Item | Protocol Specification | Implemented Reality | Status |
|---|---|---|---|
| Task = benchmark problem ID | Each dataset has a unique task_id per problem | `src/schemas/canonical.py`: `task_id` field in EpisodeRecord | ✅ Compliant |
| Task-disjoint split | All episodes of task T_i in exactly one split | `src/preprocessing/splitter.py` L29-31: runtime assertions | ✅ Compliant |

**Classification: No deviation.**

### 2.5 Prefix Definition

| Item | Protocol Specification | Implemented Reality | Status | Classification |
|---|---|---|---|---|
| Checkpoint schedule | Outcome-independent, episode-symmetric: t ∈ {1, …, min(T_i, K)} (Rule 1) | `src/preprocessing/prefix_generator.py` generates prefixes t=1 to min(T_i, K) | ✅ Compliant | — |
| Horizon K | K=30 primary, K∈{10,20,30} sensitivity (Gate 1 finding) | `configs/data.yaml`: max_horizon_k=30, sensitivity=[10,20,30] | ✅ Compliant | — |
| No post-terminal padding | Prefixes must not extend beyond natural termination | Gate 2 validation: `5_prefixes_stop_at_natural_termination: true` | ✅ Compliant | — |
| Feature vector | X_t = f(e_1, …, e_t) only — no future events (Rule 2) | Features computed cumulatively per `prefix_generator.py` | ✅ Compliant | — |

**Classification: No deviation.**

### 2.6 Feature Schema

| Item | Protocol Specification | Implemented Reality | Status | Classification |
|---|---|---|---|---|
| Cross-dataset compatibility (Rule 9) | Primary transferable model uses only features computable on both datasets | Category A features used: `steps_so_far`, `actor_role`, `action_type`, `tool_error_count`, `retry_count`, `unique_tools_used`, `tool_call_ratio`, `repeated_action_last2` | ✅ Compliant | — |
| No TerminalBench-only features in primary model | Tokens, cost, duration must not enter shared model | Registry uses only `feat_*` columns from processed manifests | ✅ Compliant | — |
| `gate2_validation_report.json` check 10 | `identical_transfer_feature_schema: true` | Validated | ✅ Compliant | — |

**Classification: No deviation.**

### 2.7 Baseline Taxonomy

| Item | Protocol Specification (Section 6) | Implemented Reality | Status | Classification |
|---|---|---|---|---|
| **H** — Heuristic | Rule-based, training-free | H1 (tool error), H2 (retry), H3 (repeated action), H4 (combined z-score with sigmoid) | ✅ Compliant | — |
| **M** — Classical ML | Logistic regression / XGBoost | M1: LogisticRegression (`src/baselines/logistic.py`) | ✅ Compliant | — |
| **S** — Sequence model | Small GRU/1D-CNN over feature time series | S1: **RandomForestClassifier** (`src/baselines/random_forest.py`) | ❌ **DEVIATION** | **Protocol drift** |
| **L** — Semantic/LLM | Optional, local open-weight | L: "L_PENDING" placeholder | ✅ Compliant (optional) | — |

> [!CAUTION]
> **D-2 (Protocol drift — HIGH SEVERITY):** The frozen protocol explicitly defines the S family as "Small GRU/1D-CNN over the feature time series." The implemented S1 is a RandomForestClassifier — a tabular ensemble method that belongs to the M (Classical ML) family. This means the repository has **two M-family models (LogReg + RF)** and **zero S-family models**, which fundamentally changes the experiment's ability to answer the core research question about H vs M vs S ranking stability.
>
> The gate reports acknowledge S1 is "Random Forest" but never flag this as a protocol deviation or document it as an intentional amendment. Per AGENTS.md: "Frozen decisions change by deliberate amendment, not by whatever turned out to be convenient while coding."

### 2.8 Evaluation Protocol

| Item | Protocol Specification | Implemented Reality | Status | Classification |
|---|---|---|---|---|
| Mode A — TerminalBench TEST | Full prospective evaluation | Evaluated with all specified metrics | ✅ Compliant | — |
| Mode B — τ²-Bench | Eventual-outcome diagnostic only | Evaluated with frozen thresholds | ✅ Compliant | — |
| Mode labeling (Section 4) | Every metric must be labeled with its mode | CSV: `dataset="TerminalBench (Mode A)"` | ✅ Compliant | — |
| Mode B τ²-Bench labeling | Must never be presented as equivalent to Mode A | JSON: separate `mode_a_terminalbench_test` and `mode_b_tau2_bench` keys | ✅ Compliant | — |
| Threshold frozen before TEST | Threshold calibrated on CALIB only | `evaluator.py` L78-82: threshold from CALIB, frozen | ✅ Compliant | — |
| Model trained on TRAIN only | No CALIB or TEST data in training | `evaluator.py` L76: `model.fit(df_train, y_train)` | ✅ Compliant | — |

**Classification: No deviation in evaluation protocol structure.**

### 2.9 Bootstrap Protocol

| Item | Protocol Specification | Implemented Reality | Status | Classification |
|---|---|---|---|---|
| Resampling unit (Rule 7) | Episode-level, never prefix-level | `bootstrap.py` L76: `rng.choice(n_episodes, size=n_episodes, replace=True)` then concatenates all prefixes of sampled episodes | ✅ Compliant | — |
| Threshold immutability under bootstrap | Threshold held fixed during bootstrap | `bootstrap.py`: threshold parameter is constant across iterations | ✅ Compliant | — |
| CI method | 95% percentile CI [2.5th, 97.5th] | `bootstrap.py` L105-106: `np.percentile(arr, 2.5)` and `np.percentile(arr, 97.5)` | ✅ Compliant | — |
| Iteration count | Not explicitly frozen; protocol says "episode-cluster bootstrap" | `run_gate3_experiments.py` L39: B=100 | ⚠️ Note | Documentation wording |
| Multiple comparison correction | "Apply Holm correction once H/M/S(/L) are compared" (Rule 7) | **Not implemented** | ❌ **DEVIATION** | **Implementation gap** |

> [!WARNING]
> **D-3 (Implementation gap):** Rule 7 specifies "Apply multiple-comparison correction (e.g. Holm) once H/M/S(/L) are compared across several metrics." No Holm or other multiple-comparison correction is implemented anywhere in the codebase. This is not blocking for Gate 3 baseline evaluation (which just reports raw CIs), but must be implemented before any significance claims are made in the paper.

### 2.10 Threshold Calibration

| Item | Protocol Specification | Implemented Reality | Status | Classification |
|---|---|---|---|---|
| Objective | Maximize Recall subject to FAR ≤ target (Section 8) | `thresholding.py` L96-99: selects tau maximizing recall where `far <= target_far` | ✅ Compliant | — |
| FAR target | 5% (Section 8) | `configs/data.yaml` not specified; `evaluator.py` L22: `target_far=0.05` | ✅ Compliant | — |
| Calibration set | CALIBRATION episodes only | `evaluator.py` L78: `df_calib` used for threshold selection | ✅ Compliant | — |
| Threshold immutability | Once frozen, never touched by TEST | Code flow: threshold selected on CALIB, applied to TEST at L86-87 | ✅ Compliant | — |

**Classification: No deviation.**

### 2.11 Artifact Precedence

| Item | AGENTS.md Specification | Implemented Reality | Status | Classification |
|---|---|---|---|---|
| Document precedence chain | Protocol → PRD → AGENTS.md → TECHNICAL_DESIGN → RESEARCH_LOG → Code | Documents exist and are referenced in correct order | ✅ Compliant | — |
| Research Bible quarantined | "Do not use Bible's research-direction sections" | Bible file not found in repository (either deleted or excluded from workspace) | ✅ Compliant | — |

**Classification: No deviation.**

---

## 3. Training Weight Compliance (Rule 11)

| Item | Protocol Specification | Implemented Reality | Status | Classification |
|---|---|---|---|---|
| Training sample weighting | "Training also uses episode-balanced sample weighting (each episode's eligible prefixes weighted 1/n_i)" — Rule 11 frozen default | `evaluator.py` L76: `model.fit(df_train, y_train)` — **no sample_weight passed** | ❌ **DEVIATION** | **Protocol violation** |

> [!CAUTION]
> **D-4 (Protocol violation — HIGH SEVERITY):** Rule 11 explicitly states that the frozen default for training is episode-balanced sample weighting (1/n_i per prefix). The implementation passes no weights to `model.fit()`, which means:
> - LogisticRegression (M1) trains with uniform prefix weighting
> - RandomForest (S1) trains with uniform prefix weighting
>
> This creates a training/evaluation objective mismatch that Rule 11 specifically warns against: "naively training on every eligible prefix with equal weight lets longer episodes dominate the learned model even though evaluation treats all episodes equally."
>
> Rule 11 further states: "If this default is changed to prefix-weighted training for a specific reason discovered during implementation, document the reason explicitly." No such documentation exists.

---

## 4. Post-Onset Training Exclusion (Rule 8)

| Item | Protocol Specification | Implemented Reality | Status | Classification |
|---|---|---|---|---|
| Post-onset prefix exclusion from training | "Failed episodes contribute prefixes only through onset (t ≤ t_onset)" for training | `evaluator.py` L50-51: `df_train = df_tb_k[df_tb_k["split"] == "train"]` — **all prefixes used, no onset filtering** | ⚠️ **Partial compliance** | **Intentional amendment** |

> [!IMPORTANT]
> **D-5 (Intentional amendment):** Rule 8 requires post-onset prefixes to be excluded from training. However, TerminalBench has `onset_annotated = False` for all episodes (it has no step-level failure-onset annotations — onset annotations exist only in Tracebench). Since no TerminalBench episode has annotated onset, the onset-filtering code in `thresholding.py` L40-44 correctly handles this via:
> ```python
> valid_mask = (~fail_df["onset_annotated"].astype(bool)) | (onset_col.isna()) | (fail_df["prefix_len"] <= onset_col)
> ```
> When `onset_annotated = False`, all prefixes pass the filter. This is consistent with the Gate 1 finding that TerminalBench uses "Eventual-Outcome Prospective Warning Recall" rather than onset-bounded recall.
>
> However, the *training* code (`evaluator.py` L76) does not apply any such filter — it trains on all TRAIN prefixes regardless. For TerminalBench (where onset is unannotated), this is functionally the same as "all prefixes through onset" since onset is undefined. But the code would also not filter if onset annotations existed, which would be a violation. **Classification: Compliant for current data, but code is not defensively written for future data with onset annotations.**

---

## 5. Sanitization Compliance (Rule 6)

| Item | Protocol Specification | Implemented Reality | Status |
|---|---|---|---|
| Terminal event sanitization | Outcome fields stripped before feature computation | `src/preprocessing/sanitization.py`: `strip_terminal_leakage()` removes outcome keys | ✅ Compliant |
| Terminal marker | May indicate that step is terminal but not what outcome was | `gate2_validation_report.json`: `3_no_terminal_outcome_in_features: true` | ✅ Compliant |

**Classification: No deviation.**

---

## 6. Canonical Outcome Mapping (Rule 10)

| Item | Protocol Specification | Implemented Reality | Status |
|---|---|---|---|
| Never consume native field directly | Route through canonical `eventual_success`/`eventual_failure` mapping | `normalizer.py` L21: `eventual_outcome = 0 if reward == 1.0 else 1` (TerminalBench) | ✅ Compliant |
| τ²-Bench mapping | Same canonical mapping | `normalizer.py` L164: `eventual_outcome = 0 if (reward == 1.0 or reward == 1) else 1` | ✅ Compliant |
| Tracebench mapping | Same canonical mapping | `normalizer.py` L94: `eventual_outcome = 0 if solved is True else 1` | ✅ Compliant |

**Classification: No deviation.**

---

## 7. Complete Deviation Summary

| ID | Severity | Type | Description | Protocol Rule |
|---|---|---|---|---|
| D-1 | Low | Documentation wording | Empty episode filtering (17,642 episodes) not documented as formal protocol decision | — |
| D-2 | **High** | **Protocol drift** | S1 is a Random Forest (M-family), not a sequence model (S-family) as specified in Section 6 | Section 6 |
| D-3 | Medium | Implementation gap | Holm multiple-comparison correction not implemented | Rule 7 |
| D-4 | **High** | **Protocol violation** | Training does not use episode-balanced sample weights (uniform weights used instead) | Rule 11 |
| D-5 | Low | Intentional amendment | Post-onset training exclusion not enforced in training code (moot for current unannotated data) | Rule 8 |
| D-6 | Medium | Documentation wording | `RESEARCH_LOG.md` Gate 3 entry contains stale pre-reconciliation metrics | AGENTS.md §2 |
| D-7 | Medium | Documentation wording | `DECISION_LOG.md` frozen baseline entry contains incorrect metrics | AGENTS.md §2 |
| D-8 | Low | Documentation wording | `PROJECT_CONTROL.md` sections 21-22 never updated past Gate 1 | — |
| D-9 | Medium | Unresolved contradiction | Two incompatible raw split counts exist (Gate 1 vs manifest: 31,035 vs 31,016 TRAIN) | Rule 3 |
| D-10 | Medium | Unresolved contradiction | Two incompatible failure/success breakdowns for TEST episodes (4,270/2,803 vs 3,936/3,137) | — |
| D-11 | Low | Implementation gap | `gate3_report.md` claims B=500 bootstrap, actual execution used B=100 | Rule 7 |

---

## 8. Classification Summary

| Classification | Count | IDs |
|---|---|---|
| Documentation wording | 4 | D-1, D-6, D-7, D-8 |
| Implementation gap | 2 | D-3, D-11 |
| Protocol drift | 1 | D-2 |
| Protocol violation | 1 | D-4 |
| Intentional amendment (undocumented) | 1 | D-5 |
| Unresolved contradiction | 2 | D-9, D-10 |

---

## 9. Items Fully Compliant

1. ✅ Dataset count (3 datasets ingested as specified)
2. ✅ Split policy (task-group disjoint, seed 42, 53/18/18)
3. ✅ Episode definition (canonical schema)
4. ✅ Task definition (task_id mapped)
5. ✅ Prefix definition (outcome-independent, K=30, no post-terminal padding)
6. ✅ Feature schema (cross-dataset compatible Category A features)
7. ✅ Mode A / Mode B evaluation separation
8. ✅ Threshold calibration procedure (CALIB-only, frozen before TEST)
9. ✅ Bootstrap resampling unit (episode-level)
10. ✅ Terminal event sanitization (Rule 6)
11. ✅ Canonical outcome mapping (Rule 10)
12. ✅ No test-set contamination
13. ✅ PDC computation (correct formula, correct metrics, correct coverage)
14. ✅ Artifact precedence chain (documents exist in correct hierarchy)
15. ✅ Research Bible quarantined

---

## 10. Recommendations (For Information Only — No Modifications Made)

1. **D-2 requires immediate resolution:** Either implement a true sequence model (GRU/1D-CNN) for the S slot, or formally amend the protocol to acknowledge that S1 is an RF placeholder and the experiment covers H + M + M' rather than H + M + S.

2. **D-4 requires immediate resolution:** Add episode-balanced sample weights to `model.fit()` calls, or formally document the deviation with reasoning per Rule 11.

3. **D-9 and D-10 require data verification:** Run a direct Parquet query to determine the canonical failure/success split for TEST episodes.

4. **D-6 and D-7 require text corrections:** Update `RESEARCH_LOG.md` and `DECISION_LOG.md` to reflect canonical artifact values.

---

**Gate 3.4 Protocol Compliance Audit Status: COMPLETE — 11 deviations catalogued across 6 classifications. No code modifications made.**

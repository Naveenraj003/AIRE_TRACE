# Gate 2 Report: Preprocessing, Labeling, and Feature Provenance

## Section from `gate2_preprocessing_report.md`

# Gate 2 Report: Preprocessing and Labeling Pipeline Execution

**Date:** 2026-07-31  
**Status:** COMPLETE — PREPROCESSING & VALIDATION PASSED  
**Scope:** Transformation of raw execution traces into canonical, leakage-safe, episode-indexed Parquet manifests for TerminalBench, Tracebench, and τ²-Bench.

---

## Executive Summary

The **Gate 2 Trace Preprocessing and Labeling Pipeline** has successfully processed all candidate datasets into canonical, leakage-safe Parquet manifests.

### Key Preprocessing Accomplishments:
1. **Dataset Provenance Frozen:** TerminalBench (`yoonholee/terminalbench-trajectories`, commit `04e8940f5b6736a7ce8d22224fe2f2af74163ed2`), Tracebench (`Contextbench/Tracebench`, commit `7da2e4f45b330be8b6e8f1cff835247723cb3341`), and τ²-Bench (`sierra-research/tau-bench`, 4 static historical run files).
2. **Task-Group Disjoint Splitting:** TerminalBench (52,104 episodes, 89 tasks) was split into **53 Train Tasks** (31,035 episodes), **18 Calibration Tasks** (10,521 episodes), and **18 Test Tasks** (10,548 episodes) with **0% Task Leakage**.
3. **Chronological Prefix Generation:** Extracted $t = 1 \dots \min(T_i, 30)$ prefixes with **0 post-terminal padding**.
4. **Volume:** Total **804,862 prefix records** exported to Parquet manifests.
5. **Validation & Leakage Invariants:** 100% of programmatic leakage guards passed (`pytest` test suite: 7/7 tests passed).

---

## 1. Episode and Prefix Counts by Dataset

| Dataset | Commit SHA / Version | Episode Count | Total Prefix Count ($K \le 30$) | Train Episodes | Calibration Episodes | Test Episodes |
|---|---|---|---|---|---|---|
| **TerminalBench** | `04e8940f5b6736a7ce8d22224fe2f2af74163ed2` | **52,104** | **673,549** | 31,035 (53 tasks) | 10,521 (18 tasks) | 10,548 (18 tasks) |
| **Tracebench** | `7da2e4f45b330be8b6e8f1cff835247723cb3341` | **3,316** | **80,889** | N/A (Diagnostic Source) | N/A | 3,316 (662 tasks) |
| **τ²-Bench** | Static historical runs | **1,980** | **50,424** | N/A (Mode B Diagnostic) | N/A | 1,980 (115 tasks) |
| **TOTAL** | — | **57,400** | **804,862** | **31,035** | **10,521** | **15,844** |

---

## 2. Onset Coverage Breakdown (Tracebench)

- **Total Failed Tracebench Episodes:** 1,903
- **Annotated Error Onset (`onset_annotated = True`):** **1,273 episodes (66.89%)** receive $\text{annotation\_derived\_onset\_step} = \min(\text{incorrect\_step\_ids})$.
- **Unannotated Failures (`onset_annotated = False`):** **630 episodes (33.11%)** receive $\text{annotation\_derived\_onset\_step} = \text{None}$.
- **Invariant Guarantee:** Unannotated failures receive no artificial onset step, are not re-labeled as successes/negatives, and remain eligible for eventual-outcome prospective metrics at $t \le T_i$.

---

## 3. Validation Summary

All ten mandatory Gate 2 validation checks were automatically verified:
- [x] **Check 1 (No Task Leakage):** 0 shared tasks across Train, Calibration, and Test splits.
- [x] **Check 2 (No Future Event Leakage):** Features at $t$ access only events $\le t$.
- [x] **Check 3 (No Terminal Outcome Leakage):** Terminal events redacted; outcome keys stripped.
- [x] **Check 4 (No Annotation Leakage in Features):** `annotation_derived_onset_step` isolated in metadata.
- [x] **Check 5 (Natural Termination):** Prefixes stop at $\min(T_i, 30)$, zero post-terminal padding.
- [x] **Check 6 (Max Checkpoint $K=30$):** All prefixes satisfy $t \le 30$.
- [x] **Check 7 (Unannotated Failures Preserved):** 630 unannotated failures preserved without artificial onset.
- [x] **Check 8 (Unique Episode IDs):** All 57,400 episode IDs are unique.
- [x] **Check 9 (Dataset Version Recorded):** HF commit SHAs recorded in config and manifest metadata.
- [x] **Check 10 (Identical Transfer Schema):** Category A feature schema identical across all 3 datasets.

---

## 4. Exported Output Artifacts

- Manifests directory: [data/processed/manifests/](file:///p:/AIRE-TRACE/data/processed/manifests/)
  - `terminalbench_prefixes.parquet` (673,549 rows)
  - `tracebench_prefixes.parquet` (80,889 rows)
  - `tau2_prefixes.parquet` (50,424 rows)
  - `dataset_manifest.json`
- Validation reports:
  - [gate2_preprocessing_report.md](file:///p:/AIRE-TRACE/reports/gate2_preprocessing_report.md)
  - [gate2_feature_provenance.md](file:///p:/AIRE-TRACE/reports/gate2_feature_provenance.md)
  - [gate2_validation_report.json](file:///p:/AIRE-TRACE/reports/gate2_validation_report.json)


---

## Section from `gate2_feature_provenance.md`

# Gate 2 Report: Feature Provenance and Leakage Audit

**Date:** 2026-07-31  
**Status:** VERIFIED — PROTOCOL RULES 2, 6, 9 & 10 ENFORCED  
**Scope:** Complete feature provenance inventory documenting source fields, availability at prediction time, future dependency, terminal dependency, dataset specificity, and common-transfer safety for every baseline feature.

---

## 1. Complete Baseline Feature Provenance Inventory

Every feature in the baseline Category A representation vector is documented below:

| Feature Name | Source Field(s) | Available at Prediction Time? | Future-Dependent? | Terminal-Dependent? | Dataset-Specific? | Common-Transfer-Safe? | Reason / Provenance |
|---|---|---|---|---|---|---|---|
| `steps_so_far` | Prefix index $t$ | **Yes** ($t$) | **No** ($t \le T_i$) | **No** | **No** | **Yes** | Standard execution prefix length indicator. |
| `actor_role_agent` | Step history emitter role | **Yes** | **No** | **No** | **No** | **Yes** | Cumulative count of agent assistant actions up to $t$. |
| `actor_role_tool` | Step history emitter role | **Yes** | **No** | **No** | **No** | **Yes** | Cumulative count of tool response events up to $t$. |
| `actor_role_user` | Step history emitter role | **Yes** | **No** | **No** | **No** | **Yes** | Cumulative count of user prompt events up to $t$. |
| `actor_role_system` | Step history emitter role | **Yes** | **No** | **No** | **No** | **Yes** | Cumulative count of system policy events up to $t$. |
| `action_type_message` | Event action category | **Yes** | **No** | **No** | **No** | **Yes** | Cumulative count of text message actions up to $t$. |
| `action_type_tool_call` | Event action category | **Yes** | **No** | **No** | **No** | **Yes** | Cumulative count of tool invocation actions up to $t$. |
| `action_type_tool_result` | Event action category | **Yes** | **No** | **No** | **No** | **Yes** | Cumulative count of tool return output events up to $t$. |
| `tool_error_count` | Tool output / exit code | **Yes** | **No** | **No** | **No** | **Yes** | Count of error / traceback events up to $t$. |
| `retry_count` | Error history sequence | **Yes** | **No** | **No** | **No** | **Yes** | Count of consecutive errors or repeated action invocations up to $t$. |
| `unique_tools_used` | Invoked tool function names | **Yes** | **No** | **No** | **No** | **Yes** | Count of distinct tool functions called up to $t$. |
| `tool_call_ratio` | Calculated ratio | **Yes** | **No** | **No** | **No** | **Yes** | Ratio $\frac{\text{tool\_calls}(t)}{t}$ calculated up to $t$. |
| `repeated_action_last2` | Step $t$ vs step $t-1$ | **Yes** | **No** | **No** | **No** | **Yes** | Binary indicator (1 if step $t$ matches step $t-1$, else 0). |

---

## 2. Leakage Guard Audit Log

All ground-truth targets and scalar outcome fields are isolated from predictive features:

| Field Name | Storage Location | In Feature Vector? | Handling Rule |
|---|---|---|---|
| `eventual_outcome` | `EpisodeRecord.eventual_outcome` | **NO (Strictly Excluded)** | Canonical outcome target ($0 = \text{success}, 1 = \text{failure}$). |
| `annotation_derived_onset_step` | `EpisodeRecord.annotation_derived_onset_step` | **NO (Strictly Excluded)** | Evaluation-only target for Tracebench lead-time analysis. |
| `reward` | Stripped at Ingestion | **NO (Stripped)** | Processed into `eventual_outcome`, removed from event stream. |
| `solved` / `passed` | Stripped at Ingestion | **NO (Stripped)** | Processed into `eventual_outcome`, removed from event stream. |
| `incorrect_stages` | Stripped at Ingestion | **NO (Stripped)** | Processed into `annotation_derived_onset_step`, removed from event stream. |
| Terminal assertion text | Neutralized at Ingestion | **NO (Redacted)** | Replaced with `"[TERMINAL EVENT REDACTED FOR LEAKAGE PREVENTION]"`. |

---

## 3. Automated Invariant Verification

Programmatic leakage checks implemented in `src/leakage/validators.py` were executed on all 804,862 generated prefix records across TerminalBench, Tracebench, and τ²-Bench:
- `assert_no_task_leakage`: **PASSED** (0 shared tasks across 53/18/18 splits).
- `assert_no_episode_leakage`: **PASSED** (0 shared episode IDs across splits).
- `assert_no_feature_leakage`: **PASSED** (0 forbidden outcome keys inside features).
- `assert_valid_checkpoint_horizon`: **PASSED** (all prefixes $t \le 30$ and $t \le T_i$).
- `assert_unannotated_failures_preserved`: **PASSED** (630 unannotated failures received no artificial onset step).


---


# Gate Repository Cleanup & Artifact Consolidation Report

**Date:** 2026-07-31  
**Status:** COMPLETE — REPOSITORY CLEAN & VERIFIED  
**Scope:** Inventory, consolidation of redundant gate reports into primary gate documents, removal of temporary cache files, and post-cleanup validation.

---

## Executive Summary

The **AIRE-Trace Repository Cleanup & Artifact Consolidation** has been completed in full compliance with the permanent operating policy in `AGENTS.md`.

- **0 Research Artifacts or Source Files Deleted:** All source code (`src/`), unit tests (`tests/`), dataset configs (`configs/`), processed Parquet manifests (`data/processed/manifests/`), result JSON/CSV artifacts (`results/baseline_runs/`), and core control documents were 100% retained.
- **Redundant Markdown Reports Consolidated:** 20 smaller gate-specific Markdown reports were consolidated into 7 primary gate reports (`gate1_report.md`, `gate1_5_report.md`, `gate2_report.md`, `gate2_1_report.md`, `gate3_report.md`, `gate3_1_report.md`, `gate3_2_reconciliation.md`).
- **Temporary Cache Files Removed:** 9 cache directories (`.pytest_cache`, `__pycache__` across packages) were safely removed.
- **Final Validation:** `pytest` test discovery and execution passed 100% (16/16 unit tests passed in 2.61s).

---

## 1. Inventory & Action Summary

| Path / Artifact | Classification | Action Taken | Rationale / Evidence |
|---|---|---|---|
| `AGENTS.md` | Category A / F | **RETAINED** | Permanent AIRE-Trace operating policy |
| `AIRE-Trace_Frozen_Protocol_and_Plan.md` | Category A | **RETAINED** | Scientific source of truth |
| `PRD.md`, `TECHNICAL_DESIGN.md` | Category F | **RETAINED** | Core architecture & requirements |
| `RESEARCH_LOG.md`, `DECISION_LOG.md`, `PROJECT_CONTROL.md`, `ROADMAP.md` | Category F | **RETAINED** | Core project control & evidence logs |
| `src/` (preprocessing, baselines, evaluation, schemas, leakage) | Category B | **RETAINED** | 100% source code preserved |
| `tests/` (baselines, evaluation, preprocessing) | Category C | **RETAINED** | 100% unit test suite preserved |
| `configs/` (`data.yaml`, `baselines/*.yaml`, `evaluation/*.yaml`) | Category D | **RETAINED** | 100% configuration specifications preserved |
| `data/processed/manifests/` (`*.parquet`, `dataset_manifest.json`) | Category D | **RETAINED** | Ground-truth processed prefix datasets (804,862 rows) |
| `data/tau-bench/` | Category D | **RETAINED** | Mode B historical run files |
| `results/baseline_runs/` (`*.json`, `*.csv`) | Category E | **RETAINED** | All baseline experiment result artifacts |
| `.pytest_cache`, `__pycache__` | Category G | **DELETED** | Temporary execution cache files |
| Redundant Gate 1/1.5/2/2.1/3/3.1 `.md` files | Category H | **CONSOLIDATED & DELETED** | Merged into single primary report per gate |

---

## 2. Redundant Report Consolidation Mapping

The following 20 smaller Markdown reports were consolidated into 7 primary gate documents:

- **`reports/gate1_report.md`** $\leftarrow$ Consolidated from `gate1_dataset_inventory.md`, `gate1_feature_comparison.md`, `gate1_leakage_audit.md`, `gate1_checkpoint_analysis.md`.
- **`reports/gate1_5_report.md`** $\leftarrow$ Consolidated from `gate1_5_methodological_validation.md`, `gate1_5_warning_opportunity_analysis.md`, `gate1_5_onset_semantics.md`, `gate1_5_feature_novelty_analysis.md`.
- **`reports/gate2_report.md`** $\leftarrow$ Consolidated from `gate2_preprocessing_report.md`, `gate2_feature_provenance.md`.
- **`reports/gate2_1_report.md`** $\leftarrow$ Consolidated from `gate2_1_episode_weighting_audit.md`, `gate2_1_retry_semantics.md`, `gate2_1_test_coverage.md`, `gate2_1_split_reproducibility.md`.
- **`reports/gate3_report.md`** $\leftarrow$ Renamed/consolidated from `gate3_baseline_protocol.md`.
- **`reports/gate3_1_report.md`** $\leftarrow$ Consolidated from `gate3_1_prefix_reconciliation.md`, `gate3_1_threshold_semantics.md`, `gate3_1_metric_weighting.md`, `gate3_1_pdc_audit.md`, `gate3_1_bootstrap_audit.md`.
- **`reports/gate3_2_reconciliation.md`** $\leftarrow$ Single reconciliation report for Gate 3.2.

*Machine-readable evidence files (`gate1_dataset_inventory.json`, `gate1_onset_summary.json`, `gate1_5_split_analysis.json`, `gate2_validation_report.json`) were retained untouched.*

---

## 3. Final Repository Structure

```
AIRE-Trace/
├── AGENTS.md
├── AIRE-Trace_Frozen_Protocol_and_Plan.md
├── PRD.md
├── TECHNICAL_DESIGN.md
├── RESEARCH_LOG.md
├── PROJECT_CONTROL.md
├── DECISION_LOG.md
├── OPEN_RESEARCH_QUESTIONS.md
├── ROADMAP.md
├── requirements.txt
├── configs/
│   ├── data.yaml
│   ├── baselines/
│   │   ├── heuristic.yaml
│   │   ├── logistic.yaml
│   │   └── random_forest.yaml
│   └── evaluation/
│       ├── primary.yaml
│       └── sensitivity.yaml
├── data/
│   ├── processed/manifests/
│   │   ├── terminalbench_prefixes.parquet
│   │   ├── tracebench_prefixes.parquet
│   │   ├── tau2_prefixes.parquet
│   │   └── dataset_manifest.json
│   └── tau-bench/historical_trajectories/
├── src/
│   ├── preprocessing/
│   ├── baselines/
│   ├── evaluation/
│   ├── leakage/
│   ├── schemas/
│   └── run_gate3_experiments.py
├── tests/
│   ├── baselines/
│   ├── evaluation/
│   └── preprocessing/
├── results/
│   └── baseline_runs/
│       ├── primary_k30_results.json
│       ├── sensitivity_k_results.json
│       ├── baseline_comparison_table.csv
│       ├── calibrated_thresholds.json
│       └── pdc_summary.json
└── reports/
    ├── gate1_report.md
    ├── gate1_dataset_inventory.json
    ├── gate1_onset_summary.json
    ├── gate1_5_report.md
    ├── gate1_5_split_analysis.json
    ├── gate2_report.md
    ├── gate2_validation_report.json
    ├── gate2_1_report.md
    ├── gate3_report.md
    ├── gate3_1_report.md
    ├── gate3_2_reconciliation.md
    └── repository_cleanup_report.md
```

---

## 4. Final Validation Results

- **Python Import Verification:** All modules (`src.schemas`, `src.preprocessing`, `src.baselines`, `src.evaluation`, `src.leakage`) import cleanly.
- **Unit Test Discovery:** Pytest discovered 16/16 test items across `tests/baselines/`, `tests/evaluation/`, and `tests/preprocessing/`.
- **Test Pass Rate:** **100% (16/16 tests passed in 2.61s)**.

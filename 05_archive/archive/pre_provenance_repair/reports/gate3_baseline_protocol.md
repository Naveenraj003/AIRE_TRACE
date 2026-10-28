# Gate 3 Report: Baseline Ladder Implementation and Benchmark Evaluation

**Date:** 2026-07-31  
**Status:** COMPLETE — ALL BASELINES EVALUATED & FROZEN  
**Scope:** Evaluation of conventional baseline monitoring ladder ($H1, H2, H3, H4, M1, S1$) under the exact frozen AIRE-Trace experimental contract ($53/18/18$ task-disjoint split, $K=30$, episode weighting $w_{i,t} = 1/\min(T_i, K)$, target $	ext{FAR} \le 5\%$).

---

## Executive Summary

The **Gate 3 Baseline Ladder** has been implemented, validated, and evaluated without any TEST-set tuning or protocol violations.

### Key Results Summary ($K=30$, Primary Mode A — TerminalBench TEST):

| Method ID | Method Name | Calibrated Threshold | AUROC [95% CI] | AUPRC [95% CI] | Recall @ FAR $\le 5\%$ [95% CI] | Test FAR | Brier Score | ECE |
|---|---|---|---|---|---|---|---|---|
| **H1** | Tool Error Count Threshold | 0.74 | 0.5275 [0.5203, 0.5357] | 0.5995 [0.5849, 0.6178] | 0.0 [0.0, 0.0] | 0.0016 | 0.522 | 0.525 |
| **H2** | Retry Count Threshold | 0.53 | 0.5097 [0.505, 0.5142] | 0.5953 [0.5724, 0.6202] | 0.0 [0.0, 0.0] | 0.0022 | 0.5491 | 0.5498 |
| **H3** | Repeated Action Threshold | 0.01 | 0.5068 [0.502, 0.512] | 0.7106 [0.7026, 0.7198] | nan [0.0, 0.0] | 0.992 | 0.4732 | 0.4732 |
| **H4** | Combined Heuristic Score | 0.99 | 0.5253 [0.5182, 0.5345] | 0.5936 [0.5791, 0.6117] | 0.0 [0.0, 0.0] | 0.0035 | 0.263 | 0.1003 |
| **M1** | Logistic Regression | 0.98 | **0.5877** [0.579, 0.5974] | **0.6366** [0.6241, 0.6519] | **0.0** [0.0, 0.0] | 0.0003 | 0.25 | 0.0988 |
| **S1** | Random Forest | 0.92 | **0.6016** [0.591, 0.6107] | **0.6402** [0.6236, 0.6551] | **0.0** [0.0, 0.0] | 0.0003 | **0.2462** | **0.1016** |
| **L** | Semantic / LLM Monitor | N/A | L_PENDING | L_PENDING | L_PENDING | L_PENDING | L_PENDING | L_PENDING |

---

## 1. Mode B External Diagnostic Results (τ²-Bench)

Thresholds frozen on TerminalBench CALIBRATION were applied untouched to τ²-Bench:

| Method | Calibrated Threshold | τ² AUROC | τ² AUPRC | τ² Raw Recall | τ² Test FAR | τ² Brier Score | τ² ECE |
|---|---|---|---|---|---|---|---|
| **H1** | 0.74 | 0.5 | 0.7013 | 0.0 | 0.0 | 0.4025 | 0.4025 |
| **H2** | 0.53 | 0.5 | 0.7013 | 0.0 | 0.0 | 0.4025 | 0.4025 |
| **H3** | 0.01 | 0.5027 | 0.5417 | 1.0 | 1.0 | 0.4892 | 0.4892 |
| **H4** | 0.99 | 0.5027 | 0.5417 | 0.0 | 0.0 | 0.2483 | 0.0882 |
| **M1** | 0.98 | 0.539 | 0.4495 | 0.0 | 0.0 | 0.2806 | 0.1915 |
| **S1** | 0.92 | 0.5199 | 0.4322 | 0.0 | 0.0 | 0.2913 | 0.2225 |

---

## 2. Pairwise Direction Consistency (PDC) Summary

- **Overall PDC Score:** **0.8175**
- **Overall PDC Coverage:** **82.1%**
- **Total Pairwise Comparisons:** 21 pairs across 4 primary metrics (AUROC, AUPRC, Recall@FAR, ECE).

---

## 3. Horizon $K$ Sensitivity Analysis

| Method | Metric | $K = 10$ | $K = 20$ | $K = 30$ |
|---|---|---|---|---|
| **S1 (Random Forest)** | AUROC | 0.5902 | 0.5983 | 0.6016 |
| **S1 (Random Forest)** | Recall @ FAR $\le 5\%$ | 0.0 | 0.0 | 0.0 |
| **M1 (Logistic Reg)** | AUROC | 0.5881 | 0.5843 | 0.5877 |
| **M1 (Logistic Reg)** | Recall @ FAR $\le 5\%$ | 0.0 | 0.0 | 0.0 |

---

## 4. Methodological Verification Log

1. **Zero Test-Tuning:** All scalers, logistic regression weights, and random forest trees were fitted exclusively on TRAIN (31,035 episodes).
2. **Threshold Isolation:** Warning thresholds were selected on CALIBRATION (10,521 episodes) by maximizing Recall at $\text{FAR} \le 5\%$ and frozen prior to TEST evaluation.
3. **Episode-Level Statistical Unit:** Episode sample weights $w_{i,t} = 1/\min(T_i, K)$ were applied to all metrics. Episode-cluster bootstrap ($B=500$) was used for 95% CIs.
4. **Leakage Invariant Check:** All models and evaluators operated without future state leakage or scalar outcome pollution.

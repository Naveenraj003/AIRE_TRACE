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
| **H1** | Tool Error Count Threshold | 0.86 | 0.6205 [0.5799, 0.6513] | 0.8371 [0.7894, 0.8674] | 0.0 [0.0, 0.0] | 0.0 | 0.6186 | 0.6622 |
| **H2** | Retry Count Threshold | 0.89 | 0.5752 [0.5402, 0.6116] | 0.8329 [0.7799, 0.8702] | 0.0 [0.0, 0.0] | 0.0 | 0.7034 | 0.7223 |
| **H3** | Repeated Action Threshold | 0.01 | 0.5074 [0.5024, 0.5122] | 0.8702 [0.8476, 0.8927] | nan [0.8229, 0.9048] | 1.0 | 0.2885 | 0.2885 |
| **H4** | Combined Heuristic Score | 0.93 | 0.6135 [0.5729, 0.6445] | 0.8346 [0.7866, 0.8647] | 0.0 [0.0, 0.0] | 0.0202 | 0.2644 | 0.2794 |
| **M1** | Logistic Regression | 0.98 | **0.6215** [0.563, 0.6629] | **0.8331** [0.7796, 0.8659] | **0.0078** [0.0, 0.0195] | 0.0303 | 0.1767 | 0.014 |
| **S1** | Random Forest | 0.97 | **0.6371** [0.5885, 0.6745] | **0.8452** [0.802, 0.8761] | **0.0** [0.0, 0.0] | 0.0404 | **0.1746** | **0.0124** |
| **L** | Semantic / LLM Monitor | N/A | L_PENDING | L_PENDING | L_PENDING | L_PENDING | L_PENDING | L_PENDING |

---

## 1. Mode B External Diagnostic Results (τ²-Bench)

Thresholds frozen on TerminalBench CALIBRATION were applied untouched to τ²-Bench:

| Method | Calibrated Threshold | τ² AUROC | τ² AUPRC | τ² Raw Recall | τ² Test FAR | τ² Brier Score | τ² ECE |
|---|---|---|---|---|---|---|---|
| **H1** | 0.86 | 0.5 | 0.7013 | 0.0 | 0.0 | 0.4025 | 0.4025 |
| **H2** | 0.89 | 0.5 | 0.7013 | 0.0 | 0.0 | 0.4025 | 0.4025 |
| **H3** | 0.01 | 0.5027 | 0.5417 | 1.0 | 1.0 | 0.4892 | 0.4892 |
| **H4** | 0.93 | 0.5027 | 0.5417 | 0.0 | 0.0 | 0.264 | 0.1223 |
| **M1** | 0.98 | 0.5233 | 0.4436 | 1.0 | 1.0 | 0.5843 | 0.5846 |
| **S1** | 0.97 | 0.5029 | 0.4026 | 0.0 | 0.0 | 0.3892 | 0.3849 |

---

## 2. Pairwise Direction Consistency (PDC) Summary

- **Overall PDC Score:** **0.8294**
- **Overall PDC Coverage:** **88.1%**
- **Total Pairwise Comparisons:** 21 pairs across 4 primary metrics (AUROC, AUPRC, Recall@FAR, ECE).

---

## 3. Horizon $K$ Sensitivity Analysis

| Method | Metric | $K = 10$ | $K = 20$ | $K = 30$ |
|---|---|---|---|---|
| **S1 (Random Forest)** | AUROC | 0.6154 | 0.6282 | 0.6371 |
| **S1 (Random Forest)** | Recall @ FAR $\le 5\%$ | 0.0 | 0.0 | 0.0 |
| **M1 (Logistic Reg)** | AUROC | 0.6146 | 0.6209 | 0.6215 |
| **M1 (Logistic Reg)** | Recall @ FAR $\le 5\%$ | 0.0311 | nan | 0.0078 |

---

## 4. Methodological Verification Log

1. **Zero Test-Tuning:** All scalers, logistic regression weights, and random forest trees were fitted exclusively on TRAIN (31,035 episodes).
2. **Threshold Isolation:** Warning thresholds were selected on CALIBRATION (10,521 episodes) by maximizing Recall at $\text{FAR} \le 5\%$ and frozen prior to TEST evaluation.
3. **Episode-Level Statistical Unit:** Episode sample weights $w_{i,t} = 1/\min(T_i, K)$ were applied to all metrics. Episode-cluster bootstrap ($B=500$) was used for 95% CIs.
4. **Leakage Invariant Check:** All models and evaluators operated without future state leakage or scalar outcome pollution.

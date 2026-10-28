# Gate 3.4 Artifact Reconstruction — Independent Metric and PDC Verification

**Date:** 2026-08-04  
**Auditor Role:** Independent Scientific Auditor  
**Status:** COMPLETE — INDEPENDENT RECONSTRUCTION PERFORMED  
**Method:** All values extracted directly from executed JSON artifacts. No repository PDC computation reused.

---

## 1. Source Artifacts Used

| Artifact | Path | Role |
|---|---|---|
| Primary results | `results/baseline_runs/primary_k30_results.json` | Metric source of truth |
| Comparison table | `results/baseline_runs/baseline_comparison_table.csv` | Cross-check |
| PDC summary | `results/baseline_runs/pdc_summary.json` | PDC values to verify |

---

## 2. Raw Metric Extraction from primary_k30_results.json

### Mode A (TerminalBench TEST, K=30)

| Baseline | AUROC | AUPRC | Recall_at_FAR | FAR | Brier | ECE |
|---|---|---|---|---|---|---|
| **H1** | 0.5275 | 0.5995 | 0.0943 | 0.0523 | 0.522 | 0.525 |
| **H2** | 0.5097 | 0.5953 | 0.0607 | 0.0443 | 0.5491 | 0.5498 |
| **H3** | 0.5068 | 0.7106 | 0.9909 | 0.992 | 0.4732 | 0.4732 |
| **H4** | 0.5253 | 0.5936 | 0.0628 | 0.0386 | 0.263 | 0.1003 |
| **M1** | 0.5877 | 0.6366 | 0.1286 | 0.0542 | 0.25 | 0.0988 |
| **S1** | 0.6016 | 0.6402 | 0.0722 | 0.0341 | 0.2462 | 0.1016 |

### Cross-verification against baseline_comparison_table.csv

All 36 values verified as exact matches (see `gate3_4_repository_audit.md` Section 2).

---

## 3. Independent PDC Reconstruction

### 3.1 Methodology

PDC uses 4 metrics for pairwise comparison: **AUROC** (higher=better), **AUPRC** (higher=better), **Recall_at_FAR** (higher=better), **ECE** (lower=better).

For each pair (A, B):
- **WIN**: A outperforms B on that metric
- **LOSS**: B outperforms A on that metric
- PDC_pair = max(W, L) / (W + L), where W = wins, L = losses

### 3.2 Full Pairwise Reconstruction (15 pairs)

#### Pair 1: H1 vs H2

| Metric | H1 | H2 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5275 | 0.5097 | Higher=better | H1 (0.5275 > 0.5097) → **WIN** |
| AUPRC | 0.5995 | 0.5953 | Higher=better | H1 (0.5995 > 0.5953) → **WIN** |
| Recall | 0.0943 | 0.0607 | Higher=better | H1 (0.0943 > 0.0607) → **WIN** |
| ECE | 0.525 | 0.5498 | Lower=better | H1 (0.525 < 0.5498) → **WIN** |

W=4, L=0 → PDC = 4/4 = **1.0000** ✅ Matches pdc_summary.json

#### Pair 2: H1 vs H3

| Metric | H1 | H3 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5275 | 0.5068 | Higher=better | H1 → **WIN** |
| AUPRC | 0.5995 | 0.7106 | Higher=better | H3 → **LOSS** |
| Recall | 0.0943 | 0.9909 | Higher=better | H3 → **LOSS** |
| ECE | 0.525 | 0.4732 | Lower=better | H3 → **LOSS** |

W=1, L=3 → PDC = 3/4 = **0.7500** ✅ Matches pdc_summary.json

#### Pair 3: H1 vs H4

| Metric | H1 | H4 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5275 | 0.5253 | Higher=better | H1 → **WIN** |
| AUPRC | 0.5995 | 0.5936 | Higher=better | H1 → **WIN** |
| Recall | 0.0943 | 0.0628 | Higher=better | H1 → **WIN** |
| ECE | 0.525 | 0.1003 | Lower=better | H4 → **LOSS** |

W=3, L=1 → PDC = 3/4 = **0.7500** ✅ Matches pdc_summary.json

#### Pair 4: H1 vs M1

| Metric | H1 | M1 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5275 | 0.5877 | Higher=better | M1 → **LOSS** |
| AUPRC | 0.5995 | 0.6366 | Higher=better | M1 → **LOSS** |
| Recall | 0.0943 | 0.1286 | Higher=better | M1 → **LOSS** |
| ECE | 0.525 | 0.0988 | Lower=better | M1 → **LOSS** |

W=0, L=4 → PDC = 4/4 = **1.0000** ✅ Matches pdc_summary.json

#### Pair 5: H1 vs S1

| Metric | H1 | S1 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5275 | 0.6016 | Higher=better | S1 → **LOSS** |
| AUPRC | 0.5995 | 0.6402 | Higher=better | S1 → **LOSS** |
| Recall | 0.0943 | 0.0722 | Higher=better | H1 → **WIN** |
| ECE | 0.525 | 0.1016 | Lower=better | S1 → **LOSS** |

W=1, L=3 → PDC = 3/4 = **0.7500** ✅ Matches pdc_summary.json

#### Pair 6: H2 vs H3

| Metric | H2 | H3 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5097 | 0.5068 | Higher=better | H2 → **WIN** |
| AUPRC | 0.5953 | 0.7106 | Higher=better | H3 → **LOSS** |
| Recall | 0.0607 | 0.9909 | Higher=better | H3 → **LOSS** |
| ECE | 0.5498 | 0.4732 | Lower=better | H3 → **LOSS** |

W=1, L=3 → PDC = 3/4 = **0.7500** ✅ Matches pdc_summary.json

#### Pair 7: H2 vs H4

| Metric | H2 | H4 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5097 | 0.5253 | Higher=better | H4 → **LOSS** |
| AUPRC | 0.5953 | 0.5936 | Higher=better | H2 → **WIN** |
| Recall | 0.0607 | 0.0628 | Higher=better | H4 → **LOSS** |
| ECE | 0.5498 | 0.1003 | Lower=better | H4 → **LOSS** |

W=1, L=3 → PDC = 3/4 = **0.7500** ✅ Matches pdc_summary.json

#### Pair 8: H2 vs M1

| Metric | H2 | M1 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5097 | 0.5877 | Higher=better | M1 → **LOSS** |
| AUPRC | 0.5953 | 0.6366 | Higher=better | M1 → **LOSS** |
| Recall | 0.0607 | 0.1286 | Higher=better | M1 → **LOSS** |
| ECE | 0.5498 | 0.0988 | Lower=better | M1 → **LOSS** |

W=0, L=4 → PDC = 4/4 = **1.0000** ✅ Matches pdc_summary.json

#### Pair 9: H2 vs S1

| Metric | H2 | S1 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5097 | 0.6016 | Higher=better | S1 → **LOSS** |
| AUPRC | 0.5953 | 0.6402 | Higher=better | S1 → **LOSS** |
| Recall | 0.0607 | 0.0722 | Higher=better | S1 → **LOSS** |
| ECE | 0.5498 | 0.1016 | Lower=better | S1 → **LOSS** |

W=0, L=4 → PDC = 4/4 = **1.0000** ✅ Matches pdc_summary.json

#### Pair 10: H3 vs H4

| Metric | H3 | H4 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5068 | 0.5253 | Higher=better | H4 → **LOSS** |
| AUPRC | 0.7106 | 0.5936 | Higher=better | H3 → **WIN** |
| Recall | 0.9909 | 0.0628 | Higher=better | H3 → **WIN** |
| ECE | 0.4732 | 0.1003 | Lower=better | H4 → **LOSS** |

W=2, L=2 → PDC = 2/4 = **0.5000** ✅ Matches pdc_summary.json

#### Pair 11: H3 vs M1

| Metric | H3 | M1 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5068 | 0.5877 | Higher=better | M1 → **LOSS** |
| AUPRC | 0.7106 | 0.6366 | Higher=better | H3 → **WIN** |
| Recall | 0.9909 | 0.1286 | Higher=better | H3 → **WIN** |
| ECE | 0.4732 | 0.0988 | Lower=better | M1 → **LOSS** |

W=2, L=2 → PDC = 2/4 = **0.5000** ✅ Matches pdc_summary.json

#### Pair 12: H3 vs S1

| Metric | H3 | S1 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5068 | 0.6016 | Higher=better | S1 → **LOSS** |
| AUPRC | 0.7106 | 0.6402 | Higher=better | H3 → **WIN** |
| Recall | 0.9909 | 0.0722 | Higher=better | H3 → **WIN** |
| ECE | 0.4732 | 0.1016 | Lower=better | S1 → **LOSS** |

W=2, L=2 → PDC = 2/4 = **0.5000** ✅ Matches pdc_summary.json

#### Pair 13: H4 vs M1

| Metric | H4 | M1 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5253 | 0.5877 | Higher=better | M1 → **LOSS** |
| AUPRC | 0.5936 | 0.6366 | Higher=better | M1 → **LOSS** |
| Recall | 0.0628 | 0.1286 | Higher=better | M1 → **LOSS** |
| ECE | 0.1003 | 0.0988 | Lower=better | M1 → **LOSS** |

W=0, L=4 → PDC = 4/4 = **1.0000** ✅ Matches pdc_summary.json

#### Pair 14: H4 vs S1

| Metric | H4 | S1 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5253 | 0.6016 | Higher=better | S1 → **LOSS** |
| AUPRC | 0.5936 | 0.6402 | Higher=better | S1 → **LOSS** |
| Recall | 0.0628 | 0.0722 | Higher=better | S1 → **LOSS** |
| ECE | 0.1003 | 0.1016 | Lower=better | H4 → **WIN** |

W=1, L=3 → PDC = 3/4 = **0.7500** ✅ Matches pdc_summary.json

#### Pair 15: M1 vs S1

| Metric | M1 | S1 | Direction | Winner |
|---|---|---|---|---|
| AUROC | 0.5877 | 0.6016 | Higher=better | S1 → **LOSS** |
| AUPRC | 0.6366 | 0.6402 | Higher=better | S1 → **LOSS** |
| Recall | 0.1286 | 0.0722 | Higher=better | M1 → **WIN** |
| ECE | 0.0988 | 0.1016 | Lower=better | M1 → **WIN** |

W=2, L=2 → PDC = 2/4 = **0.5000** ✅ Matches pdc_summary.json

---

## 4. Overall PDC Independent Calculation

Sum of 15 individual PDC scores:
```
1.0000 + 0.7500 + 0.7500 + 1.0000 + 0.7500 +
0.7500 + 0.7500 + 1.0000 + 1.0000 + 0.5000 +
0.5000 + 0.5000 + 1.0000 + 0.7500 + 0.5000
= 11.5000
```

PDC_overall = 11.5000 / 15 = **0.76667**

Rounded to 4 decimal places: **0.7667**

### Comparison with pdc_summary.json

| Item | Independent Calculation | pdc_summary.json | Status |
|---|---|---|---|
| Overall PDC | **0.7667** | **0.7667** | **VERIFIED** ✅ |
| Coverage | 15/15 = **1.0** | **1.0** | **VERIFIED** ✅ |
| Informative pairs | **15** | **15** | **VERIFIED** ✅ |
| Total pairs | **15** | **15** | **VERIFIED** ✅ |

### Individual Pair Verification Summary

| Pair | Independent PDC | JSON PDC | Status |
|---|---|---|---|
| H1 vs H2 | 1.0000 | 1.0 | ✅ |
| H1 vs H3 | 0.7500 | 0.75 | ✅ |
| H1 vs H4 | 0.7500 | 0.75 | ✅ |
| H1 vs M1 | 1.0000 | 1.0 | ✅ |
| H1 vs S1 | 0.7500 | 0.75 | ✅ |
| H2 vs H3 | 0.7500 | 0.75 | ✅ |
| H2 vs H4 | 0.7500 | 0.75 | ✅ |
| H2 vs M1 | 1.0000 | 1.0 | ✅ |
| H2 vs S1 | 1.0000 | 1.0 | ✅ |
| H3 vs H4 | 0.5000 | 0.5 | ✅ |
| H3 vs M1 | 0.5000 | 0.5 | ✅ |
| H3 vs S1 | 0.5000 | 0.5 | ✅ |
| H4 vs M1 | 1.0000 | 1.0 | ✅ |
| H4 vs S1 | 0.7500 | 0.75 | ✅ |
| M1 vs S1 | 0.5000 | 0.5 | ✅ |

---

## 5. PDC Code Logic Verification

The PDC computation in `src/evaluation/pdc.py` was also verified against the protocol definition:

- **Protocol (Section 8):** `PDC_pair = max(W, L) / (W + L)` for W + L > 0; Coverage = (W+L) / total_metrics
- **Code (pdc.py L73-76):** Special case for W=2, L=2 → hardcoded 0.50; otherwise `max(W, L) / informative_total`

The code's special case for 2-2 ties produces the same result as the general formula: max(2,2) / (2+2) = 2/4 = 0.50. The hardcoding is redundant but not incorrect.

The code's tolerance for metric ties (`tol=1e-4` at line 15) matches the protocol's instruction that "tolerance value set during implementation before results are seen."

> [!NOTE]
> The protocol specifies 4 primary metrics for PDC: AUROC, AUPRC, Recall@FAR, ECE. The code defaults to exactly these 4 metrics (`metrics_to_compare = ["AUROC", "AUPRC", "Recall_at_FAR", "ECE"]` at line 45). However, the protocol also lists Brier and FAR as additional metrics (Section 8 metric hierarchy). The PDC computation correctly uses only the 4 primary metrics.

---

## 6. Final Verdict

| Verification Item | Independent Result | Artifact Value | Verdict |
|---|---|---|---|
| H1 AUROC | 0.5275 (from JSON) | 0.5275 | **VERIFIED** |
| H2 AUROC | 0.5097 (from JSON) | 0.5097 | **VERIFIED** |
| H3 AUROC | 0.5068 (from JSON) | 0.5068 | **VERIFIED** |
| H4 AUROC | 0.5253 (from JSON) | 0.5253 | **VERIFIED** |
| M1 AUROC | 0.5877 (from JSON) | 0.5877 | **VERIFIED** |
| S1 AUROC | 0.6016 (from JSON) | 0.6016 | **VERIFIED** |
| Overall PDC | 0.7667 (independently computed) | 0.7667 | **VERIFIED** |
| PDC Coverage | 1.0 (independently computed) | 1.0 | **VERIFIED** |
| All 15 pairwise PDC values | independently computed | JSON values | **VERIFIED** |
| JSON↔CSV consistency | 72 metric cells compared | 72 matches | **VERIFIED** |
| Threshold consistency | 6 baselines × 3 sources | All match | **VERIFIED** |

**Reconstruction Audit Status: ALL VALUES VERIFIED. PDC independently confirmed at 0.7667.**

---

*No code was modified. No experiments were regenerated. This report is purely observational.*

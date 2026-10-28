# Forensic Verification Report: `reports/gate3_report.md` Status Audit

**Date:** 2026-08-05  
**Role:** Forensic Repository Auditor  
**Scope:** Forensic evaluation of `reports/gate3_report.md` against surviving active reports (`gate3_3_result_lineage.md`, `gate3_4_artifact_reconstruction.md`, `gate3_4_final_verdict.md`), JSON artifacts (`primary_k30_results.json`, `pdc_summary.json`, `sensitivity_k_results.json`), and governance tracking documents.  
**Execution Invariant:** **AUDIT ONLY — ZERO FILES MOVED, MODIFIED, OR REWRITTEN**.

---

## Executive Summary

A forensic verification was performed to determine whether `reports/gate3_report.md` should remain in the **ACTIVE** working reports directory or be moved to **ARCHIVE**. 

The audit evaluated five core criteria:
1. Preservation of unique scientific findings in downstream reports.
2. Presence of stale or superseded metrics/claims.
3. Primary evidence reliance in project governance documents.
4. Active cross-references across surviving reports.
5. Risk of scientific evidence loss upon archiving.

### Final Classification

$$\mathbf{KEEP\ ACTIVE}$$

`reports/gate3_report.md` must remain in the **ACTIVE** working directory. While `gate3_3_result_lineage.md` canonicalized the Mode A point metrics, `gate3_report.md` contains the **only formatted report tables in the repository** for:
- **Mode B External Diagnostic Results ($\tau^2$-Bench)** under frozen TerminalBench thresholds.
- **Horizon $K$ Sensitivity Analysis ($K=10, 20, 30$)** for $S1$ and $M1$.

Archiving `gate3_report.md` would remove active visibility of cross-benchmark generalization and horizon sensitivity evidence.

---

## Detailed Criterion Verification

### 1. Unique Scientific Findings Check

**Question:** Does `gate3_report.md` contain any scientific findings that are **NOT** already preserved in `reports/gate3_3_result_lineage.md`, `reports/gate3_4_artifact_reconstruction.md`, or `reports/gate3_4_final_verdict.md`?

**Verdict:** **YES (Contains Unique Formatted Results).**

**Evidence:**
1. **Mode B External Diagnostic Results ($\tau^2$-Bench) Table (Section 1):**
   - Formats evaluation metrics (AUROC, AUPRC, Recall@FAR $\le 5\%$, Test FAR, Brier, ECE) for all baselines ($H1, H2, H3, H4, M1, S1$) evaluated on $\tau^2$-Bench using frozen TerminalBench thresholds ($H1=0.20, H2=0.09, H3=0.01, H4=0.77, M1=0.80, S1=0.81$).
   - Neither `gate3_3_result_lineage.md`, `gate3_4_artifact_reconstruction.md`, nor `gate3_4_final_verdict.md` includes this $\tau^2$-Bench performance matrix.
2. **Horizon $K$ Sensitivity Analysis Table (Section 3):**
   - Formats AUROC and Recall@FAR $\le 5\%$ metrics for $S1$ (Random Forest) and $M1$ (Logistic Regression) across horizons $K=10$, $K=20$, and $K=30$.
   - Neither `gate3_3_result_lineage.md`, `gate3_4_artifact_reconstruction.md`, nor `gate3_4_final_verdict.md` includes this sensitivity analysis matrix.

---

### 2. Stale or Superseded Values Audit

**Question:** Does `gate3_report.md` contain stale or superseded values?

**Verdict:** **PARTIAL (Point Metrics 100% Valid; Minor Text Metadata Staleness).**

**Detailed Breakdown:**

| Item / Metric | `gate3_report.md` Value | Canonical Value (`primary_k30_results.json` / `gate3_3`) | Status | Analysis |
|---|---|---|---|---|
| **AUROC (H1–S1)** | $H1: 0.5275$, $H2: 0.5097$, $H3: 0.5068$, $H4: 0.5253$, $M1: 0.5877$, $S1: 0.6016$ | $H1: 0.5275$, $H2: 0.5097$, $H3: 0.5068$, $H4: 0.5253$, $M1: 0.5877$, $S1: 0.6016$ | **CANONICAL MATCH** ✅ | Point metrics match `primary_k30_results.json` exactly. |
| **AUPRC (H1–S1)** | $H1: 0.5995$, $H2: 0.5953$, $H3: 0.7106$, $H4: 0.5936$, $M1: 0.6366$, $S1: 0.6402$ | $H1: 0.5995$, $H2: 0.5953$, $H3: 0.7106$, $H4: 0.5936$, $M1: 0.6366$, $S1: 0.6402$ | **CANONICAL MATCH** ✅ | Point metrics match `primary_k30_results.json` exactly. |
| **Recall @ FAR $\le 5\%$** | $H1: 0.0943$, $H2: 0.0607$, $H3: 0.9909$, $H4: 0.0628$, $M1: 0.1286$, $S1: 0.0722$ | $H1: 0.0943$, $H2: 0.0607$, $H3: 0.9909$, $H4: 0.0628$, $M1: 0.1286$, $S1: 0.0722$ | **CANONICAL MATCH** ✅ | Point metrics match `primary_k30_results.json` exactly. |
| **Calibrated Thresholds ($\tau^*$)** | $H1: 0.20$, $H2: 0.09$, $H3: 0.01$, $H4: 0.77$, $M1: 0.80$, $S1: 0.81$ | $H1: 0.20$, $H2: 0.09$, $H3: 0.01$, $H4: 0.77$, $M1: 0.80$, $S1: 0.81$ | **CANONICAL MATCH** ✅ | Frozen thresholds match calibration JSON exactly. |
| **Overall PDC & Coverage** | $\text{PDC} = 0.7667$, $\text{Coverage} = 100.0\%$ | $\text{PDC} = 0.7667$, $\text{Coverage} = 100.0\%$ | **CANONICAL MATCH** ✅ | Matches `pdc_summary.json` and `gate3_4_artifact_reconstruction.md`. |
| **Bootstrap Iteration Count** | $B = 500$ (Line 65 text claim) | $B = 100$ (executed code reality) | **MINOR STALENESS** ⚠️ | Prose text claims $B=500$. `gate3_3` Section 6 and `gate3_4_final_verdict` (F-5) clarify actual execution used $B=100$. |
| **Split Episode Counts** | $31,035$ TRAIN / $10,521$ CALIBRATION (Lines 63–64) | $31,016$ TRAIN / $10,516$ CALIB ($20,454$ / $6,935$ actionable) | **MINOR STALENESS** ⚠️ | Pre-filtering raw row parsing counts; `gate3_3` Section 2 provides the canonical manifest totals ($31,016$ / $10,516$ raw; $20,454$ / $6,935$ actionable). |

---

### 3. Governance Reliance Audit

**Question:** Does any governance document (`RESEARCH_LOG.md`, `DECISION_LOG.md`, `PROJECT_CONTROL.md`, `ROADMAP.md`) still rely on `gate3_report.md` as the primary evidence document?

**Verdict:** **NO (Governance Points to `gate3_3_result_lineage.md` and Executed JSON Artifacts).**

**Evidence:**
- `RESEARCH_LOG.md`: Mentions `gate3_report.md` in a historical report consolidation inventory entry (Line 80), but cites `results/baseline_runs/primary_k30_results.json`, `results/baseline_runs/pdc_summary.json`, and `reports/gate3_3_result_lineage.md` as primary evidence for Gate 3 decisions.
- `docs/DECISION_LOG.md`: Decision D-016 cites `reports/gate3_3_result_lineage.md` and `primary_k30_results.json` as its primary evidence.
- `docs/PROJECT_CONTROL.md`: Does not cite `gate3_report.md`.
- `docs/ROADMAP.md`: Does not cite `gate3_report.md`.

---

### 4. Active Cross-Reference Check

**Question:** Does any remaining active report reference `gate3_report.md`?

**Verdict:** **YES.**

**Evidence:**
- `reports/gate3_3_result_lineage.md` explicitly references `gate3_report.md` in Section 3 ("Result Artifact Consistency & Reconciliation Table") to document the lineage resolution between narrative prose template typos from early drafts and the canonical executed metrics.

---

### 5. Impact of Archiving Analysis

**Question:** If `gate3_report.md` were archived today, would any reproducibility, implementation, or scientific evidence be lost?

**Verdict:** **YES (Loss of Active Report Visibility for Mode B and Horizon $K$ Sensitivity).**

**Evidence:**
1. **Mode B Diagnostic Evidence:** `gate3_report.md` is the **only report in `reports/`** presenting the complete $\tau^2$-Bench evaluation table under frozen TerminalBench thresholds. Moving it to `archive/` would leave the active workspace without any document displaying Mode B performance across all 6 baselines.
2. **Horizon $K$ Sensitivity Evidence:** `gate3_report.md` is the **only report in `reports/`** presenting the Horizon $K$ ($K=10, 20, 30$) sensitivity table for $S1$ and $M1$.
3. **Primary Gate Sequence Continuity:** `gate3_report.md` anchors the canonical milestone report ladder (`gate1_report.md`, `gate1_5_report.md`, `gate2_report.md`, `gate2_1_report.md`, `gate3_report.md`).

---

## 6. Final Decision & Recommendation

### Classification: `KEEP ACTIVE`

`reports/gate3_report.md` must remain in the active `reports/` directory.

```
       ┌─────────────────────────────────────────────────────────────┐
       │                   FINAL CLASSIFICATION                      │
       │                        KEEP ACTIVE                          │
       └─────────────────────────────────────────────────────────────┘
```

### Key Rationale
1. **Contains Unique Empirical Tables:** It holds the only active report tables for Mode B ($\tau^2$-Bench) evaluation and Horizon $K$ ($10, 20, 30$) sensitivity.
2. **Point Metrics are 100% Canonical:** All primary metrics ($S1\text{ AUROC}=0.6016$, $M1\text{ AUROC}=0.5877$, $\text{PDC}=0.7667$, thresholds $\tau^*$) are exact matches to `primary_k30_results.json` and `gate3_3_result_lineage.md`.
3. **Minor Text Staleness is Reconciled:** The minor prose text claims ($B=500$ vs executed $B=100$, pre-filtering split counts) are explicitly documented and superseded by `reports/gate3_3_result_lineage.md` and `reports/gate3_4_final_verdict.md`.
4. **Maintains Milestone Sequence:** Preserves the core gate report chain (`gate1`, `gate1_5`, `gate2`, `gate2_1`, `gate3`).

---
*Verification Audit Complete. Report output strictly to `reports/gate3_report_status_verification.md`.*

# AIRE-Trace Claim Traceability Audit

This document records every major numerical or scientific claim in the master manuscript,
with its source artifact, evidence level, and verification status.
Generated: 2026-08-14. Based on repository inspection completed before manuscript drafting.

---

## Population and Provenance Claims

| # | Claim | Section | Source Artifact | Evidence | Field/Line | Verified |
|---|-------|---------|-----------------|----------|------------|---------|
| P1 | Declared Tracebench rows: 3,316 | IV.B | post_recovery_audit.txt | LEVEL 1 | "Total Declared Tracebench Rows: 3316" | YES |
| P2 | Valid reconstructed episodes: 636 | IV.B | post_recovery_audit.txt | LEVEL 1 | "Total Valid Reconstructed Episodes: 636" | YES |
| P3 | Structurally invalid: 2,655 | IV.B | post_recovery_audit.txt | LEVEL 1 | "Total Structurally Invalid: 2655" | YES |
| P4 | Missing artifact path: 25 | IV.B | post_recovery_audit.txt | LEVEL 1 | "Total Missing Artifact Path: 25" | YES |
| P5 | Coverage: 19.18% | IV.B | post_recovery_audit.txt | LEVEL 1 | "Final Coverage: 636 / 3316 (19.18%)" | YES |
| P6 | Recovery: 1,457 network-excluded downloaded; 100% structurally invalid | IV.B | lineage_verification.txt | LEVEL 1 | all transition counts | YES |
| P7 | TRAIN: 163 episodes | IV.D | gate7_ablation.json | LEVEL 1 | A0 train_episodes: 163 | YES |
| P8 | CALIBRATION: 57 episodes | IV.D | gate7_ablation.json | LEVEL 1 | A0 calibration_episodes: 57 | YES |
| P9 | TEST: 416 episodes | IV.D | primary_k30_results.json | LEVEL 1 | consistent across all models | YES |
| P10| TEST failed episodes: 317 | IV.E | primary_k30_results.json | LEVEL 1 | Exclusion_Stats.Total_Failures: 317 | YES |
| P11| TEST successful episodes: 99 | IV.E | Computed: 416-317 | LEVEL 1 | gate6_false_alarms.json confirms denominator | YES |
| P12| Valid annotated failure episodes: 257 | IV.E | primary_k30_results.json | LEVEL 1 | Exclusion_Stats.Valid_Episodes: 257 | YES |
| P13| Unannotated failure episodes: 60 | IV.E | primary_k30_results.json | LEVEL 1 | Exclusion_Stats.Unannotated_Episodes: 60 | YES |

---

## Primary Mode A AUROC Claims

| # | Claim | Section | Source Artifact | Evidence | Field | Verified |
|---|-------|---------|-----------------|----------|-------|---------|
| R1 | H1 AUROC = 0.6205 | VIII.C | primary_k30_results.json | LEVEL 1 | mode_a_terminalbench_test.H1.AUROC | YES |
| R2 | H1 95% CI [0.5799, 0.6513] | VIII.C | baseline_comparison_table.csv | LEVEL 1 | H1 AUROC_95CI | YES |
| R3 | H2 AUROC = 0.5752 | VIII.C | primary_k30_results.json | LEVEL 1 | mode_a_terminalbench_test.H2.AUROC | YES |
| R4 | H2 95% CI [0.5402, 0.6116] | VIII.C | baseline_comparison_table.csv | LEVEL 1 | H2 AUROC_95CI | YES |
| R5 | H3 AUROC = 0.5074 | VIII.C | primary_k30_results.json | LEVEL 1 | mode_a_terminalbench_test.H3.AUROC | YES |
| R6 | H3 95% CI [0.5024, 0.5122] | VIII.C | baseline_comparison_table.csv | LEVEL 1 | H3 AUROC_95CI | YES |
| R7 | H4 AUROC = 0.6135 | VIII.C | primary_k30_results.json | LEVEL 1 | mode_a_terminalbench_test.H4.AUROC | YES |
| R8 | H4 95% CI [0.5729, 0.6445] | VIII.C | baseline_comparison_table.csv | LEVEL 1 | H4 AUROC_95CI | YES |
| R9 | M1 AUROC = 0.6215 | VIII.C | primary_k30_results.json | LEVEL 1 | mode_a_terminalbench_test.M1.AUROC | YES |
| R10| M1 95% CI [0.5630, 0.6629] | VIII.C | baseline_comparison_table.csv | LEVEL 1 | M1 AUROC_95CI | YES |
| R11| S1 AUROC = 0.6371 | VIII.C | primary_k30_results.json | LEVEL 1 | mode_a_terminalbench_test.S1.AUROC | YES |
| R12| S1 95% CI [0.5885, 0.6745] | VIII.C | baseline_comparison_table.csv | LEVEL 1 | S1 AUROC_95CI | YES |
| R13| S2 AUROC = 0.5496 | VIII.C | primary_k30_results.json | LEVEL 1 | mode_a_terminalbench_test.S2.AUROC | YES |
| R14| S2 95% CI [0.5212, 0.5734] | VIII.C | baseline_comparison_table.csv | LEVEL 1 | S2 AUROC_95CI | YES |

---

## Frozen Threshold Claims

| # | Claim | Section | Source Artifact | Evidence | Verified |
|---|-------|---------|-----------------|----------|---------|
| T1 | H1 threshold = 0.86 | V.D | primary_k30_results.json | LEVEL 1 | YES |
| T2 | H2 threshold = 0.89 | V.D | primary_k30_results.json | LEVEL 1 | YES |
| T3 | H3 threshold = 0.01 (calib FAR = 1.000) | V.D | primary_k30_results.json | LEVEL 1 | YES |
| T4 | H4 threshold = 0.93 | V.D | primary_k30_results.json | LEVEL 1 | YES |
| T5 | M1 threshold = 0.98 | V.D | primary_k30_results.json | LEVEL 1 | YES |
| T6 | S1 threshold = 0.97 | V.D | primary_k30_results.json | LEVEL 1 | YES |
| T7 | S2 threshold = 0.74 | V.D | primary_k30_results.json | LEVEL 1 | YES |

---

## FAR and Recall@FAR Claims

| # | Claim | Section | Source Artifact | Evidence | Verified |
|---|-------|---------|-----------------|----------|---------|
| F1 | H1 TEST FAR = 0.000 | VIII.C | primary_k30_results.json | LEVEL 1 | YES |
| F2 | H3 TEST FAR = 1.000 | VIII.C | primary_k30_results.json | LEVEL 1 | YES |
| F3 | H3 Recall@FAR = undefined (NaN) | VIII.C | primary_k30_results.json | LEVEL 1 | YES (null field) |
| F4 | M1 Recall@FAR = 0.0078 | VIII.C | primary_k30_results.json | LEVEL 1 | YES |
| F5 | S1 Recall@FAR = 0.0000 | VIII.C | primary_k30_results.json | LEVEL 1 | YES |
| F6 | S1 TEST FAR = 0.0404 | VIII.C | primary_k30_results.json | LEVEL 1 | YES |

---

## Statistical Test Claims

| # | Claim | Section | Source Artifact | Evidence | Verified |
|---|-------|---------|-----------------|----------|---------|
| S1 | S1 vs S2 AUROC: p_raw=0.001, p_adj=0.006, reject H0 | VIII.D | gate7_statistical_tests.json | LEVEL 1 | YES |
| S2 | S1 vs H2 AUROC: p_raw=0.001, p_adj=0.006, reject H0 | VIII.D | gate7_statistical_tests.json | LEVEL 1 | YES |
| S3 | S1 vs H3 AUROC: p_raw=0.001, p_adj=0.006, reject H0 | VIII.D | gate7_statistical_tests.json | LEVEL 1 | YES |
| S4 | S1 vs M1 AUROC: p_raw=0.159, p_adj=0.318, NOT reject | VIII.D | gate7_statistical_tests.json | LEVEL 1 | YES |
| S5 | S1 vs H1 AUROC: p_raw=0.195, p_adj=0.318, NOT reject | VIII.D | gate7_statistical_tests.json | LEVEL 1 | YES |
| S6 | S1 vs H4 AUROC: p_raw=0.056, p_adj=0.168, NOT reject | VIII.D | gate7_statistical_tests.json | LEVEL 1 | YES |
| S7 | S1 vs S2 AUPRC: p_adj=0.012, reject H0 | VIII.D | gate7_statistical_tests.json | LEVEL 1 | YES |
| S8 | H3 Delta_obs AUPRC vs S1 = -0.0250 (directionally fav, not significant) | VIII.D | gate7_statistical_tests.json | LEVEL 1 | YES |
| S9 | Bootstrap B=1000 | VII.B | RESEARCH_LOG.md 2026-08-11 | LEVEL 1 | YES |
| S10| Holm-Bonferroni alpha=0.05 | VII.C | gate7_statistical_tests.json | LEVEL 1 | YES |

---

## PDC Claims

| # | Claim | Section | Source Artifact | Evidence | Verified |
|---|-------|---------|-----------------|----------|---------|
| PDC1 | Overall PDC = 0.8294 | VIII.E | pdc_summary.json | LEVEL 1 | YES |
| PDC2 | Coverage = 0.881 | VIII.E | pdc_summary.json | LEVEL 1 | YES |
| PDC3 | Total pairs = 21, informative pairs = 21 | VIII.E | pdc_summary.json | LEVEL 1 | YES |

---

## Gate 6 Claims

| # | Claim | Section | Source Artifact | Evidence | Verified |
|---|-------|---------|-----------------|----------|---------|
| G1 | S1 false alarm episodes = 4, FAR = 4/99 = 0.0404 | IX.C | gate6_false_alarms.json | LEVEL 1 | YES |
| G2 | H3 false alarm episodes = 99, FAR = 1.000 | IX.C | gate6_false_alarms.json | LEVEL 1 | YES |
| G3 | H1 false alarm episodes = 0 | IX.C | gate6_false_alarms.json | LEVEL 1 | YES |
| G4 | H3 late detections: 3,339 total; 51/257 episodes only-late (19.84%) | IX.B | gate6_late_detections.json | LEVEL 1 | YES |
| G5 | S1 late detections: 19 total; 16/257 episodes only-late (6.23%) | IX.B | gate6_late_detections.json | LEVEL 1 | YES |
| G6 | S1 total alerts = 25, mean 0.060/episode, max 2 | IX.D | gate6_alert_burden.json | LEVEL 1 | YES |
| G7 | H3 total alerts = 8,012, mean 19.26/episode | IX.D | gate6_alert_burden.json | LEVEL 1 | YES |
| G8 | Alert burden denominator = 416 TEST episodes | IX.D | gate6_alert_burden.json | LEVEL 1 | YES (distribution sums verified) |

---

## Ablation Claims

| # | Claim | Section | Source Artifact | Evidence | Verified |
|---|-------|---------|-----------------|----------|---------|
| A1 | A0 (full baseline) S1 AUROC = 0.6371 | VIII.G | gate7_ablation.json | LEVEL 1 | YES |
| A2 | A4 (no error/retry) AUROC = 0.5302 | VIII.G | gate7_ablation.json | LEVEL 1 | YES |
| A3 | A4 Delta_AUROC = -0.1069 (0.6371 - 0.5302 = 0.1069) | VIII.G | gate7_ablation.json | LEVEL 1 | YES (computed) |
| A4 | A1 AUROC = 0.6357, Delta = -0.0014 | VIII.G | gate7_ablation.json | LEVEL 1 | YES |
| A5 | A3 AUROC = 0.6383 (slight increase, +0.0012) | VIII.G | gate7_ablation.json | LEVEL 1 | YES |
| A6 | A6 AUROC = 0.6341, Delta = -0.0030 | VIII.G | gate7_ablation.json | LEVEL 1 | YES |

---

## FAR Sensitivity Claims (S1)

| # | Claim | Section | Source Artifact | Evidence | Verified |
|---|-------|---------|-----------------|----------|---------|
| FS1| S1 at FAR 1%: threshold=0.97, TEST FAR=0.0404, Recall=0.000 | VIII.F | gate7_far_sensitivity.json | LEVEL 1 | YES |
| FS2| S1 at FAR 5%: threshold=0.97, TEST FAR=0.0404, Recall=0.000 | VIII.F | gate7_far_sensitivity.json | LEVEL 1 | YES |
| FS3| S1 at FAR 10%: threshold=0.93, TEST FAR=0.1212, Recall=0.0973 | VIII.F | gate7_far_sensitivity.json | LEVEL 1 | YES |

---

## Methodological Claims

| # | Claim | Section | Source | Evidence | Verified |
|---|-------|---------|--------|----------|---------|
| M1 | Episode-cluster bootstrap (not prefix-level) | VII.B | RESEARCH_LOG.md 2026-08-11 | LEVEL 1 | YES |
| M2 | Episode-balanced weights w = 1/min(Ti,30) | VII.A | src/evaluation/evaluator.py | LEVEL 1 | YES |
| M3 | Threshold calibration on CALIBRATION only | V.D | src/evaluation/thresholding.py | LEVEL 1 | YES |
| M4 | K=30 checkpoint horizon | V.B | primary_k30_results.json | LEVEL 1 | YES |
| M5 | FAR denominator = successful TEST episodes (99) | III.D | gate6_false_alarms.json | LEVEL 1 | YES |
| M6 | Recall@FAR denominator = valid annotated failures (257) | V.E | primary_k30_results.json | LEVEL 1 | YES |
| M7 | 13 Category-A features | V.A | gate7_ablation.json A0 retained_features | LEVEL 1 | YES |
| M8 | S1 = RandomForestClassifier (n_estimators=100, max_depth=6, seed=42) | VI.C | src/baselines/random_forest.py | LEVEL 1 | YES |
| M9 | S2 = GRU (hidden_dim=64, 1 layer, epochs=10, seed=42) | VI.D | src/baselines/sequence.py | LEVEL 1 | YES |
| M10| L = L_PENDING, not evaluated | VI.E | src/baselines/registry.py | LEVEL 1 | YES |
| M11| 38 tests passing | XII.D | RESEARCH_LOG.md 2026-08-11 | LEVEL 1 | YES |

---

## Claim-Strength Audit (Prohibited Language Check)

The following terms were searched for in the manuscript. Results:

| Term | Occurrences | Supported? |
|------|-------------|-----------|
| "first" | 0 | N/A |
| "novel" | 0 | N/A |
| "best" | 0 | N/A |
| "superior" | 0 | N/A |
| "proves" | 0 | N/A |
| "causes" | 0 | N/A |
| "generalizes" | 0 | N/A |
| "state-of-the-art" | 0 | N/A |
| "guarantees" | 0 | N/A |
| "robust" | 0 | N/A |
| "significant" | Multiple | All occurrences reference Holm-corrected statistical tests; supported |
| "highest observed AUROC" | Used for S1 | Supported (S1 AUROC = 0.6371 is highest in TABLE III) |
| "strongly associated" | Used for A4 | Supported (Delta_AUROC = -0.1069 is substantially largest ablation impact) |
| "universal superiority" | Explicitly denied | Correct |

---

## Unverified Items Requiring Attention Before Submission

| # | Item | Action Required |
|---|------|-----------------|
| U1 | All 9 reference entries marked [REFERENCE TO BE VERIFIED] | Verify title, authors, venue, year against authoritative source |
| U2 | 4 additional [RELATED-WORK CITATION REQUIRED] placeholders | Find and verify actual citations |
| U3 | Author names, affiliations, emails | Provide actual author information |
| U4 | IEEE venue, conference name, submission date | Determined when venue is selected |
| U5 | All 6 figures marked [FIGURE REQUIRED FROM CANONICAL ARTIFACT] | Generate from canonical JSON/CSV data |
| U6 | Mode B metrics near-chance (AUROC 0.50-0.53): further analysis of tau2-Bench conditions | Optional investigation before submission |

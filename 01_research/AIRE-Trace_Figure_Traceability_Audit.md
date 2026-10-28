# AIRE-Trace Figure Traceability Audit

This document records the provenance, sources, and generation methods for all figures included in the AIRE-Trace IEEE manuscript. All empirical figures were generated programmatically directly from the canonical evaluation artifacts, without manual data entry or alteration.

---

## Figure 1: AIRE-Trace Evaluation Architecture
- **Title:** AIRE-Trace standardized prospective evaluation pipeline
- **Type:** Conceptual diagram
- **Source Artifact:** `AIRE-Trace_Frozen_Protocol_and_Plan.md` and `AIRE-Trace_Master_IEEE_Manuscript.md` (Sections III, IV, and V)
- **Evidence Level:** Protocol definition
- **Exact Fields Used:** Conceptual components (Provenance/Recovery, TRAIN/CALIBRATION/TEST split, Threshold Calibration, Gate 6 Operational Analysis)
- **Transformations/Calculations:** None
- **Derived Statistic Calculated:** None
- **Caption:** Fig. 1. AIRE-Trace standardized prospective evaluation pipeline. Trajectories are provenance-audited before episode-level splitting; trainable methods are fitted on TRAIN, operating thresholds are selected on CALIBRATION under the false-alarm constraint, and frozen thresholds are applied to the TEST population for prospective evaluation and operational analysis.
- **Manuscript Section:** Introduction / Problem Formulation
- **Output Filenames:** `fig1_aire_trace_architecture.svg`, `fig1_aire_trace_architecture.png`
- **Validation Status:** PASS

---

## Figure 2: Dataset Provenance and Recovery Flow
- **Title:** Provenance and exclusion accounting for the AIRE-Trace empirical population
- **Type:** Conceptual diagram
- **Source Artifact:** `post_recovery_audit.txt` and `AIRE-Trace_Master_IEEE_Manuscript.md` (Section IV.B)
- **Evidence Level:** Canonical Audit
- **Exact Fields Used:** Declared rows (3,316), Excluded (2,680), Structurally invalid (2,655), Missing artifact path (25), Valid/recovered episodes (636)
- **Transformations/Calculations:** None
- **Derived Statistic Calculated:** None
- **Caption:** Fig. 2. Provenance and exclusion accounting for the AIRE-Trace empirical population. The downstream study is restricted to the canonical 636-episode population for which the required trajectory evidence was verified or deterministically reconstructed.
- **Manuscript Section:** Section IV. Dataset, Provenance, and Study Population
- **Output Filenames:** `fig2_provenance_recovery.svg`, `fig2_provenance_recovery.png`
- **Validation Status:** PASS

---

## Figure 3: Prospective Prefix / Checkpoint Evaluation
- **Title:** Prospective prefix evaluation semantics
- **Type:** Conceptual diagram
- **Source Artifact:** `AIRE-Trace_Frozen_Protocol_and_Plan.md` and `AIRE-Trace_Master_IEEE_Manuscript.md` (Section III.C)
- **Evidence Level:** Protocol definition
- **Exact Fields Used:** Conceptual representations of checkpoing $t$, unobserved future events, failure onset, valid prospective alert, and late detection.
- **Transformations/Calculations:** None
- **Derived Statistic Calculated:** None
- **Caption:** Fig. 3. Prospective prefix evaluation semantics. At each permitted checkpoint, the monitor observes only the trajectory information available up to that point. Alerts at or before the annotated failure onset are prospective detections; alerts after onset are analyzed separately as late detections.
- **Manuscript Section:** Section III. Problem Formulation
- **Output Filenames:** `fig3_prospective_prefix.svg`, `fig3_prospective_prefix.png`
- **Validation Status:** PASS

---

## Figure 4: PRIMARY MODE A TEST AUROC
- **Title:** Mode A TEST AUROC for the evaluated warning methods
- **Type:** Empirical
- **Source Artifact:** `results/baseline_runs/baseline_comparison_table.csv`
- **Evidence Level:** Level 1 (Empirical results)
- **Exact Fields Used:** `method` (H1-H4, M1, S1, S2), `AUROC`, `AUROC_95CI`
- **Transformations/Calculations:** Lower and upper error bounds extracted directly from the canonical string `[low, high]` 95% CI format in the CSV for matplotlib `errorbar` generation. No values were re-calculated.
- **Derived Statistic Calculated:** Error bar relative lengths (AUROC - ci_lower, ci_upper - AUROC) for plotting purposes only.
- **Caption:** Fig. 4. Mode A TEST AUROC for the evaluated warning methods under the K=30 protocol. Error bars denote the corresponding 95% episode-cluster bootstrap confidence intervals.
- **Manuscript Section:** Section VIII. Results (Table III visualization)
- **Output Filenames:** `fig4_mode_a_auroc.svg`, `fig4_mode_a_auroc.png`
- **Validation Status:** PASS

---

## Figure 5: FEATURE/COMPONENT ABLATION
- **Title:** A4 component ablation under the defined evaluation protocol
- **Type:** Empirical
- **Source Artifact:** `reports/gate7_ablation.json`
- **Evidence Level:** Level 1 (Empirical results)
- **Exact Fields Used:** `ablation_id` (A0-A6), `description`, `TEST_AUROC`
- **Transformations/Calculations:** Plotted exactly from the `TEST_AUROC` fields. Delta values plotted visually by taking the difference with `A0`'s AUROC, exactly mirroring the `Delta_AUROC` column reported in Table VI.
- **Derived Statistic Calculated:** Delta AUROC strictly for plotting annotation.
- **Caption:** Fig. 5. A4 component ablation under the defined evaluation protocol. The observed AUROC change is reported as an empirical association under the ablation design and does not establish causal attribution.
- **Manuscript Section:** Section VIII.G. Feature Ablation Results
- **Output Filenames:** `fig5_a4_ablation.svg`, `fig5_a4_ablation.png`
- **Validation Status:** PASS

---

## Figure 6: GATE 6 OPERATIONAL ANALYSIS
- **Title:** Gate 6 operational analysis
- **Type:** Empirical
- **Source Artifact:** `results/baseline_runs/gate6_false_alarms.json`, `results/baseline_runs/gate6_late_detections.json`, `results/baseline_runs/gate6_alert_burden.json`
- **Evidence Level:** Level 1 (Empirical results)
- **Exact Fields Used:** `false_alarm_rate`, `pct_failed_episodes_with_only_late_alerts`, `alerts_per_episode_mean` for models H1-H4, M1, S1, S2.
- **Transformations/Calculations:** Percentage converted to decimal proportion for consistency. Plotted exactly from the fields.
- **Derived Statistic Calculated:** None.
- **Caption:** Fig. 6. Gate 6 operational analysis showing false alarms, late-alert-only episodes, and alert burden under the frozen TEST evaluation.
- **Manuscript Section:** Section IX. Operational Analysis (Gate 6)
- **Output Filenames:** `fig6_gate6_operational.svg`, `fig6_gate6_operational.png`
- **Validation Status:** PASS

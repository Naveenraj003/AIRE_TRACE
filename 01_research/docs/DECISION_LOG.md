# AIRE-Trace Decision Log

**New Log Format Mandate:** All new entries in this log MUST use the following format:

```markdown
## YYYY-MM-DD HH:MM — EVENT-ID

Type: DECISION
Track: IEEE-RESEARCH | LIVE-DEMO | FUTURE-RESEARCH | REPOSITORY

### Event
What happened.

### Motivation
Why it was done or considered.

### Evidence
Exact file, command, artifact, test output, or user decision supporting the event. (e.g., LEVEL 1 — DIRECTLY OBSERVED).

### Decision
What was decided.

### Files Affected
Exact files changed, if any.

### Result
Observed result only. Do not convert assumptions into results.

### Scientific Impact
Whether the event affects: protocol, implementation, evaluation, statistics, demo only, documentation only.

### Status
PROPOSED | IN PROGRESS | COMPLETED | FROZEN | REJECTED | BLOCKED

### Next Action
The next concrete action, if any.
```

---

## [FROZEN] Dataset Roles
**Question:** What roles do the datasets play in training and evaluation?
**Decision:** TerminalBench is the primary prospective benchmark (Mode A) and the sole source for training/calibration. τ²-Bench is the secondary, external-transfer diagnostic (Mode B) and is evaluation-only.
**Evidence:** `AIRE-Trace_Frozen_Protocol_and_Plan.md` (Section 4).

## [FROZEN] Evaluation Metrics and Modes
**Question:** How are metrics applied across datasets without onset labels?
**Decision:** Mode A (TerminalBench) supports prospective evaluation (AUROC, AUPRC, Recall@FAR, Lead time). Mode B (τ²-Bench) only supports eventual-outcome diagnostic evaluation. Metrics must not be pooled or presented as identical across modes.
**Evidence:** `AIRE-Trace_Frozen_Protocol_and_Plan.md` (Section 4).

## [FROZEN] Checkpoint Schedule Construction
**Question:** How are prefixes extracted for evaluation?
**Decision:** Checkpoints must be outcome-independent and episode-symmetric. Anchor-then-stride is rejected. (Exact horizon K is pending Gate 1).
**Evidence:** `AIRE-Trace_Frozen_Protocol_and_Plan.md` (Rule 1).

## [FROZEN] Statistical Unit
**Question:** What is the unit of statistical measurement?
**Decision:** The statistical unit is the episode, not the prefix. Episode-cluster bootstrap must be used for CIs. Episode-balanced prefix weighting (1/n_i) is used for aggregation.
**Evidence:** `AIRE-Trace_Frozen_Protocol_and_Plan.md` (Rule 7, Rule 11).

## [FROZEN] Threshold Calibration
**Question:** How are thresholds set?
**Decision:** Fit models on TRAIN. On CALIBRATION, select threshold maximizing recall subject to FAR ≤ target. Freeze this threshold and apply unchanged to TEST and τ²-Bench.
**Evidence:** `AIRE-Trace_Frozen_Protocol_and_Plan.md` (Section 8).

## [FROZEN] Ranking Stability Statistic
**Question:** How do we measure ranking consistency across metrics?
**Decision:** Use Pairwise Direction Consistency (PDC) over informative pairs (W+L > 0), explicitly reporting coverage. A 2-2 tie scores 0.50.
**Evidence:** `AIRE-Trace_Frozen_Protocol_and_Plan.md` (Section 8).

## [FROZEN] Terminal Event Sanitization
**Question:** Do we score at t=T?
**Decision:** Yes, but outcome-bearing content in terminal events must be explicitly sanitized/stripped prior to feature computation.
**Evidence:** `AIRE-Trace_Frozen_Protocol_and_Plan.md` (Rule 6).

## [VERIFIED] TerminalBench Episode Sufficiency & Task-Cluster Splitting
**Question:** Does TerminalBench contain enough episodes for a 3-way split, and is random episode splitting safe?
**Decision:** TerminalBench contains 52,104 episodes across 89 tasks (60.37% failure rate), fully supporting a 3-way split. However, random episode splitting causes severe Task Leakage (~585 runs per task). Splitting MUST be task-cluster aware (all episodes of task $T_i$ assigned to exactly one split).
**Evidence:** `reports/gate1_dataset_inventory.md`, `RESEARCH_LOG.md` (2026-07-31).

## [FROZEN] Task-Group Disjoint Splitting & Task Generalization Claim
**Question:** What split policy and generalization claim should be adopted for TerminalBench?
**Decision:** Episode-random split results in 100% Task Leakage. Adopt Task-Group Disjoint Splitting (53 tasks TRAIN, 18 tasks CALIB, 18 tasks TEST). Primary research claim: "Generalization to unseen tasks under task-disjoint splitting."
**Evidence:** `reports/gate1_5_split_analysis.json`, `reports/gate1_5_methodological_validation.md`.

## [FROZEN] Episode-Adaptive Checkpoint Formulation
**Question:** How should prospective warning prediction opportunities be formulated?
**Decision:** Use Episode-Adaptive Checkpoints $t \in \{1, \dots, \min(T_i, K)\}$ ($K=30$) with episode-balanced prefix sample weighting ($1/n_i$), avoiding post-terminal padding and observation-window bias. Sensitivity horizons: $K \in \{10, 20, 30\}$.
**Evidence:** `reports/gate1_5_warning_opportunity_analysis.md`.

## [FROZEN] Failure-Onset Semantics & Unannotated Failures
**Question:** What is the operational failure-onset definition and how are unannotated failures handled?
**Decision:** Operational onset is approved ONLY as "annotation-derived error onset" ($\min(\text{incorrect\_step\_ids})$ for Tracebench, covering 66.89% of failures). Never call it true failure onset or causal onset. The 630 unannotated failed episodes are classified as *onset-unannotated failures*—excluded from lead-time CIs, but retained for overall prospective recall at $t \le T_i$.
**Evidence:** `reports/gate1_5_onset_semantics.md`.

## [FROZEN] Canonical Preprocessing Pipeline & Parquet Manifests
**Question:** What are the canonical processed datasets and feature vectors for experiments?
**Decision:** Category A baseline features (`steps_so_far`, `actor_role`, `action_type`, `tool_error_count`, `retry_count`, `unique_tools_used`, `tool_call_ratio`, `repeated_action_last2`). Exported to `data/processed/manifests/` as Parquet manifests with dataset commit SHAs (`terminalbench`: `04e8940f5b6736a7ce8d22224fe2f2af74163ed2`, `tracebench`: `7da2e4f45b330be8b6e8f1cff835247723cb3341`).
**Evidence:** `reports/gate2_preprocessing_report.md`, `reports/gate2_validation_report.json`.

## [VERIFIED] Pre-Baseline Implementation & Manifest Audit
**Question:** Is the Gate 2 implementation 100% compliant with frozen protocol rules and manifest integrity?
**Decision:** Gate 2.1 audit confirmed: (1) 13 numerical columns represent a faithful vector space decomposition of frozen categorical attributes; (2) Manifest schema supports exact episode weighting $w_{i,t} = \frac{1}{\min(T_i, 30)}$; (3) Retry semantics strictly isolate error sequences; (4) 100% invariant test traceability; (5) Manifest integrity verified across all 804,862 prefix records; (6) Task-disjoint split allocation (53/18/18) verified 100% reproducible with seed 42.
**Evidence:** `reports/gate2_1_episode_weighting_audit.md`, `reports/gate2_1_retry_semantics.md`, `reports/gate2_1_test_coverage.md`, `reports/gate2_1_split_reproducibility.md`.

## [FROZEN] Baseline Model Ladder & Calibrated Thresholds
**Question:** What are the baseline performance numbers and frozen thresholds for prospective failure warning?
**Decision:** Conventional baseline ladder ($H1, H2, H3, H4, M1, S1$, $L_{\text{PENDING}}$) evaluated under strict protocol. Warning thresholds calibrated on CALIBRATION ($\text{FAR} \le 5\%$) and frozen: $H1 = 0.20$, $H2 = 0.09$, $H3 = 0.01$, $H4 = 0.77$, $M1 = 0.80$, $S1 = 0.81$. Best tabular baseline: Random Forest ($S1$) achieving $\text{AUROC} = 0.7635$, $\text{Recall@FAR} \le 5\% = 0.4128$ on TerminalBench TEST ($K=30$).
**Evidence:** `reports/gate3_baseline_protocol.md`, `results/baseline_runs/primary_k30_results.json`, `results/baseline_runs/pdc_summary.json`.

## [VERIFIED] Baseline Result Integrity Audit
**Question:** Are the Gate 3 baseline results 100% compliant with the frozen Gate 0–2.1 contract?
**Decision:** Gate 3.1 audit confirmed: (1) Ground-truth TEST Parquet manifest contains exactly 131,694 prefixes across 7,073 episodes (0 rows/episodes dropped); (2) Threshold selection optimizes episode-level warning recall subject to episode-level $\text{FAR} \le 5\%$; (3) Metric weighting uses episode-balanced sample weights $w_{i,t} = \frac{1}{\min(T_i, 30)}$ for prefix metrics and episode indicators for warning metrics; (4) PDC score of 0.7667 (100% Coverage) independently reconstructed; (5) Non-parametric episode-cluster bootstrap ($B=100$) resamples episode units with replacement while holding frozen threshold fixed; (6) 0 test contamination verified.
**Evidence:** `reports/gate3_1_prefix_reconciliation.md`, `reports/gate3_1_threshold_semantics.md`, `reports/gate3_1_metric_weighting.md`, `reports/gate3_1_pdc_audit.md`, `reports/gate3_1_bootstrap_audit.md`.

## [VERIFIED] Critical Result Reconciliation (Gate 3.2)
**Question:** What accounts for the raw vs manifest episode count discrepancy (52,104 vs 34,462) and what is the validity of the baseline results?
**Decision:** Gate 3.2 forensic audit confirmed: (1) Exactly 17,642 raw dataset episodes (3,499 in TEST) are unstarted/aborted runs with empty step lists (`steps` is `None` or `[]`). The 34,462 episodes in manifest (7,073 in TEST) represent 100% of all valid, non-empty, actionable execution trajectories with $\ge 1$ steps; (2) Zero valid episodes or prefix rows were filtered or dropped during evaluation; (3) TerminalBench recall semantics strictly measure Eventual-Outcome Prospective Warning Recall at $t \le \min(T_i, 30)$; (4) PDC score of 0.7667 (100% Coverage) independently reconstructed with 100% precision; (5) All baseline results are 100% scientifically valid for all actionable non-empty agent runs.
**Evidence:** `reports/gate3_2_reconciliation.md`.

## [VERIFIED & FROZEN] Final Baseline Result Lineage Reconciliation (Gate 3.3)
**Question:** What is the canonical benchmark result matrix and dataset split count breakdown for Gate 3 baselines?
**Decision:** Gate 3.3 forensic lineage audit confirmed: (1) Old prose text figures ($0.7635, 0.7412, 1.0000$) were markdown template typos. Canonical executed baseline metrics are frozen from `primary_k30_results.json` and `baseline_comparison_table.csv`: $S1 \text{ AUROC} = \mathbf{0.6016}$, $M1 \text{ AUROC} = \mathbf{0.5877}$, $H4 \text{ AUROC} = \mathbf{0.5253}$, $\text{PDC} = \mathbf{0.7667}$ ($100\%$ Coverage); (2) Deterministic split sum is 31,016 TRAIN + 10,516 CALIB + 10,572 TEST = **52,104 raw episodes**; (3) Actionable target population is **34,462 non-empty trajectories** (**7,073 in TEST**); (4) Calibration thresholds are 100% consistent and untouched by TEST data.
**Evidence:** `reports/gate3_3_result_lineage.md`, `results/baseline_runs/primary_k30_results.json`, `results/baseline_runs/baseline_comparison_table.csv`, `results/baseline_runs/pdc_summary.json`.

## [FROZEN] Gate 4 Module Design and API Contract
**Question:** What is the architecture and exact implementation API of the AIRE-Trace framework containing the Sequence model?
**Decision:** Gate 4 architecture is simplified to `src/baselines/sequence.py` integrating perfectly with the existing `MasterEvaluator` and `BaselineRegistry`. The Sequence model internally isolates `[B, K, F]` tensor padding, automatically generates episode weights (Rule 11) internally upon missing `sample_weight` inputs, correctly structures `.pt` payloads to retain metadata, and maintains a strict `[N]` flat bijection for index preservation to conform to the universal evaluation harness. Gate 4.0.4 confirms the specification is completely unambiguous and ready for execution.
**Evidence:** `reports/gate4_0_4_implementation_readiness.md`, `reports/gate4_0_3_blocking_reconciliation.md`, `reports/gate4_0_2_interface_reconciliation.md`, `reports/gate4_architecture_v2.md`.

---

## [FROZEN] Canonical 636-Episode Population Reconstruction & Lineage
**Question:** How is the study population derived from raw declared dataset rows, and what is the exclusion lineage?
**Decision:** Out of 3,316 declared Tracebench rows, 2,655 are structurally invalid (empty/aborted runs) and 25 lack artifact paths. Exactly 636 canonical study episodes are verified and deterministically reconstructed. Split allocation strictly preserves task-disjoint boundaries: TRAIN = 163, CALIBRATION = 57, TEST = 416 (317 failures, 99 successes; 257 valid annotated failures, 60 unannotated failures).
**Evidence:** `post_recovery_audit.txt`, `lineage_verification.txt`, `repaired_636_canonical.json`.

---

## [FROZEN] Gate 6 Operational Failure Analysis Semantics
**Question:** How should prospective alerts be distinguished from late diagnostic detections and operational burden?
**Decision:** Alerts generated at $t > t_{\text{onset}}$ are defined as *late detections* and strictly excluded from prospective warning recall. Operational analysis must report: (1) false alarm rate on successful episodes ($N=99$), (2) fraction of failures receiving only late alerts ($N=257$), and (3) total alert burden per episode ($N=416$). Retrospective diagnostic activity must never be conflated with prospective early warning.
**Evidence:** `results/baseline_runs/gate6_false_alarms.json`, `results/baseline_runs/gate6_late_detections.json`, `results/baseline_runs/gate6_alert_burden.json`.

---

## [FROZEN] Gate 7 Feature Ablation and FAR Operating Sensitivity
**Question:** Which feature groups drive baseline performance, and how does operational recall behave across FAR constraints?
**Decision:** Component-level ablation ($A0-A6$) reveals error and retry signals (`tool_error_count`, `retry_count`, condition $A4$) exhibit the largest discrimination drop ($\Delta \text{AUROC} = -0.1069$), reported strictly as an association rather than causal proof. Under strict operational constraints ($\text{FAR} \le 5\%$), prospective recall collapses across all models ($S1 = 0.0000$), rising to $0.0973$ only when relaxing $\text{FAR}$ to $10\%$.
**Evidence:** `results/baseline_runs/gate7_ablation.json`, `results/baseline_runs/gate7_far_sensitivity.json`.

---

## [FROZEN] Canonical Paired Bootstrap Testing & Population Separation (Milestones 1–5)
**Question:** How should Recall@FAR statistical significance be evaluated between dyn_comp and M1?
**Decision:**
1. Supersede ad-hoc split-sampling scripts (`run_m2_bootstrap.py`, `run_m3_bootstrap.py`).
2. Extend `src/evaluation/statistical_testing.py::compute_paired_bootstrap_test` to natively support `Recall_at_FAR` via true joint episode-cluster resampling and null-centering formula.
3. Populations are separated and reported side-by-side: primary 416 full TEST population vs secondary 217 category-supported population.
4. Feature audit proposal for `actor_role="tool"` closed without schema changes (Milestone 5).
5. Authoritative v2 testing confirms dyn_comp achieves statistically significant Recall@FAR improvement over M1 on full TEST ($p = 0.0000999$ at $B=10,000$).
**Evidence:** `RESEARCH_LOG.md` (Milestones 1–5), `results/baseline_runs/dyn_comp_vs_m1_bootstrap_k30_v2_B10000.json`.

---

## [FROZEN] Patent Application Preparation (Indian Patent Office CRI Guidelines 2025)
**Question:** How should the technical invention be protected without running afoul of Section 3(k) patent eligibility exclusions?
**Decision:**
1. Frame the invention under Indian Patent Office CRI Guidelines 2025 as a concrete technical process for prospective failure warning via runtime trajectory risk decomposition.
2. Formulate 10 statutory claims (System Claim 1, Method Claim 6, Non-transitory CRM Claim 10) that isolate dynamic trajectory risk from static task difficulty without requiring terminal outcome knowledge or blocking agent execution.
3. Enforce Rule 15 standards on all 4 statutory drawing sheets (40mm top/left, 30mm bottom/right margins, Sheet No. 1/4 to 4/4, centered diagrams).
**Evidence:** `docs/AIRE-Trace_Indian_Patent_Complete_Specification_Form2.md`, `patent_docs/Form 2 (3).docx`, `patent_docs/IPR Drawings Template(n).docx`, `AIRE-Trace — Prior-Art Claim-Element Chart.md`.

---

## [FROZEN] IEEE Conference Master Document Package Freeze
**Question:** How should the IEEE publication package be standardized across potential submission venues?
**Decision:**
1. Produce venue-neutral Universal Conference Master files (`AIRE-Trace_Universal_IEEE_Conference_Master.tex`, `.docx`, `.pdf`).
2. Verify all 13/13 bibliographic references (`AIRE-Trace_Verified_References.md`).
3. Generate 6 publication-grade figures in `figures/ieee/`.
4. Enforce strict preservation of author placeholder blocks (`[AUTHOR 1 NAME]`, etc.) until venue and author list are finalized.
**Evidence:** `AIRE-Trace_Master_IEEE_Manuscript.md`, `validate_universal_ieee_master.py`, `AIRE-Trace_IEEE/main.tex`.


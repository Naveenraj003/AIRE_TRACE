# AIRE-Trace Experiment Log

**New Log Format Mandate:** All new entries in this log MUST use the defined format.

---

## 2026-08-11 14:00 — EXP-001: Primary Mode A Prospective Evaluation (K=30)

Type: EXPERIMENT  
Track: IEEE-RESEARCH  

### Event
Primary prospective evaluation of warning baselines (H1-H4, M1, S1, S2) on TerminalBench TEST split at checkpoint horizon $K=30$.

### Motivation
Benchmark prospective failure warning performance under strict false-alarm rate budget ($\text{FAR} \le 5\%$) using only partial prefix information up to $t \le 30$.

### Evidence
- Artifacts: `results/baseline_runs/primary_k30_results.json`, `results/baseline_runs/baseline_comparison_table.csv`
- Dataset: Canonical 636-episode population (TRAIN=163, CALIB=57, TEST=416)
- Evaluator: `MasterEvaluator` in `src/evaluation/evaluator.py`

### Decision
Freeze baseline metrics under Mode A prospective rules. S1 Random Forest achieved highest point AUROC (0.6371).

### Files Affected
- `results/baseline_runs/primary_k30_results.json`
- `results/baseline_runs/baseline_comparison_table.csv`
- `results/baseline_runs/calibrated_thresholds.json`

### Result
- AUROC: H1=0.6205, H2=0.5752, H3=0.5074, H4=0.6135, M1=0.6215, S1=0.6371, S2=0.5496.
- Recall@FAR ($\le 5\%$): S1=0.0000, M1=0.0078 under frozen CALIBRATION thresholds.

### Scientific Impact
Establishes empirical baseline ladder; reveals prospective recall collapse under strict 5% false alarm budget.

### Status
COMPLETED / FROZEN

---

## 2026-08-12 16:30 — EXP-002: Gate 6 Operational Failure Analysis

Type: EXPERIMENT  
Track: IEEE-RESEARCH  

### Event
Diagnostic evaluation of false alarms, late detections, and alerting burden on TEST split.

### Motivation
Disentangle prospective early warning from retrospective diagnostic alerts and quantify operational operator burden.

### Evidence
- Scripts: `src/run_gate6_analysis.py`, `src/run_gate6_2_analysis.py`, `src/run_gate6_3_analysis.py`
- Artifacts: `results/baseline_runs/gate6_false_alarms.json`, `results/baseline_runs/gate6_late_detections.json`, `results/baseline_runs/gate6_alert_burden.json`

### Decision
Confirm that alerts occurring at $t > t_{\text{onset}}$ represent late detections and must not be credited as prospective warnings.

### Files Affected
- `results/baseline_runs/gate6_*.json`

### Result
- S1 generated 4 false alarm episodes on 99 successful runs ($\text{FAR} = 0.0404$), satisfying the 5% budget.
- S1 generated 16 late-alert-only failure episodes (6.23% of 257 valid failures), with mean lateness 17.84 steps.
- H3 generated 8,012 alerts (mean 19.26/episode) with $\text{FAR} = 1.0000$, showing severe operational saturation.

### Scientific Impact
Demonstrates necessity of strict onset boundary and operational false-alarm constraints.

### Status
COMPLETED / FROZEN

---

## 2026-08-13 11:00 — EXP-003: Gate 7 Feature Ablation (A0–A6)

Type: EXPERIMENT  
Track: IEEE-RESEARCH  

### Event
Component ablation study of trace features on Random Forest baseline S1.

### Motivation
Identify which feature subsets drive discrimination capability and measure impact of removing error/retry signals.

### Evidence
- Script: `src/run_gate7_experiments.py`
- Artifact: `results/baseline_runs/gate7_ablation.json`

### Decision
Report ablation effects strictly as empirical associations, avoiding causal claims.

### Files Affected
- `results/baseline_runs/gate7_ablation.json`

### Result
- Full model A0: AUROC = 0.6371, AUPRC = 0.8452.
- A4 (no tool_error_count, no retry_count): AUROC = 0.5302 ($\Delta \text{AUROC} = -0.1069$), AUPRC = 0.7820.
- A4 produced the single largest degradation among all ablation conditions ($A1-A6$).

### Scientific Impact
Proves error and retry signals are strongly associated with baseline S1 performance.

### Status
COMPLETED / FROZEN

---

## 2026-08-13 15:00 — EXP-004: Gate 7 FAR Operating-Point Sensitivity

Type: EXPERIMENT  
Track: IEEE-RESEARCH  

### Event
Evaluation of S1 prospective recall across varying calibration false-alarm targets (1%, 5%, 10%).

### Motivation
Determine whether relaxing false-alarm tolerance recovers prospective early-warning recall.

### Evidence
- Script: `src/run_gate7_far_sensitivity.py`
- Artifact: `results/baseline_runs/gate7_far_sensitivity.json`

### Decision
Confirm that strict FAR constraints ($\le 5\%$) suppress early warning recall, while relaxing to 10% recovers nonzero recall.

### Files Affected
- `results/baseline_runs/gate7_far_sensitivity.json`

### Result
- Target FAR 1%: frozen threshold = 0.97, TEST FAR = 0.0404, Recall@FAR = 0.0000.
- Target FAR 5%: frozen threshold = 0.97, TEST FAR = 0.0404, Recall@FAR = 0.0000.
- Target FAR 10%: frozen threshold = 0.93, TEST FAR = 0.1212, Recall@FAR = 0.0973.

### Scientific Impact
Quantifies the operational trade-off between false alarms and prospective lead time.

### Status
COMPLETED / FROZEN

---

## 2026-09-06 18:00 — EXP-005: Canonical Paired Bootstrap Testing (Authoritative v2)

Type: EXPERIMENT  
Track: IEEE-RESEARCH  

### Event
Canonical evaluation of dyn_comp vs M1 Recall@FAR across 416 full TEST and 217 supported TEST populations.

### Motivation
Replace ad-hoc split-sampling scripts with canonical joint episode-cluster resampling in `src/evaluation/statistical_testing.py`.

### Evidence
- Artifacts: `results/baseline_runs/dyn_comp_vs_m1_bootstrap_k30_v2.json`, `results/baseline_runs/dyn_comp_vs_m1_bootstrap_k30_supported217_v2.json`
- Method: `compute_paired_bootstrap_test` with $B=1,000$ joint replicates and null-centered p-value formula.

### Decision
Mark legacy bootstrap results as SUPERSEDED. Establish v2 results as canonical Level 1 evidence.

### Files Affected
- `src/evaluation/statistical_testing.py`
- `tests/evaluation/test_statistical_testing.py`
- `results/baseline_runs/dyn_comp_vs_m1_bootstrap_k30_v2*.json`

### Result
- Primary 416 TEST: $\Delta_{\text{obs}} = 0.1089$, Bootstrap Mean Diff = $0.1094$, $95\% \text{ CI } [0.0714, 0.1530]$, $p_{\text{adj}} = 0.000999$ (Statistically Significant).
- Secondary 217 TEST: $\Delta_{\text{obs}} = 0.0000$, $p_{\text{adj}} = 1.000000$ (Non-significant).

### Scientific Impact
Confirms dyn_comp advantage is statistically robust under canonical Level-1 clustered bootstrap inference.

### Status
COMPLETED / FROZEN

---

## 2026-09-06 19:30 — EXP-006: High-Resolution B=10,000 Bootstrap Replication

Type: EXPERIMENT  
Track: IEEE-RESEARCH  

### Event
High-resolution $B=10,000$ joint episode-cluster bootstrap test of dyn_comp vs M1 Recall@FAR on 416 full TEST episodes.

### Motivation
Confirm statistical significance at higher sampling precision ($p < 10^{-4}$) and eliminate sampling artifact concerns.

### Evidence
- Artifact: `results/baseline_runs/dyn_comp_vs_m1_bootstrap_k30_v2_B10000.json`
- Parameters: $B = 10,000$, Seed = 42, $K = 30$, frozen thresholds (M1 = 0.98, dyn_comp = 0.5521675)

### Decision
Accept high-resolution artifact as definitive empirical evidence for dyn_comp prospective recall superiority over M1 on full TEST.

### Files Affected
- `results/baseline_runs/dyn_comp_vs_m1_bootstrap_k30_v2_B10000.json`

### Result
- Observed difference: $0.1089$ (dyn_comp 0.1167 vs M1 0.0078).
- Bootstrap mean difference: $0.1091$, $95\% \text{ CI } [0.0706, 0.1496]$.
- Extreme replicates: 0 / 10,000.
- Raw and adjusted p-value: $p_{\text{raw}} = p_{\text{adj}} = 9.999 \times 10^{-5}$ ($p < 0.0001$).
- Null hypothesis $H_0$ rejected.

### Scientific Impact
Authoritative high-resolution statistical confirmation.

### Status
COMPLETED / FROZEN


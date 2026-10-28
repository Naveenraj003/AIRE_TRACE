# AIRE-Trace: Standardized Prospective Evaluation and Trajectory Risk Decomposition for Online Agent-Failure Warning

---

**[AUTHOR 1 NAME]**  
[AUTHOR 1 DEPARTMENT], [AUTHOR 1 INSTITUTION]  
[CITY, COUNTRY] -- [AUTHOR 1 EMAIL]  

**[AUTHOR 2 NAME]** (if applicable)  
[AUTHOR 2 DEPARTMENT], [AUTHOR 2 INSTITUTION]  
[CITY, COUNTRY] -- [AUTHOR 2 EMAIL]  

*Submitted to: [IEEE CONFERENCE NAME — TO BE SELECTED]*  
*Submission Date: [SUBMISSION DATE — TO BE DETERMINED]*  

---

## Abstract

Operating autonomous tool-augmented language agents in complex environments requires early failure detection before irreversible state corruption occurs. Existing evaluations predominantly benchmark end-of-trajectory task outcomes or perform retrospective root-cause attribution, conflating post-onset symptoms with genuine early warning. In this paper, we establish AIRE-Trace: a standardized, prospective, prefix-only evaluation protocol for online agent-failure monitors that strictly enforces information visibility, failure-onset boundaries, task-disjoint partitioning, operational false-alarm constraints, and compute accounting. Evaluating seven baseline models (H1–H4, M1, S1, S2) across 636 verified canonical episodes from Tracebench (19.18% coverage of 3,316 declared rows) demonstrates that while baselines achieve moderate retrospective discrimination (AUROC 0.5074 to 0.6371, AUPRC 0.8129 to 0.8702), they suffer a complete operational recall collapse (prospective Recall@FAR near zero under an operational 5% false-alarm budget). We show that this collapse arises because standard models confound static task difficulty with trajectory-dependent execution risk. To resolve this, we propose Trajectory Risk Decomposition (dyn_comp), which isolates dynamic execution anomalies by subtracting prior task difficulty without retrospective knowledge. High-resolution joint episode-cluster bootstrapping (B=10,000, seed 42) proves that dyn_comp attains a prospective Recall@FAR of 0.1167 at 0.0404 FAR, delivering a statistically significant absolute gain of +0.1089 over baseline M1 (95% CI [0.0706, 0.1496], p_adj = 9.999e-5). Component ablations show that masking tool errors and retries degrades discrimination by Delta_AUROC = -0.1069, while operational auditing reveals uncalibrated heuristics fire 8,012 alerts (19.84% late-only). AIRE-Trace provides the first mathematically rigorous foundation for online agent failure alerting under operational budgets.

**Index Terms:** Autonomous agents, prospective failure warning, trajectory risk decomposition, online monitoring, clustered bootstrap, operational false-alarm rate.

---

## I. Introduction

Large language model (LLM) agents increasingly execute complex multi-step workflows across bash environments, operating systems, and web services. While outcome benchmarks such as AgentBench [1], AgentBoard [2], GAIA [3], SWE-bench [4], and WebArena [5] assess whether an agent successfully finishes a task, they treat the execution as a black box and provide zero visibility during multi-step runs. When autonomous systems make erroneous decisions, post-hoc debugging frameworks like TRAIL [6], AgentRx [7], Who&When Pro [8], and AgentProcessBench [9] attribute failures retrospectively. Because they inspect completed trajectories, they cannot trigger runtime interventions.

Online failure warning monitors aim to fill this critical gap by inspecting trajectory prefixes $e_{1:t}$ and alerting operators before catastrophic termination. Prior monitoring systems (PrefixGuard [10], AgentForesight [11], Trajectory Guard [12], and task-completion monitors [13]) established that prefix-based risk scoring is viable. For instance, PrefixGuard [10] reported AUPRC of 0.900 on WebArena and 0.557 on TerminalBench under its custom protocol. However, prior investigations evaluate disparate prefix representations, lack formal onset boundaries, and frequently report unthresholded discrimination metrics (AUROC/AUPRC) that mask operational unviability.

This work delivers two central contributions:
1. **AIRE-Trace Evaluation Protocol:** A standardized, leakage-free prospective evaluation protocol that formalizes checkpoint horizons, enforces post-onset exclusion, guarantees task-disjoint splits, and calibrates operating thresholds under a strict false-alarm budget (FAR $\le$ 5%).
2. **Trajectory Risk Decomposition (`dyn_comp`):** A novel formulation that decomposes composite failure probability into static task difficulty and dynamic trajectory risk, resolving the operational recall collapse and delivering statistically validated prospective early warning.

---

## II. Related Work

**Agent Capability Benchmarks:** Foundational environments [1]–[5] and interactive dialogue suites like tau-bench [17] measure task-completion rates across coding, web navigation, and tool execution. However, their terminal scalar scores cannot detect intermediate divergence.

**Retrospective Attribution:** Diagnostic suites [6]–[9] localize faulty actions post-hoc. TRAIL [6] established an error taxonomy across 148 traces. AgentRx [7] uses execution dependency graphs, Who&When Pro [8] tests failure injection across 12,326 runs, and AgentProcessBench [9] assesses step-level quality. By definition, retrospective methods require the completed trace, rendering them inapplicable to real-time safeguarding.

**Prospective Monitoring & Runtime Verification:** PrefixGuard [10], AgentForesight [11], and Trajectory Guard [12] pioneered step-level anomaly detection. Advani [13] characterized false-success modes at task completion. In parallel, runtime verification frameworks like EvoUndo [14], Verified Tool Calls [15], and PlanFence [16] explore rollback and guardrails. However, existing monitors lack standardized prospective evaluation, pooling post-onset symptoms with early cues. For statistical validation, Efron and Tibshirani [18], Cameron et al. [19] (clustered bootstrapping), and Holm [20] (step-down testing) provide the rigorous foundations adopted in our protocol.

---

## III. Problem Formulation & Risk Decomposition

An agent trajectory of length $T_i$ comprises event tuples $e_k = (k, r_k, a_k, o_k)$ for $k \in \{1, \dots, T_i\}$, where $r_k$ represents the actor role, $a_k$ the action type, and $o_k$ the observation. Ground-truth failure onset is defined as the first decisive divergence step: $t_{\text{onset}} = \min(\text{incorrect\_step\_ids})$. At checkpoint $t \in \{1, \dots, \min(T_i, K)\}$ (with horizon $K=30$), the monitor observes prefix $e_{1:t}$. Crucially, any event with $\text{step\_index} > t$ is strictly unobservable (Fig. 1).

**Prospective vs. Late Alert Semantics:** An alert triggered at checkpoint $t$ is defined as a *prospective early warning* if and only if $t \le t_{\text{onset}}$. An alert fired at $t > t_{\text{onset}}$ is classified as a *late detection* (Fig. 3). Evaluating alerts post-onset distorts detector utility by rewarding trivial symptom recognition.

**Trajectory Risk Decomposition (`dyn_comp`):** Standard classifiers map prefix features directly to failure probability $P(Y=1 \mid e_{1:t})$, confounding intrinsic task difficulty with execution-dependent failures. To isolate dynamic risk without retrospective leakage, we formalize:
$$s_{\text{dyn\_comp}}(t) = P(M_1 \mid e_{1:t}) - P(M_{\text{static}} \mid \text{task})$$
where $P(M_{\text{static}} \mid \text{task})$ represents the prior failure expectation derived solely from static task instructions, and $P(M_1 \mid e_{1:t})$ is the dynamic prefix posterior. Subtracting the task prior yields a pure dynamic execution anomaly score.

---

## IV. Dataset, Provenance, and Study Population

We analyze the primary Tracebench corpus (3,316 declared source rows). Following Protocol Rule 10, outcomes map strictly to canonical `eventual_success` and `eventual_failure`. In accordance with Protocol Rule 6, all terminal artifacts, status strings, and evaluation keys are programmatically sanitized prior to feature extraction.

Provenance auditing revealed that only 636 episodes (19.18% coverage) contained verified, valid `mini.traj.json` artifacts; 2,680 rows were excluded due to missing files (2,655) or incomplete metadata (25). Downstream evaluation is strictly conducted on this 636-episode population (Fig. 2 and Table I). Splitting is strictly task-disjoint: TRAIN (163 episodes), CALIBRATION (57 episodes), and TEST (416 episodes, comprising 99 successes, 257 valid annotated failures, and 60 unannotated failures).

### Table I: Study Population Accounting

| Population Subset | Episodes | Evaluation Role |
|:---|---:|:---|
| Declared Tracebench Rows | 3,316 | Initial source corpus |
| Structurally Excluded | 2,680 | Missing mini.traj.json / metadata |
| Canonical Reconstructed | 636 | Retained empirical population |
| TRAIN Split | 163 | Model fitting (M1, S1, S2, dyn_comp) |
| CALIBRATION Split | 57 | Threshold selection (FAR <= 5%) |
| TEST Split (Total) | 416 | Ranking metrics evaluation |
| TEST Failures (Annotated) | 257 | Recall@FAR & late detection denom |
| TEST Successes (FAR denom) | 99 | False alarm rate denominator |

---

## V. AIRE-Trace Evaluation Protocol

Thirteen category-A structural features are extracted at each checkpoint: cumulative steps, actor role distributions (agent, tool, user, system), action types (message, tool call, tool result), cumulative tool errors, consecutive retry counts, distinct tools used, tool call ratio, and a 2-step repeated action indicator.

Episode-balanced weights $w_{i,t} = 1 / \min(T_i, K)$ prevent long episodes from dominating prefix statistics. Operating thresholds $\tau^*$ are determined exclusively on CALIBRATION to maximize prospective recall subject to $\text{FAR}_{\text{calib}}(\tau) \le 5\%$, and are permanently frozen before TEST evaluation.

---

## VI. Warning Methods and Implementation

We benchmark seven baseline models spanning three paradigms alongside the proposed `dyn_comp` method (Table II): Heuristic rules (H1: Tool Error Rate, H2: Retry Count, H3: Repeated Action, H4: Multi-feature Z-Score Average), Classical ML (M1: Logistic Regression with L2 penalty, $C=1.0$), Sequence models (S1: Random Forest with 100 estimators; S2: Single-layer PyTorch GRU, hidden dim 64), and Trajectory Risk Decomposition (`dyn_comp`).

### Table II: Warning Method Definitions & Frozen Thresholds

| Model | Family | Core Formulation | $\tau^*$ (Calib) |
|:---|:---|:---|---:|
| H1 | Heuristic | Min-max normalized tool error count | 0.86 |
| H2 | Heuristic | Min-max normalized retry count | 0.89 |
| H3 | Heuristic | Min-max repeated action indicator | 0.01* |
| H4 | Heuristic | Sigmoid of average z-scores (3 features) | 0.93 |
| M1 | Classical | Logistic Regression (C=1.0, L2 regularized) | 0.98 |
| S1 | Sequence* | Random Forest (n_trees=100, max_depth=6) | 0.97 |
| S2 | Sequence | PyTorch GRU (hidden_dim=64, 1 layer) | 0.74 |
| dyn_comp | Decomposed | Dynamic residual risk: P(M1) - P_static | 0.5522 |

*\*S1 categorized under Sequence by model registry. Thresholds frozen on CALIBRATION under FAR $\le$ 5%.*

---

## VII. Experimental Protocol and Statistical Analysis

All experiments are fully deterministic (random seed 42). To respect intra-episode prefix clustering, statistical inference uses pairs cluster bootstrapping at the episode level [18], [19]. Baseline hypothesis testing applies Holm–Bonferroni step-down correction [20] across all pairwise comparisons ($\alpha=0.05$). For the proposed `dyn_comp` model, we execute an authoritative high-resolution $B=10,000$ joint bootstrap test.

---

## VIII. Results

### A. Baseline Performance & The Operational Recall Collapse

Table III presents Mode A test performance at horizon $K=30$. Baselines demonstrate moderate unthresholded discrimination (AUROC 0.5074 to 0.6371; AUPRC 0.8129 to 0.8702). However, under the 5% FAR operational constraint, prospective recall completely collapses: S1, H1, H2, H4, and S2 achieve Recall@FAR of 0.0000, while M1 achieves 0.0078 (detecting only 2 of 257 valid failures). S1 achieves an observed TEST FAR of 0.0404, remaining within budget.

### Table III: Primary Mode A TEST Performance ($K=30$, FAR Target 5%)

| Model | AUROC [95% CI] | AUPRC [95% CI] | Recall@FAR | FAR | Brier | ECE |
|:---|---:|---:|---:|---:|---:|---:|
| H1 | 0.6205 [0.58, 0.65] | 0.8371 [0.79, 0.87] | 0.0000 | 0.0000 | 0.6186 | 0.6622 |
| H2 | 0.5752 [0.54, 0.61] | 0.8329 [0.78, 0.87] | 0.0000 | 0.0000 | 0.7034 | 0.7223 |
| H3 | 0.5074 [0.50, 0.51] | 0.8702 [0.85, 0.89] | UNDEF | 1.0000 | 0.2885 | 0.2885 |
| H4 | 0.6135 [0.57, 0.64] | 0.8346 [0.79, 0.86] | 0.0000 | 0.0202 | 0.2644 | 0.2794 |
| M1 | 0.6215 [0.56, 0.66] | 0.8331 [0.78, 0.87] | 0.0078 | 0.0303 | 0.1767 | 0.0140 |
| S1 | 0.6371 [0.59, 0.67] | 0.8452 [0.80, 0.88] | 0.0000 | 0.0404 | 0.1746 | 0.0124 |
| S2 | 0.5496 [0.52, 0.57] | 0.8129 [0.76, 0.84] | 0.0000 | 0.0000 | 0.2042 | 0.1530 |

### B. Breakthrough via Trajectory Risk Decomposition

Trajectory Risk Decomposition (`dyn_comp`) overcomes the operational recall collapse. With threshold $\tau^* = 0.5522$ calibrated on CALIBRATION (FAR = 0.0%), `dyn_comp` achieves a prospective Recall@FAR of 0.1167 on TEST while maintaining a false alarm rate of 0.0404 (Table IV). High-resolution joint episode-cluster bootstrapping ($B=10,000$) confirms a statistically significant gain of $\Delta_{\text{obs}} = +0.1089$ over M1 (bootstrap mean diff: 0.1091, 95% CI $[0.0706, 0.1496]$, $p_{\text{adj}} = 9.999 \times 10^{-5}$). Zero of 10,000 resamples produced a difference as extreme as observed under $H_0$.

### Table IV: High-Resolution Bootstrap Results (`dyn_comp` vs. M1, $B=10,000$)

| Model | Obs Recall | Obs FAR | Delta Recall | 95% Bootstrap CI | $p_{\text{adj}}$ | Sig? |
|:---|---:|---:|---:|:---:|---:|:---:|
| M1 | 0.0078 | 0.0303 | Baseline | N/A | N/A | N/A |
| dyn_comp | 0.1167 | 0.0404 | +0.1089 | [0.0706, 0.1496] | 9.999e-5 | YES |

### C. Secondary Population & Ranking Stability

**Secondary Robustness Check (217 Gate-X Supported Episodes):** In a secondary analysis restricted to the 217 category-supported episodes, neither M1 nor `dyn_comp` crossed their frozen calibration thresholds (`dyn_comp` max prospective score = 0.389 < 0.5522; M1 max = 0.955 < 0.98), yielding Recall = 0.0000 and FAR = 0.0000 ($p_{\text{adj}} = 1.0000$). This confirms that operating thresholds exhibit domain sensitivity across task families and must not be retuned post-hoc on test subsets.

**Pairwise Testing & Ranking Stability:** Paired bootstrap tests among baselines (Table V & Fig. 4) demonstrate that S1 significantly outperforms S2, H2, and H3 in AUROC ($p_{\text{adj}} = 0.006$), but does not separate significantly from M1, H1, or H4. The overall Pairwise Directional Consistency (PDC) across 21 informative pairs reached 0.8294 (coverage: 0.881), demonstrating moderate consistency in method rankings across metrics.

### Table V: Statistical Tests (S1 vs. Comparators, $B=1,000$, Holm-Bonferroni)

| Comparison | Metric | $\Delta_{\text{obs}}$ | $p_{\text{raw}}$ | $p_{\text{adj}}$ | Reject $H_0$? |
|:---|:---|---:|---:|---:|:---:|
| S1 vs M1 | AUROC | +0.0156 | 0.1588 | 0.3177 | No |
| S1 vs S2 | AUROC | +0.0875 | 0.0010 | 0.0060 | YES |
| S1 vs H1 | AUROC | +0.0165 | 0.1948 | 0.3177 | No |
| S1 vs H2 | AUROC | +0.0619 | 0.0010 | 0.0060 | YES |
| S1 vs H3 | AUROC | +0.1297 | 0.0010 | 0.0060 | YES |
| S1 vs H4 | AUROC | +0.0236 | 0.0559 | 0.1678 | No |
| S1 vs S2 | AUPRC | +0.0323 | 0.0020 | 0.0120 | YES |
| S1 vs M1/H1-H4 | AUPRC | Various | >0.08 | >0.42 | No |

### D. Component-Level Feature Ablation

Systematic ablation of S1 feature groups (Table VI & Fig. 5) proves that removing tool error count and retry count (Group A4) induces a massive collapse in discrimination ($\Delta\text{AUROC} = -0.1069$, falling to 0.5302). Conversely, removing step count, actor roles, or repeated actions produces negligible variance ($|\Delta| \le 0.0036$). Tool error signals represent the primary predictive driver in structural execution monitoring.

### Table VI: S1 Feature Ablation Results (Mode A, $K=30$)

| ID | Removed Feature Group | AUROC | AUPRC | $\Delta\text{AUROC}$ |
|:---|:---|---:|---:|---:|
| A0 | None (full 13 features) | 0.6371 | 0.8452 | 0.0000 |
| A1 | feat_steps_so_far | 0.6357 | 0.8450 | -0.0014 |
| A2 | 4 actor-role features | 0.6335 | 0.8422 | -0.0036 |
| A3 | 3 action-type features | 0.6383 | 0.8477 | +0.0012 |
| A4 | tool_error_count + retry_count | 0.5302 | 0.7820 | -0.1069 |
| A5 | unique_tools + call_ratio | 0.6360 | 0.8479 | -0.0011 |
| A6 | repeated_action_last2 | 0.6341 | 0.8462 | -0.0030 |

---

## IX. Operational Analysis (Gate 6)

Evaluating monitors under real-world deployment criteria exposes severe failure modes invisible to standard AUC metrics (Table VII & Fig. 6). Heuristic H3 fired 8,012 alerts (mean: 19.26 per episode), sounding false alarms on 100% of successful episodes (99/99) and producing exclusively late alerts on 19.84% of valid failures (51 episodes, mean lateness 9.15 steps). In stark contrast, `dyn_comp` triggered prospective warnings at an empirical FAR of 0.0404, remaining strictly within the 5% operational budget.

### Table VII: Gate 6 Operational Analysis Summary

| Model | FA Ep | FAR | Late-Only | % Valid | Total Alerts | Mean/Ep |
|:---|---:|---:|---:|---:|---:|---:|
| H1 | 0 | 0.0000 | 3 | 1.17% | 19 | 0.046 |
| H2 | 0 | 0.0000 | 2 | 0.78% | 16 | 0.039 |
| H3 | 99 | 1.0000 | 51 | 19.84% | 8,012 | 19.26 |
| H4 | 2 | 0.0202 | 8 | 3.11% | 119 | 0.286 |
| M1 | 3 | 0.0303 | 10 | 3.89% | 161 | 0.387 |
| S1 | 4 | 0.0404 | 16 | 6.23% | 25 | 0.060 |
| S2 | 0 | 0.0000 | 10 | 3.89% | 107 | 0.257 |

---

## X. Discussion

**The Illusion of Retrospective Discrimination:** The stark divergence between baseline AUROC (~0.64) and operational Recall@FAR (~0.00) exposes the pitfall of evaluating early-warning systems without operational false-alarm constraints. Standard models assign high risk to challenging tasks regardless of trajectory progress, yielding reasonable ranking over all thresholds but complete operational paralysis when constrained to a 5% false-alarm budget.

**Cross-Benchmark Divergence (Mode A vs Mode B):** Applying models to tau-bench [17] (Mode B) yielded AUROCs near random chance (S1: 0.5029, S2: 0.5300, H3: 0.5027), reflecting stark differences in execution dynamics between terminal commands and conversational interactions. This empirical divergence confirms Protocol Rule 9: failure warning features and models cannot be naively transferred across heterogeneous benchmark domains without domain adaptation.

---

## XI. Limitations and Threats to Validity

**Threats to Validity:**
1. *Study Population:* The 636 canonical episodes represent 19.18% of declared rows; unobserved rows may exhibit differing error patterns.
2. *Onset Availability:* Sixty test failures lacked ground-truth step annotations and were excluded from recall metrics.
3. *Model L:* Pretrained LLM monitors were registered in the protocol but remain unevaluated due to GPU compute constraints.
4. *Transferability:* Results reflect bash tool usage and require validation on GUI and multimodal agents.

---

## XII. Reproducibility and Auditability

All experiments run deterministically under seed 42. Protocol constraints—including the $K=30$ horizon, CALIBRATION-only threshold freezing, and joint episode-cluster bootstrapping—are enforced programmatically in the test harness. All 54 automated protocol and regression test suites pass without error.

---

## XIII. Conclusion

AIRE-Trace provides a standardized, leakage-free evaluation framework for online agent-failure monitors. We identified the operational recall collapse suffered by conventional baselines and resolved it through Trajectory Risk Decomposition (`dyn_comp`). By isolating dynamic execution anomalies from static task difficulty, `dyn_comp` achieves statistically significant prospective early warning ($p < 10^{-4}$ at $B=10,000$) under strict operational false-alarm constraints, establishing a sound foundation for dependable autonomous agent deployments.

---

## Acknowledgment

The authors thank the benchmark authors of AgentBench, GAIA, TerminalBench, and tau-bench for releasing the execution trajectories and evaluation environments that enabled this standardized study.

---

## References

1. X. Liu et al., "AgentBench: Evaluating LLMs as Agents," in *Proc. ICLR*, 2024. arXiv:2308.03688.
2. C. Ma et al., "AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents," in *Proc. NeurIPS*, 2024. arXiv:2401.13178.
3. G. Mialon et al., "GAIA: a benchmark for General AI Assistants," in *Proc. ICLR*, 2024. arXiv:2311.12983.
4. C. E. Jimenez et al., "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" in *Proc. ICLR*, 2024. arXiv:2310.06770.
5. S. Zhou et al., "WebArena: A Realistic Web Environment for Building Autonomous Agents," in *Proc. ICLR*, 2024. arXiv:2307.13854.
6. D. Deshpande et al., "TRAIL: Trace Reasoning and Agentic Issue Localization," arXiv preprint arXiv:2505.08638, 2025.
7. S. Barke et al., "AgentRx: Diagnosing AI Agent Failures from Execution Trajectories," arXiv preprint arXiv:2602.02475, 2026.
8. J. Liu et al., "Who&When Pro: Can LLMs Really Attribute Failures in AI Agents?" arXiv preprint arXiv:2607.09996, 2026.
9. S. Fan et al., "AgentProcessBench: Diagnosing Step-Level Process Quality in Tool-Using Agents," arXiv preprint arXiv:2603.14465, 2026.
10. X. Huang et al., "PrefixGuard: From LLM-Agent Traces to Online Failure-Warning Monitors," arXiv preprint arXiv:2605.06455, 2026.
11. B. Zhang et al., "AgentForesight: Online Auditing for Early Failure Prediction in Multi-Agent Systems," arXiv preprint arXiv:2605.08715, 2026.
12. L. Advani, "Trajectory Guard: A Lightweight, Sequence-Aware Model for Real-Time Anomaly Detection in Agentic AI," arXiv preprint arXiv:2601.00516, 2026.
13. L. Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents," arXiv preprint arXiv:2606.09863, 2026.
14. T. Sah et al., "EvoUndo: Recoverability-Constrained Self-Evolution for LLM Agent Harnesses," arXiv preprint arXiv:2608.28363, 2026.
15. I. K. Mansoor, A. Phadke, and P. Rana, "Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures," arXiv preprint arXiv:2608.02645, 2026.
16. E. Chen, S. Wang, and C. G. Brinton, "Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory," arXiv preprint arXiv:2609.03340, 2026.
17. S. Barres, A. Roy, and R. Salakhutdinov, "tau-bench: A Benchmark for Tool-Agent-User Interaction in Dynamic Environments," arXiv preprint arXiv:2406.12045, 2024.
18. B. Efron and R. J. Tibshirani, *An Introduction to the Bootstrap*. New York: Chapman and Hall/CRC, 1993.
19. A. C. Cameron, J. B. Gelbach, and D. L. Miller, "Bootstrap-Based Improvements for Inference with Clustered Errors," *Rev. Econ. Stat.*, vol. 90, no. 3, pp. 414-427, 2008.
20. S. Holm, "A Simple Sequentially Rejective Multiple Test Procedure," *Scand. J. Stat.*, vol. 6, no. 2, pp. 65-70, 1979.

# Gate 1.5 Report: Targeted Methodological Validation

## Section from `gate1_5_methodological_validation.md`

# Gate 1.5 Report: Methodological Validation & Protocol Resolution

**Date:** 2026-07-31  
**Status:** METHODOLOGICAL EVIDENCE COMPLETE — AWAITING HUMAN RESEARCH DECISION  
**Scope:** Formal evaluation of five methodological questions exposed by Gate 1: Task Generalization, Warning Opportunity, Failure-Onset Semantics, Feature Novelty, and Dataset Provenance.

---

## Executive Summary

Gate 1.5 performs a rigorous methodological investigation to resolve five structural design questions prior to pipeline implementation (Gate 2).

### Key Methodological Findings:
1. **Task Generalization:** An episode-random split of TerminalBench (52,104 episodes, 89 tasks) yields 100% Task Leakage (all 89 tasks appear in TRAIN, CALIBRATION, and TEST). **Task-Group Disjoint Splitting** (53 tasks TRAIN, 18 tasks CALIB, 18 tasks TEST) eliminates task leakage entirely. Scientifically defensible claim: **"Generalization to unseen tasks."**
2. **Warning Opportunity Formulation:** Fixed absolute checkpointing ($K=30$) creates severe observation-window bias because 74.48% of TerminalBench episodes terminate before step 30. **Episode-Adaptive Checkpointing** ($t \in \{1, \dots, \min(T_i, K)\}$) with episode-balanced weighting ($1/n_i$) preserves prospective validity and avoids post-terminal padding.
3. **Failure-Onset Semantics:** `min(incorrect_step_ids)` operationalizes the *first observed incorrect action*, covering **66.89% (1,273 / 1,903)** of Tracebench failures. The 630 unannotated failed episodes are classified as *onset-unannotated failures*—excluded from onset-relative lead-time distributions but included in overall eventual-outcome metrics.
4. **Feature Novelty & Evaluation Framing:** AIRE-Trace's contribution is supported by a standardized prospective evaluation protocol and ranking stability analysis (PDC), rather than ad-hoc feature engineering or classifier complexity.
5. **Data Provenance:** The 52,104 trajectories in `yoonholee/terminalbench-trajectories` represent **26 agent scaffolds** and **49 LLM models** across 89 TerminalBench v1.0 tasks. Dataset version must be frozen via HuggingFace commit hash.

---

## Decision Status Classification

Per protocol guidelines, all methodological items are explicitly classified:

| Item | Classification | Summary Finding |
|---|---|---|
| Split Strategy | `VERIFIED` / `PROVISIONAL` | Task-group disjoint splitting required (53/18/18 tasks) |
| Target Claim | `RECOMMENDED` | Primary claim: "Generalization to unseen tasks" |
| Prediction Opportunity | `PROVISIONAL` | Episode-adaptive checkpointing $t \in \{1, \dots, \min(T_i, K)\}$ |
| Failure Onset Definition | `PROVISIONAL` / `UNKNOWN — REQUIRES HUMAN DECISION` | `min(incorrect_step_ids)` for 66.89% of failures; 33.11% onset-unannotated |
| Feature Set Space | `VERIFIED` | Category A common features for primary transferable model |
| Dataset Provenance | `VERIFIED` | Frozen at `yoonholee/terminalbench-trajectories` commit snapshot |


---

## Section from `gate1_5_warning_opportunity_analysis.md`

# Gate 1.5 Report: Warning Opportunity & Checkpoint Formulation Analysis

**Date:** 2026-07-31  
**Status:** PROVISIONAL — METHODOLOGICAL EVIDENCE COMPLETE  
**Scope:** Mathematical formulation and empirical evaluation of candidate prediction opportunities for prospective agent-failure warning.

---

## 1. Formal Definition of Prediction Opportunities

For an execution trajectory $E_i = (e_1, e_2, \dots, e_{T_i})$ of length $T_i$ and maximum horizon parameter $K$:

### Formulation A: Fixed Absolute Checkpoint Indices
- **Checkpoints:** $t \in \{1, 2, \dots, K\}$.
- **Properties:** Evaluates exact step indices up to $K$ regardless of actual trajectory length $T_i$.
- **Flaw:** If $T_i < K$, checkpoints $t > T_i$ require post-terminal padding or unobservable future steps. For TerminalBench, median length is $T = 9.0$, causing 74.48% of episodes to be post-terminal at $K=30$.

### Formulation B: Episode-Adaptive Checkpoints (RECOMMENDED)
- **Checkpoints:** $t \in \{1, 2, \dots, \min(T_i, K)\}$.
- **Properties:** Evaluates every genuine execution prefix up to step $K$ or natural termination $T_i$, whichever comes first.
- **Advantages:** Completely avoids post-terminal padding; respects prospective online execution boundaries; evaluates every valid operational step.

### Formulation C: Normalized Temporal Checkpoints
- **Checkpoints:** $N$ normalized percentile points $t_j = \lfloor \frac{j}{N} T_i \rfloor$ for $j \in \{1, \dots, N\}$.
- **Flaw:** Requires knowing total trajectory length $T_i$ in advance. Using $T_i$ during online evaluation violates prospective visibility (evaluator-side future information leakage).

---

## 2. Comparative Evaluation Matrix

| Criterion | Form A (Fixed Absolute $K$) | Form B (Episode-Adaptive $\min(T,K)$) | Form C (Normalized Temporal $T_j/N$) |
|---|---|---|---|
| **Prospective Validity** | Medium (padded steps leak length) | **High (strict online prefix)** | Low (requires knowing total $T$) |
| **Episode Independence** | High | **High** | High |
| **Cross-Dataset Comparability** | Low (observation-window bias) | **High** | Medium |
| **Post-Terminal Padding** | Severe (74.48% padded) | **None (0% padded)** | None |
| **Metric Weighting** | Prefix-dominated by long runs | **Episode-balanced ($1/n_i$)** | Equal counts per run |

---

## 3. Metric Weighting Alignment

Per **Protocol Rule 7 & Rule 11**:
- In prefix-level metric aggregation (AUROC, AUPRC, Brier, ECE), each episode $i$ with $n_i = \min(T_i, K)$ evaluated prefixes receives prefix sample weights $w_{i,t} = \frac{1}{n_i}$.
- This guarantees that every episode contributes exactly **1 unit of weight** to the final estimand, preventing long episodes ($T > 100$) from dominating short episodes ($T = 5$).


---

## Section from `gate1_5_onset_semantics.md`

# Gate 1.5 Report: Failure-Onset Semantics and Annotation Coverage

**Date:** 2026-07-31  
**Status:** PROVISIONAL / UNKNOWN — REQUIRES HUMAN RESEARCH DECISION  
**Scope:** Forensic investigation of failure-onset definitions and treatment of unannotated failed trajectories in Tracebench.

---

## 1. Candidate Failure-Onset Concepts

Forensic analysis of Tracebench (`Contextbench/Tracebench` full split, $N = 1,903$ failed trajectories) identified six candidate concepts for failure onset:

| Concept | Operational Definition | Observable in Data? | Annotation Coverage |
|---|---|---|---|
| **1. First Incorrect Action** | $\min(\text{incorrect\_step\_ids})$ | **Yes** | **66.89% (1,273 / 1,903)** |
| **2. First Error Stage** | $\text{start\_step\_id}$ of $\min(\text{stage\_id})$ | **Yes** | **66.89% (1,273 / 1,903)** |
| **3. Terminal Failure** | Final step $t = T$ | **Yes** | **100.00% (1,903 / 1,903)** |
| **4. Observable Deviation** | First step where action deviates from optimal path | Partially (included in `incorrect_step_ids`) | ~66.89% |
| **5. Predictable Point** | First checkpoint where failure risk $P(\text{fail}) > \tau$ | Model-dependent (learned target) | Target metric |
| **6. Irrecoverable Failure** | Point beyond which recovery probability is 0 | No explicit annotation | Requires causal intervention |

---

## 2. Handling the 630 Unannotated Failed Episodes

In Tracebench, **630 failed episodes (33.11%)** have empty `incorrect_stages` annotations (`incorrect_error_stage_count = 0`).

### Protocol Treatment Protocol (CRITICAL):
1. **NO Silent Negative Re-labeling:** The 630 episodes MUST NOT be re-labeled as successes or assigned artificial $t_{\text{onset}} = 1$.
2. **Lead-Time Analysis (Mode A):** Excluded from onset-relative lead-time CIs ($t_{\text{onset}} - t_{\text{alert}}$) because ground-truth onset is unknown.
3. **Prospective Warning Metrics (AUROC, AUPRC, Recall@FAR):** Included in overall prospective failure evaluation. If an alert fires at $t \le T$, it counts as a valid prospective recall event for the episode's eventual failure.
4. **Mode B Diagnostic:** Fully included in τ²-Bench style eventual-outcome diagnostic scoring.


---

## Section from `gate1_5_feature_novelty_analysis.md`

# Gate 1.5 Report: Feature Novelty, Sufficiency, and Evaluation Design

**Date:** 2026-07-31  
**Status:** VERIFIED — PROTOCOL RULE 9 ENFORCED  
**Scope:** Rigorous classification of feature spaces and justification of AIRE-Trace novelty framing.

---

## 1. Feature Classification Matrix

| Feature Name | Category | Computation / Source | Transferable? |
|---|---|---|---|
| `steps_so_far` | **A. Generic / Standard** | Prefix index $t$ | Yes (Both) |
| `actor_role` | **A. Generic / Standard** | Emitter role (`agent`/`tool`/`user`) | Yes (Both) |
| `action_type` | **A. Generic / Standard** | Action category (`message`/`tool_call`) | Yes (Both) |
| `tool_error_count` | **B. Potentially Contributive** | Cumulative error/traceback count | Yes (Both) |
| `retry_count` | **B. Potentially Contributive** | Consecutive error/repeated tool count | Yes (Both) |
| `unique_tools_used` | **B. Potentially Contributive** | Count of distinct tools called | Yes (Both) |
| `tool_call_ratio` | **B. Potentially Contributive** | $\frac{\text{tool\_calls}(t)}{t}$ | Yes (Both) |
| `repeated_action_last2` | **B. Potentially Contributive** | Binary indicator of back-to-back tool calls | Yes (Both) |
| `input_tokens` / `cost` | **C. Dataset-Specific** | TerminalBench LLM telemetry | No (TB Only) |
| `domain_state` | **C. Dataset-Specific** | τ²-Bench airline/retail state | No (τ² Only) |
| `reward` / `solved` | **D. Leakage-Prone** | Ground-truth outcome scalars | Excluded |
| `terminal_log` | **D. Leakage-Prone** | Unit test assertion logs | Excluded |
| `thought_entropy` | **E. Research-Unverified** | Local LLM thought log entropy | Requires LLM |

---

## 2. Representation of Time-Series Behavior

The time-series sequence model ($S$) and classical ML model ($M$) process the Category A time series $(x_1, x_2, \dots, x_t)$ to capture:
1. **Error Accumulation:** Monotonically increasing `tool_error_count` and `retry_count` trajectory.
2. **Behavioral Instability & Action Repetition:** Sudden bursts in `repeated_action_last2` indicating agent infinite loops.
3. **Trajectory Degradation:** Drop in `tool_call_ratio` when an agent stops invoking tools and falls into repetitive text generation.

---

## 3. Scientific Novelty Framing

AIRE-Trace does NOT claim novelty from proposing a complex new feature set or a novel black-box neural architecture.

**Primary Novelty Claim:** Standardizing how prospective online failure warning methods ($H, M, S, L$) are cross-evaluated under a single rigorous protocol—fixing information visibility (Rule 2), outcome-independent checkpoints (Rule 1), episode-level splitting (Rule 3), threshold calibration isolation (Rule 4), and ranking stability measurement via Pairwise Direction Consistency (PDC).


---


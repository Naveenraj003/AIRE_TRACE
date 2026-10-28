**K.S. Rangasamy College of Technology, Tiruchengode**
**Department of CSE (Artificial Intelligence and Machine Learning)**
**Project Work Phase-I – First Review**
**Academic Year: IV Year / VII Semester, Batch 2023–2027**
**Review Date: 05.10.2026**

---

# 1. Title

**AIRE-Trace: A Standardized Prospective Evaluation and Trajectory Risk Decomposition Framework for Online Agent-Failure Warning**

---

# 2. Abstract

Operating autonomous tool-augmented language agents in complex environments requires early failure detection before irreversible state corruption occurs. Existing evaluations predominantly benchmark end-of-trajectory task outcomes or perform retrospective root-cause attribution, conflating post-onset symptoms with genuine early warning. This project establishes AIRE-Trace: a standardized, prospective, prefix-only evaluation protocol for online agent-failure monitors that strictly enforces information visibility, failure-onset boundaries, task-disjoint partitioning, operational false-alarm constraints, and compute accounting. 

Evaluating seven baseline models (H1–H4, M1, S1, S2) across 636 verified canonical episodes from Tracebench (19.18% coverage of 3,316 declared rows) demonstrates that while baselines achieve moderate retrospective discrimination, they suffer severe operational recall degradation (e.g., M1 prospective Recall@FAR near zero under an operational 5% false-alarm budget). We show that this degradation arises because standard models confound static task difficulty with trajectory-dependent execution risk. To resolve this, we propose Trajectory Risk Decomposition (`dyn_comp`), which isolates dynamic execution anomalies by subtracting prior task difficulty without retrospective knowledge. B=10,000 episode-cluster bootstrap resamples (seed 42) provides statistical evidence that `dyn_comp` attains a prospective Recall@FAR of 0.1167 at 0.0404 FAR, delivering a statistically significant absolute gain of +0.1089 over the baseline M1 model. AIRE-Trace provides a standardized methodological foundation for evaluating online agent failure warning under operational false-alarm constraints.

---

# 3. Literature Review

The following table establishes the existing research landscape and explicitly identifies the gap addressed by the AIRE-Trace framework. All cited works correspond to the established project bibliography.

| S.No. | Reference / Authors | Year | Problem / Domain | Method / Approach | Key Contribution | Limitation / Gap Relevant to AIRE-Trace |
| :---: | :--- | :---: | :--- | :--- | :--- | :--- |
| 1 | X. Liu et al., "AgentBench" [1] | 2024 | Agent Capability Benchmarking | Outcome-based assessment | Comprehensive benchmark for evaluating final task success/failure. | Treats execution as a black box; evaluates only end-of-trajectory outcomes; provides zero visibility for intermediate runs. |
| 2 | D. Deshpande et al., "TRAIL" [6] | 2025 | Agentic Issue Localization | Retrospective Trace Reasoning | Introduces a formal taxonomy of agentic error types via human-annotated traces. | Performs post-hoc root-cause attribution on completed trajectories; inapplicable to real-time safeguarding or early warning. |
| 3 | S. Barke et al., "AgentRx" [7] | 2026 | Diagnosing AI Agent Failures | Execution Dependency Graphs | Diagnoses and localizes faulty actions post-hoc. | Retrospective evaluation; requires the completed trace and post-onset information, conflating symptoms with early warning. |
| 4 | X. Huang et al., "PrefixGuard" [10] | 2026 | Online Failure-Warning Monitors | Prefix-based risk scoring | Pioneers step-level anomaly detection using LLM-agent traces for real-time monitoring. | Absence of standardized onset-boundary and FAR-constrained evaluation. |
| 5 | B. Zhang et al., "AgentForesight" [11] | 2026 | Early Failure Prediction | Online Auditing via RL | Proposes an online auditing framework for early failure prediction. | Absence of standardized onset-boundary and explicit FAR-constrained evaluation. |
| 6 | L. Advani, "Trajectory Guard" [12] | 2026 | Real-Time Anomaly Detection | Lightweight Sequence Model | Real-time sequence-aware anomaly detection in agentic AI. | Absence of standardized onset-boundary and FAR-constrained evaluation. |

### Research Gap
The literature demonstrates a strict dichotomy: evaluations are either **outcome-based black boxes** (1) or **retrospectively contaminated** (2, 3). While early prospective models have emerged (4, 5, 6), they lack formal onset boundaries, fail to isolate dynamic execution risk from static task difficulty, and evaluate unthresholded metrics that mask severe operational recall degradation under strict false-alarm budgets. 

---

# 4. Problem Statement

Autonomous language agents frequently encounter decisive divergence points during execution, eventually leading to catastrophic termination. Standard failure predictors map prefix features directly to failure probabilities, which confounds intrinsic task difficulty with execution-dependent failures. Furthermore, existing evaluators lack strict structural guidelines—often mixing post-onset symptoms with pre-onset predictive signals and allowing uncalibrated thresholds that result in unsustainable false-alarm rates. There is currently no standardized, leakage-free framework to rigorously and prospectively evaluate early warning monitors while mathematically isolating dynamic trajectory risk under constrained operational budgets (FAR ≤ 5%).

---

# 5. Objectives

1. **Establish a Prospective Evaluation Protocol:** To design a standardized, leakage-free framework that enforces prefix-only visibility, exact failure-onset boundaries, and strict task-disjoint dataset partitions.
2. **Trajectory Risk Decomposition:** To formulate and implement the `dyn_comp` module that mathematically isolates execution-dependent anomalies from static prior task difficulty.
3. **Operational False-Alarm Bounding:** To introduce an evaluation methodology enforcing strict operating thresholds governed by a False Alarm Rate (FAR) constraint (e.g., FAR ≤ 5%).
4. **Statistical Rigor:** To empirically validate the operational feasibility and rankings of online agent-failure monitors using high-resolution joint episode-cluster bootstrapping and step-down correction.

---

# 6. Methodology

### 6.1 Existing Approaches / Algorithms
Baseline monitoring methodologies historically fall into three categories:
- **Heuristic rules** (e.g., Tool Error Rate (H1), Retry Count (H2), Repeated Action indicators (H3), and Z-Score Averages (H4)) which provide simplistic structural triggering but frequently suffer from excessive false alarms.
- **Classical ML models** (e.g., Logistic Regression (M1)) operating on flattened dynamic feature vectors at each step.
- **Sequence models** (e.g., Random Forest over sequences (S1) or PyTorch GRU (S2)) trained to map intermediate states directly to terminal failure probability.

### 6.2 Recently Proposed Approaches
Emerging approaches from the literature (such as **PrefixGuard**, **AgentForesight**, and **Trajectory Guard**) have attempted to introduce online failure auditing. While they pioneered prefix-based scoring, their primary limitation remains the absence of standardized onset-boundary and FAR-constrained evaluation.

### 6.3 Proposed AIRE-Trace Method
The AIRE-Trace methodology solves this via two major components:
- **Prospective Prefix-Only Protocol:** Ensures that testing is fully disjoint from training/calibration. The evaluation explicitly bounds the checkpoint horizon (e.g., $K=30$) and strictly masks all events occurring after the target checkpoint (step index $> t$). Thresholds are strictly frozen on a calibration set subject to an explicit FAR limit.
- **Trajectory Risk Decomposition (`dyn_comp`):** Rather than outputting raw failure probabilities, the framework subtracts the expected static task difficulty (the prior) from the agent's current feature-based execution risk (the posterior). This isolates the dynamic anomaly actually occurring in real time.

### 6.4 Algorithm 1 — dyn_comp (Trajectory Risk Decomposition)

**Input**: 
- $e_{1:t}$: A trajectory prefix up to checkpoint step $t$
- $\mathcal{T}$: The static task definition/instruction
- $M_{1}$: A trained feature-based risk model (e.g., Logistic Regression)
- $M_{static}$: A trained static task-prior risk model

**Output**: 
- $s_{dyn\_comp}(t)$: The dynamic execution anomaly score at checkpoint $t$

**Procedure**:
1. Extract dynamic structural features $X_t$ exclusively from the observable prefix $e_{1:t}$.
2. Compute the dynamic prefix posterior: 
   $P(M_{1} \mid e_{1:t}) \leftarrow M_{1}.\text{predict\_proba}(X_t)$
3. Compute the static task-prior probability without observing the trajectory: 
   $P(M_{static} \mid \mathcal{T}) \leftarrow M_{static}.\text{predict\_proba}(\mathcal{T})$
4. Calculate the decomposed dynamic execution risk score by subtracting the static prior from the prefix posterior:
   $s_{dyn\_comp}(t) \leftarrow P(M_{1} \mid e_{1:t}) - P(M_{static} \mid \mathcal{T})$
5. **Return** $s_{dyn\_comp}(t)$

### 6.5 Algorithm 2 — Prospective Evaluation Protocol

**Input**: 
- $D_{train}, D_{calib}, D_{test}$: Task-disjoint dataset splits of trajectory prefixes
- $\text{target\_far}$: Maximum allowable false alarm rate (e.g., 0.05 / 5%)
- $K$: Maximum Checkpoint horizon limit (e.g., 30)

**Output**: 
- $\tau^*$: Frozen operating threshold
- Prospective $\text{Recall@FAR}$ and operational $\text{FAR}$ on the Test split

**Procedure**:

// Phase 1: Training
1. Train $M_{1}$ and $M_{static}$ on the prefixes bounded by horizon $K$ in $D_{train}$.

// Phase 2: Calibration (Threshold Selection)
2. For each episode in $D_{calib}$:
   a. Compute $s_{dyn\_comp}(t)$ for all observable checkpoints $t \le K$.
3. Gather $S_{succ}$: Maximum prefix scores for successful episodes in $D_{calib}$.
4. Gather $S_{fail}$: Maximum valid pre-onset prefix scores for failed episodes in $D_{calib}$.
5. Find optimal frozen threshold $\tau^*$:
   a. Initialize $\text{best\_recall} = -1.0, \text{best\_far} = 1.0, \tau^* = 0.5$
   b. For candidate threshold $\tau \in \text{CandidateRange}$:
      i. $\text{FAR}(\tau) \leftarrow \text{fraction of } S_{succ} \ge \tau$
      ii. $\text{Recall}(\tau) \leftarrow \text{fraction of } S_{fail} \ge \tau$
      iii. If $\text{FAR}(\tau) \le \text{target\_far}$:
          If $\text{Recall}(\tau) > \text{best\_recall}$ OR ($\text{Recall}(\tau) == \text{best\_recall}$ AND $\text{FAR}(\tau) < \text{best\_far}$):
              $\tau^* \leftarrow \tau, \text{best\_recall} \leftarrow \text{Recall}(\tau), \text{best\_far} \leftarrow \text{FAR}(\tau)$

// Phase 3: Prospective Testing
6. **Freeze** $\tau^*$ indefinitely.
7. For each episode in $D_{test}$:
   a. Compute $s_{dyn\_comp}(t)$ for all checkpoints $t \le K$.
8. Compute episode-level test $\text{FAR}$ and prospective test $\text{Recall@FAR}$ on $D_{test}$ using the frozen $\tau^*$.
9. Perform episode-cluster bootstrapping on the test distribution to verify statistical significance (e.g., Holm-Bonferroni correction).
10. **Return** $\tau^*$, Test Recall, Test FAR.

### 6.6 Methodology Explanation
* **Information Masking**: Enforces strict prefix bounds (checking only $e_{1:t}$) to emulate an active online run.
* **FAR-Constrained Thresholding**: Solves the operational collapse problem by optimizing the alert decision boundary exactly where False Alarms are limited.
* **Component Subtraction**: Neutralizes the bias of highly difficult tasks firing false-positives by dynamically subtracting the established difficulty prior from the current observed risk.

---

# 7. System Design & Module Development

### 7.1 Overall System Architecture
The processing pipeline is fundamentally mapped as follows:
Raw Traces $\rightarrow$ Ingestion & Canonical Schema Mapping $\rightarrow$ Terminal Sanitization $\rightarrow$ Task-Disjoint Split $\rightarrow$ Checkpoint Prefix Generation $\rightarrow$ Structural Feature Extraction $\rightarrow$ Risk Modeling & Calibration $\rightarrow$ Statistical Evaluator.

### 7.2 Module Development
The actual implemented modules managing the framework include:
* **Ingestion Module**: Parses raw trajectory JSON logs and loads them into memory within standard `Run` and `Event` dataclasses.
* **Outcome Mapping & Sanitization**: Normalizes disparate success states across benchmarks into a standard `eventual_success` flag while programmatically scrubbing terminal evaluation states from text fields to prevent early leakage.
* **Data Splitter & Prefix Generator**: Implements the task-disjoint separation boundaries (TRAIN/CALIBRATION/TEST) and iteratively slices continuous traces into independent, observation-bounded prefixes up to a checkpoint $K$.
* **Feature Extraction**: Featurizes the parsed step observations into 13 uniform structural metrics, including cumulative tool errors, consecutive retries, distinct tools utilized, and actor distributions.
* **Common Evaluator & Statistical Layer**: Hosts the unified `dyn_comp` calculations and the rigorous metrics generation logic, processing output data through a robust B=10,000 episode-cluster bootstrap procedure to compute significant confidence intervals.

### 7.3 Implementation Progress
The core design architecture defined in `TECHNICAL_DESIGN.md` has successfully progressed through the structural mapping and feature normalization phases. Phase-I successfully established the end-to-end processing pipeline, confirming the transition from ingestion to rigorous statistical reporting.

---

# 8. Project Progress & Work Completed

The following activities have been successfully completed as part of the Phase-I project scope, backed by established artifacts and verifiable implementation:

1. **Problem Identification & Research Gap Analysis**: Identified the fundamental flaw in existing AI agent evaluations reliant on uncalibrated outcomes.
2. **Evaluation Protocol Design**: Designed the standardized AIRE-Trace evaluation protocol enforcing information visibility limits and explicit dataset partitions.
3. **Dataset Preparation**: 3,316 declared Tracebench rows $\rightarrow$ 2,655 missing-artifact exclusions + 25 unreachable-path exclusions $\rightarrow$ 636 retained canonical episodes (19.18% retention).
4. **Train/Calibration/Test Separation**: Established rigorous task-disjoint splits: TRAIN (163), CALIBRATION (57), and TEST (416). The TEST split is composed of 317 failed (257 onset-valid, 60 no-onset) and 99 successful episodes.
5. **Feature & Trajectory Processing**: Developed a unified methodology for extracting 13 dynamic category-A structural features independent of dataset domain constraints.
6. **Baseline & Methodology Implementation**: Engineered seven baseline warning predictors (H1-H4 heuristics, M1 Logistic Regression, S1 Random Forest, S2 GRU) to evaluate existing limitations.
7. **AIRE-Trace (`dyn_comp`) Implementation**: Formulated and successfully implemented the Trajectory Risk Decomposition (`dyn_comp`) module.
8. **Threshold Calibration & Prospective Evaluation**: Calibrated the `dyn_comp` module on the CALIBRATION dataset under a strict target FAR ≤ 5%. Conducted formal prospective testing providing statistical evidence of an absolute gain (+0.1089) over the baseline M1 model.
9. **Statistical Framework Construction**: Implemented B=10,000 episode-cluster bootstrap resamples and Holm-Bonferroni correction testing.

---

# 9. Individual Contribution

**Mr. Naveen Raj B — Student:**
Responsible for the primary technical execution of the project, including problem formulation, research-gap analysis, methodology and evaluation-protocol development, dataset preparation, implementation of the proposed trajectory-risk decomposition approach, experimental evaluation, statistical analysis, result interpretation, and preparation of the project documentation.

**Mr. Krishnamoorthi P — Student:**
Project team member who participated in the project activities under the guidance of the project supervisors and was associated with the overall project development and review process.

**Ms. C. Janani — Associate Professor:**
Provided academic guidance, project supervision, and review of the research and development progress.

**Mr. L. Maadhava Kumar — Associate Software Developer:**
Project team member who participated in the project activities and was associated with the overall project development and review process.

---

# 10. Future Plan / Phase-II

For the upcoming Phase-II of the project timeline, efforts will center exclusively on finalizing the dissemination and end-to-end validation without altering the frozen protocol elements established in Phase-I:

1. **Implementation Refinement & Robustness Testing**: Conduct final validation runs and sanity checks on the extraction pipeline and evaluate robustness across localized configurations.
2. **Final Documentation Assembly**: Synthesize the Phase-I experiments, system design architecture, and statistical outputs into the complete Phase-II project report.
3. **Conference / Manuscript Submission**: Prepare and format the final manuscript layout for imminent external submission.
4. **Project Demonstration**: Finalize the lightweight local results visualization app for the college presentation to dynamically demonstrate the empirical divergence between retrospective evaluation and prospective monitoring.
5. **Final Evaluation/Report Preparation**: Collate comprehensive audit logs, codebases, and evaluation files into a deliverable package meeting all college standards.

---

# 11. References

[1] X. Liu et al., "AgentBench: Evaluating LLMs as Agents," in *Proc. ICLR*, 2024. arXiv:2308.03688.
[6] D. Deshpande et al., "TRAIL: Trace Reasoning and Agentic Issue Localization," arXiv preprint arXiv:2505.08638, 2025.
[7] S. Barke et al., "AgentRx: Diagnosing AI Agent Failures from Execution Trajectories," arXiv preprint arXiv:2602.02475, 2026.
[10] X. Huang et al., "PrefixGuard: From LLM-Agent Traces to Online Failure-Warning Monitors," arXiv preprint arXiv:2605.06455, 2026.
[11] B. Zhang et al., "AgentForesight: Online Auditing for Early Failure Prediction in Multi-Agent Systems," arXiv preprint arXiv:2605.08715, 2026.
[12] L. Advani, "Trajectory Guard: A Lightweight, Sequence-Aware Model for Real-Time Anomaly Detection in Agentic AI," arXiv preprint arXiv:2601.00516, 2026.

*(Note: Numeration maintained consistently with established master bibliography)*

---

# 12. Summary

The critical necessity for highly dependable and robust autonomous language agents has driven the requirement for reliable early failure alerting. The project recognized a fundamental gap in contemporary evaluations where monitors conflated final static outcomes and post-onset failure symptoms with actionable early signals, resulting in severe operational recall degradation when constrained by acceptable false-alarm limits. In Phase-I, we successfully established AIRE-Trace—a standardized, prefix-only evaluation protocol. Through our Trajectory Risk Decomposition (`dyn_comp`) module, execution risk was mathematically isolated from static task difficulty. 

The implementation was successfully completed over 636 canonical episodes resulting in bootstrap-based prospective evaluation results providing statistical evidence of `dyn_comp`'s significant (+0.1089 Recall@FAR) performance improvement under a strict operational false-alarm budget (≤ 5%). Moving into Phase-II, focus will shift strictly towards assembling the final presentation applications, robust validation audits, and finalizing the project thesis for final submission, confirming the viability of mathematically rigorous online failure warning systems.

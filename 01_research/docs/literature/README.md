# Literature Index — AIRE-TRACE

*Last updated: 2026-09-03 | Total files: 37*

This directory contains deep-research notes for all papers and patents relevant to AIRE-TRACE.
Each file follows the structure: **What It Is → What It Solves → What It Lacks → Relevance to AIRE-TRACE**.

The master research gap analysis lives at: [`docs/RESEARCH_GAP_ANALYSIS.md`](../RESEARCH_GAP_ANALYSIS.md)

---

## A. Survey Papers (Foundational)

| File | Title | Venue | Year | Ref ID |
|------|-------|-------|------|--------|
| [survey_wang_2026.md](survey_wang_2026.md) | A Survey for LLM Agent Trajectory Analysis: From Failure Attribution to Enhancement | IEEE TSE | 2026 | S1 |

---

## B. Online Failure Warning / Prefix Monitoring (Direct Competitors)

| File | Title | arXiv | Year | Ref ID |
|------|-------|-------|------|--------|
| [prefixguard.md](prefixguard.md) | PrefixGuard: From LLM-Agent Traces to Online Failure-Warning Monitors | 2605.06455 | May 2026 | M1 |
| [agentforesight.md](agentforesight.md) | AgentForesight: Online Auditing for Early Failure Prediction | 2605.08715 | May 2026 | M2 |
| [failfast_restartsmart.md](failfast_restartsmart.md) | Fail-Fast, Restart-Smart: Early Failure Prediction and Restart | 2608.03222 | Aug 2026 | M3 |
| [real_time_detection_repair.md](real_time_detection_repair.md) | Real-Time Detection and Repair of LLM Agent Failures | 2608.02464 | Aug 2026 | M4 |
| [automata_agent_traces.md](automata_agent_traces.md) | Automata from Agent Traces: Failure and Next-Step Prediction | 2608.23670 | Aug 2026 | M5 |
| [doomed_from_start.md](doomed_from_start.md) | Doomed from the Start: Early Abort via Recall-Controlled Probe Cascade | 2607.06503 | Jul 2026 | M6 |

> **Rule 7 (AGENTS.md):** Never pool M1/M2/M4 (PrefixGuard/AgentForesight/Trajectory Guard) literature numbers with locally-measured AIRE-TRACE results.

---

## C. Safety Auditing / Risk Assessment (Related Approaches)

| File | Title | arXiv | Year | Ref ID |
|------|-------|-------|------|--------|
| [traces_safety_auditing.md](traces_safety_auditing.md) | TRACES: Proactive Safety Auditing for Multi-Turn LLM Agents | 2605.27690 | May 2026 | S3 |
| [detecting_silent_failures.md](detecting_silent_failures.md) | Detecting Silent Failures in Multi-Agentic AI Trajectories | 2511.04032 | Nov 2025 | S4 |
| [oat_tracing_failure.md](oat_tracing_failure.md) | Tracing Agentic Failure from the Flow of Success (OAT) | 2607.12747 | Jul 2026 | S5 |
| [vigil.md](vigil.md) | VIGIL: A Reflective Runtime for Self-Healing LLM Agents | 2512.07094 | Oct 2025 | S6 |
| [calibration_is_not_control.md](calibration_is_not_control.md) | Calibration Is Not Control: LLM-Agent Oversight Needs Intervention | 2606.21399 | Jun 2026 | — |
| [hide_and_seek_vla.md](hide_and_seek_vla.md) | Hide-and-Seek in Trajectories: Failure Signals for VLA Models | 2605.30834 | May 2026 | — |
| [monitoring_agentic_systems.md](monitoring_agentic_systems.md) | Monitoring Agentic Systems Before They're Reliable | 2606.02494 | Jun 2026 | — |

---

## D. Anomaly Detection / One-Class Methods (Methodological Foundations)

| File | Title | Source | Year | Ref ID |
|------|-------|--------|------|--------|
| [crotad.md](crotad.md) | CroTad: Contrastive RL for Online Trajectory Anomaly Detection | arXiv 2511.16929 | Nov 2025 | A1 |
| [airl_fault_detection.md](airl_fault_detection.md) | Label-Free Industrial Fault Detection via Adversarial IRL | arXiv 2607.22987 | Jul 2026 | A3 |

*(A2: Robust Fault Detection with One-Class Training — PHM 2025 — see [additional_papers.md](additional_papers.md))*
*(A4: Survey on DL Models for Anomaly Trajectory Detection — IEEE BigComp 2026 — see [additional_papers.md](additional_papers.md))*

---

## E. Benchmarks / Datasets (Evaluation Infrastructure)

| File | Title | Source | Year | Ref ID |
|------|-------|--------|------|--------|
| [terminal_bench.md](terminal_bench.md) | Terminal-Bench: Agents on Hard CLI Tasks | ICLR 2026 / arXiv 2601.11868 | Jan 2026 | B1 |
| [atbench.md](atbench.md) | ATBench: Diverse and Realistic Agent Trajectory Benchmark | arXiv 2604.02022 | Apr 2026 | B3 |
| [monitoringbench.md](monitoringbench.md) | MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring | arXiv 2605.09684 | May 2026 | B4 |
| [horizon_benchmark.md](horizon_benchmark.md) | HORIZON: Cross-Domain Diagnostic Benchmark for Long-Horizon Failures | arXiv 2604.11978 | Apr 2026 | B5 |
| [holistic_evaluation_trail.md](holistic_evaluation_trail.md) | Holistic Evaluation and Failure Diagnosis of AI Agents (TRAIL) | arXiv 2605.14865 | May 2026 | B6/E1 |
| [telbench.md](telbench.md) | TELBench: Where Do Deep-Research Agents Go Wrong? | arXiv 2606.02060 | Jun 2026 | — |

*(B2: τ²-Bench Enterprise Evaluation Guide — see [additional_papers.md](additional_papers.md))*
*(Terminal Wrench: Reward-Hackable Tasks — see [additional_papers.md](additional_papers.md))*

---

## F. Threshold Calibration / False Alarm Control (Statistical Methods)

| File | Title | Source | Year | Ref ID |
|------|-------|--------|------|--------|
| [e_valuator.md](e_valuator.md) | E-valuator: Reliable Agent Verifiers with Sequential Hypothesis Testing | arXiv 2512.03109 | Dec 2025 | T1 |
| [stratified_bootstrap.md](stratified_bootstrap.md) | Stratified Bootstrap Test Package | arXiv 2512.15057 | Dec 2025 | T3 |

*(T2: Decision Threshold Setting in Binary Classification — J. Ops Management 2026 — see [additional_papers.md](additional_papers.md))*

---

## G. Data Leakage / Task-Disjoint Splitting (Methodological Foundations)

| File | Title | Source | Year | Ref ID |
|------|-------|--------|------|--------|
| [datasail_leakage.md](datasail_leakage.md) | DataSAIL: Data Splitting Against Information Leakage | Nature Communications | Feb 2026 | L1 |
| [timeseries_leakage.md](timeseries_leakage.md) | Rethinking Evaluation in the Era of Time Series Foundation Models | arXiv 2510.13654 | Oct 2025 | L2 |

*(L3: Train-Test Split and Data Leakage — TheoremPath 2026 — see [additional_papers.md](additional_papers.md))*

---

## H. Evaluation Methodology / Statistical Analysis

| File | Title | Source | Year | Ref ID |
|------|-------|--------|------|--------|
| [holistic_evaluation_trail.md](holistic_evaluation_trail.md) | Holistic Evaluation and Failure Diagnosis of AI Agents (TRAIL) | arXiv 2605.14865 | May 2026 | E1/B6 |
| [efficient_benchmarking.md](efficient_benchmarking.md) | Efficient Benchmarking of AI Agents | arXiv 2603.23749 | Mar 2026 | E2 |

*(E3: Bootstrap CIs for LLM Eval Metrics — see [additional_papers.md](additional_papers.md))*
*(E4: The 2026 Agent Reliability Gap — see [additional_papers.md](additional_papers.md))*

---

## I. Patents (Prior Art)

| File | Patent ID | Assignee | Status |
|------|-----------|----------|--------|
| [patents_prior_art.md](patents_prior_art.md) | US20260086538A1 | Unknown | Published Mar 2026 |
| [patents_prior_art.md](patents_prior_art.md) | US20260200498A1 | Unknown | Published Jul 2026 |
| [patents_prior_art.md](patents_prior_art.md) | US20260220278A1 | Citibank | Active Jul 2026 |
| [patents_prior_art.md](patents_prior_art.md) | Microsoft US2026/0148126 | Microsoft | Published May 2026 |
| [patents_prior_art.md](patents_prior_art.md) | US12592897 | Unknown | Granted Mar 2026 |
| [patents_prior_art.md](patents_prior_art.md) | CN121071760B | Unknown | Published Nov 2025 |

---

## J. Previously Stored / Other

| File | Title | Source | Year |
|------|-------|--------|------|
| [duotrace.md](duotrace.md) | DUOTRACE: Cascade Failure Attribution | arXiv 2608.29646 | Aug 2026 |
| [trajectory_guard.md](trajectory_guard.md) | Trajectory Guard: Siamese Recurrent Autoencoder | arXiv 2601.00516 | Jan 2026 |
| [agentrx.md](agentrx.md) | AgentRx: Diagnosing AI Agent Failures from Trajectories | arXiv 2602.02475 | Feb 2026 |
| [ade_prf.md](ade_prf.md) | ADE-PRF: Agent Delivery Engineering Predictive Reliability Framework | arXiv 2607.07689 | Jul 2026 |
| [peam.md](peam.md) | PEAM: Parametric Embodied Agent Memory | arXiv 2605.27762 | May 2026 |
| [additional_papers.md](additional_papers.md) | Omnibus file: 9 shorter notes (τ²-Bench guide, Terminal Wrench, Unsupervised Futile Cycles, etc.) | Various | 2025–2026 |

---

## Key AIRE-TRACE Baselines (Rule 7 — Always Separate from Local Numbers)

| System | Benchmark | Metric | Literature Value |
|--------|-----------|--------|-----------------|
| PrefixGuard | WebArena | AUPRC | **0.900** |
| PrefixGuard | τ²-Bench | AUPRC | **0.710** |
| PrefixGuard | TerminalBench | AUPRC | **0.557** (primary Mode A target to beat) |
| AgentForesight-7B | AFTraj-2K | Step localization gain | **+19.9%** vs GPT-4.1 |
| RT Detection (ESN) | 2,823 episodes | AUROC | **0.872** |
| FSM Automata | Per-state features | AUROC | **0.94** |
| Trajectory Guard | Balanced sets | F1 | **0.88–0.94** |
| OAT | In-domain | F1 gain | **+20%** |
| DUOTRACE | Attribution | Agent/Step | **+8.7% / +7.0%** |

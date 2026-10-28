# AgentForesight (Already stored in agentforesight.md)
# OAT (Already stored in oat_tracing_failure.md)
# Real-Time Detection (Already stored in real_time_detection_repair.md)
# FailFast-RestartSmart (Already stored in failfast_restartsmart.md)
# DUOTRACE (Already stored in duotrace.md)
# AgentRx (Already stored in agentrx.md)
# Trajectory Guard (Already stored in trajectory_guard.md)

# Survey on Deep Learning Models for Anomaly Trajectory Detection (Feb 2026)

**Category:** Anomaly Detection / One-Class Methods — Survey
**Published:** IEEE BigComp, February 2026

---

## What the Paper Is

A survey paper covering deep learning models specifically for **anomaly trajectory detection** across domains (transportation, robotics, and general sequential data).

## Relevance to AIRE-TRACE

- Catalogs DL approaches for trajectory anomaly detection that can be adapted to LLM agent traces
- IEEE BigComp venue suggests focus on big data settings — relevant scale for production agent monitoring
- Should be consulted when selecting our feature extraction and model architecture for the anomaly detection component

---

# Robust Fault Detection with One-Class Training (Oct 2025)

**Category:** Anomaly Detection / One-Class Methods
**Published:** PHM Conference, October 2025

---

## What the Paper Is

A PHM (Prognostics and Health Management) conference paper on fault detection using **one-class training** approaches — learning only from healthy/normal samples.

## Relevance to AIRE-TRACE

- Directly supports the one-class training paradigm our monitors use (train only on healthy runs → Rule 8)
- PHM community has decades of experience with one-class fault detection; their best practices (threshold setting, false alarm rates, test statistics) are applicable
- CUSUMs and other sequential tests are standard in PHM — supporting our CUSUM alarm design
- The PHM framing treats agents like machines — "healthy null" is the normal operating distribution, exactly as in our echo-state-network design

---

# Decision Threshold Setting in Binary Classification Problems (June 2026)

**Category:** Threshold Calibration / False Alarm Control
**Published:** Journal of Operations Management, June 2026

---

## What the Paper Is

A methodological paper on principled threshold selection in binary classification problems, likely covering ROC analysis, cost-sensitive thresholds, and operational constraints.

## Relevance to AIRE-TRACE

- Our Section 8 threshold procedure requires principled threshold selection from the CALIBRATION set only
- The cost-sensitive framing (FPR budget of 5% and 25% in our protocol) maps directly to threshold selection under asymmetric loss
- Operations Management perspective adds practical deployment considerations (what does a false alarm cost vs. a missed detection?)

---

# Towards a Fair and Transparent Early Warning System for Academic Failure (July 2026)

**Category:** Threshold Calibration / False Alarm Control — Cross-domain
**Published:** Frontiers in Education, July 2026

---

## What the Paper Is

An education domain paper on early warning systems for student failure, addressing **fairness and transparency** in threshold setting and alert generation.

## Relevance to AIRE-TRACE

- Cross-domain insight into early warning system design (education → agents)
- Fairness constraints in threshold setting are analogous to our mode-labeling requirement (Rule 7) — different contexts require different thresholds and must not be pooled
- Transparency in alarm generation aligns with our auditable validation log requirement (from AgentRx's constraint-violation evidence)

---

# Tau-Bench: Enterprise Evaluation Guide (Aug 2026)

**Category:** Benchmarks / Datasets
**Published:** Automation Anywhere, August 2026

---

## What the Paper Is

The **2026 Enterprise Evaluation Guide** for τ²-Bench (tau-bench), detailing how to use it for enterprise-grade agentic AI evaluation.

## Relevance to AIRE-TRACE

- τ²-Bench is our **Mode B (τ²-Bench) benchmark** — the primary retail/airline API agent dataset
- Enterprise evaluation guide provides the authoritative interpretation of success/failure criteria for τ²-Bench tasks
- The canonical `eventual_success`/`eventual_failure` mapping for τ²-Bench must follow this guide's definitions (Rule 10)
- Enterprise scenarios emphasize tool correctness and API compliance — different failure modes than TerminalBench's system-level tasks

---

# Terminal Wrench: Reward-Hackable Tasks in Terminal Agent Benchmarks (Apr 2026)

**Category:** Benchmarks / Datasets
**arXiv:** [2605.30834 area] / separate arXiv, April 2026

---

## What the Paper Is

Identifies **reward-hackable tasks** in TerminalBench — cases where agents can achieve verification success without genuinely completing the intended task.

## Relevance to AIRE-TRACE

- **Critical for our ground truth integrity**: Terminal Wrench identifies which TerminalBench tasks have compromised verification
- Gate 1 (real dataset inspection) must cross-reference Terminal Wrench findings and exclude or flag hackable tasks
- Our canonical outcome mapping (Rule 10) must be aware of these edge cases — a "success" in TerminalBench for a reward-hackable task may not be genuine success
- This should be logged in RESEARCH_LOG.md as a Gate 1 finding when inspecting TerminalBench episodes

---

# Unsupervised Approaches to Futile Cycle Detection in AI Agents (Apr 2026)

**Category:** Related Technical Approaches
**Published:** IBM Research, April 2026

---

## What the Paper Is

IBM Research paper on detecting **futile cycles** — when agents loop without making progress — using unsupervised methods.

## Relevance to AIRE-TRACE

- Futile cycles (looping) are one of the core failure modes in our taxonomy (silent failures, per 2511.04032)
- IBM's unsupervised approach (no failure labels needed) complements our one-class echo-state-network — both train on healthy patterns
- Cycle detection features (repeated state visits, action loops) should be included in our feature set
- IBM Research's production context suggests this has been validated at scale

---

# Cascade Failure Attribution for Multi-Agent Systems — DUOTRACE (Aug 2026)

→ Already stored in [`duotrace.md`](duotrace.md)

---

# End-to-End Framework for Data Lineage Analysis with Fault Diagnosis and Early Warning (Jan 2026)

**Category:** Related Technical Approaches
**Published:** Scientific Reports, January 2026

---

## What the Paper Is

A system for data lineage analysis with integrated **fault diagnosis** and **early warning** components — applied to data pipeline reliability.

## Relevance to AIRE-TRACE

- Data lineage tracking in pipeline systems is analogous to our step-chain tracking in agent traces
- Early warning component mirrors our prefix-level alarm design
- The link pattern recognition component may inspire feature ideas for detecting structural irregularities in agent action chains

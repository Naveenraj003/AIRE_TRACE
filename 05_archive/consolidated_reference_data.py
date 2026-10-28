"""
AIRE-Trace Consolidated Reference & Literature Archive Data
===========================================================
This module consolidates all historical reference update payloads, bibliographic
entries, and literature summaries originally partitioned across 9 individual
scripts:
  1. 05_archive/update_refs.py
  2. 05_archive/update_refs2.py
  3. 05_archive/update_refs3.py
  4. 05_archive/update_refs4.py
  5. 05_archive/update_refs5.py
  6. 05_archive/update_refs6.py
  7. 05_archive/update_refs7.py
  8. 05_archive/create_lit_files.py
  9. 05_archive/create_more_lit_files.py

All 48 literature files remain authoritative in:
  01_research/docs/literature/
and the verified reference list in:
  04_ieee_publication/AIRE-Trace_Verified_References.md

This file preserves all raw dictionary payloads, table rows, and bibliographic
markdown text for archival traceability and zero data loss.
"""

import os

# ----------------------------------------------------------------------
# 1. Consolidated Literature Markdown Files (49 unique papers & patents)
# ----------------------------------------------------------------------
LITERATURE_DOCS = {
    # Source: 05_archive/create_more_lit_files.py
    "accurate_failure_prediction.md": """# Accurate Failure Prediction in Agents

**Title:** Accurate Failure Prediction in Agents Does Not Imply Effective Failure Prevention
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026 (arXiv:2602.03338)

## Summary
Defines disruption/recovery tradeoff; states intervention disrupts baseline successes.""",

    # Source: 05_archive/create_more_lit_files.py
    "acrfence.md": """# ACRFence

**Title:** ACRFence
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026

## Summary
Identifies semantic rollback attacks arising from regenerated tool calls after checkpoint restoration and proposes recording irreversible effects plus replay/fork semantics.""",

    # Source: 05_archive/update_refs5.py
    "agent_trajectory_sentinel.md": """# AgentTrajectorySentinel

**Title:** AgentTrajectorySentinel
**Authors:** [Authors]
**Venue:** Hugging Face Space / Technical Notes, 2026

## Summary
A system for real-time detection and repair of LLM agent failures. Functions as a low-cost, healthy-only temporal monitor utilizing deterministic verification and a rollback-and-retry mechanism.""",

    # Source: 05_archive/create_more_lit_files.py
    "agentrewind.md": """# AgentRewind: Recoverable Execution

**Title:** AgentRewind: Recoverable Execution for Long-Horizon LLM Agents
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026 (arXiv:2608.14380)

## Summary
Discloses restoring execution states at LLM/tool hooks to recover from early errors in long-horizon tasks.""",

    # Source: 05_archive/create_more_lit_files.py
    "agenttether.md": """# AgentTether: Graph-Guided Diagnosis

**Title:** AgentTether: Graph-Guided Diagnosis and Runtime Intervention for Reliable LLM Agent Operation
**Authors:** Zhao et al.
**Venue:** arXiv preprint, 2026 (arXiv:2607.06273)

## Summary
Discloses post-run diagnosis and guided recovery interventions using transition graphs.""",

    # Source: 05_archive/create_lit_files.py
    "blip.md": """# BLIP

**Title:** BLIP: Minimal verifiable provenance for black-box LLMs
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026 (arXiv:2608.25210)

## Summary
Focuses on minimal verifiable provenance for black-box LLMs. Evaluated as Candidate 5 for the prior-art chart.""",

    # Source: 05_archive/create_more_lit_files.py
    "chronomem.md": """# ChronoMem

**Title:** Version Control and Semantic Rollback for Large Language Model Agent Memory
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026

## Summary
Snapshots agent memory, maintains version histories, maps rollback requests to historical versions, and evaluates post-rollback behavior.""",

    # Source: 05_archive/update_refs6.py
    "coagent.md": """# CoAgent

**Title:** CoAgent: Concurrency Control for Multi-Agent Systems
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026

## Summary
Addresses the challenge of multiple LLM agents working on shared state simultaneously by introducing MTPO (Monotonic Trajectory Pre-Order), treating control as advisory rather than blocking or aborting.""",

    # Source: 05_archive/create_more_lit_files.py
    "cora.md": """# CORA: Conformal Risk-Controlled Agents

**Title:** CORA: Conformal Risk-Controlled Agents for Safeguarded Mobile GUI Automation
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026 (arXiv:2604.09155)

## Summary
Discloses bounding risk distributionally via conformal risk control without full trial execution.""",

    # Source: 05_archive/update_refs4.py
    "crab_2025.md": """# Crab (Checkpoint-and-Restore for Agent SandBoxes)

**Title:** Crab: Checkpoint-and-Restore for Agent SandBoxes
**Authors:** [Authors]
**Venue:** arXiv preprint, 2025

## Summary
A transparent, host-side runtime system designed to bridge the agent-OS semantic gap. Uses an eBPF-based inspector for OS-visible state minimization, cutting checkpoint traffic by up to 87%. Evaluated for Semantic checkpointing.""",

    # Source: 05_archive/update_refs5.py
    "da_lce.md": """# DA-LCE

**Title:** Difficulty-Aware Learning Curve Extrapolation
**Authors:** [Authors]
**Venue:** AAAI 2026

## Summary
Improves Learning Curve Extrapolation by incorporating task difficulty as a fundamental dimension, quantifying it directly from early learning curve dynamics using conditional diffusion models.""",

    # Source: 05_archive/create_lit_files.py
    "de_kleer_1986.md": """# An Assumption-based TMS

**Title:** An Assumption-based TMS
**Authors:** Johan de Kleer
**Venue:** Artificial Intelligence, Vol. 28, No. 2, pp. 127-162, 1986

## Summary
Introduces the ATMS (Assumption-based Truth Maintenance System). Unlike justification-based TMS, it manages multiple contexts simultaneously by tracking the minimal sets of assumptions for beliefs. Evaluated as Candidate 4.""",

    # Source: 05_archive/update_refs5.py
    "decider.md": """# DECIDER (Model Disagreement)

**Title:** DECIDER
**Authors:** [Authors]
**Venue:** 2026

## Summary
Focuses on model disagreement techniques (ensembling/uncertainty estimation) to detect conflicting model outputs, which serve as signals for potential errors or necessary human intervention.""",

    # Source: 05_archive/create_lit_files.py
    "doyle_1979.md": """# A Truth Maintenance System

**Title:** A Truth Maintenance System
**Authors:** Jon Doyle
**Venue:** Artificial Intelligence, Vol. 12, pp. 231-272, 1979

## Summary
Foundational paper on truth maintenance systems (TMS). Discloses justification-based belief revision, allowing systems to track assumptions and revise them upon encountering contradictions. Evaluated as Candidate 4.""",

    # Source: 05_archive/update_refs6.py
    "dpbench.md": """# DPBench

**Title:** DPBench: Structural Determinants of Multi-Agent LLM Coordination Under Simultaneous Resource Contention
**Authors:** Hasan & BusiReddyGari
**Venue:** arXiv preprint, 2026

## Summary
A benchmark adapting the Dining Philosophers problem to evaluate how LLM agents coordinate under simultaneous resource contention. Highlights agent failures due to convergent reasoning in concurrent settings.""",

    # Source: 05_archive/create_more_lit_files.py
    "dreamguard.md": """# DreamGuard: Efficient Runtime Guardrail

**Title:** DreamGuard: Efficient Runtime Guardrail for LLM Agents via Risk-Aware World Model
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026 (arXiv:2608.05695)

## Summary
Pre-execution estimator. Predicts unexecuted successor latent states using a world model to proactively assess hazard/risk.""",

    # Source: 05_archive/create_lit_files.py
    "err_measure.md": """# Recoverability Has a Law

**Title:** Recoverability Has a Law: The ERR Measure for Tool-Augmented Agents
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026 (arXiv:2601.22352)

## Summary
Proposes the ERR measure for tool-augmented agents, establishing analytic boundaries on recoverability.""",

    # Source: 05_archive/update_refs4.py
    "evo_bench.md": """# Evo-Bench

**Title:** Evo-Bench
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026

## Summary
A research framework designed to evaluate an LLM agent's ability to autonomously optimize its own "operating harness" (workflows, tool-use strategies). Flagged as Unverified - Level 3.""",

    # Source: 05_archive/create_more_lit_files.py
    "evoundo.md": """# EvoUndo: Recoverability-Constrained Self-Evolution

**Title:** EvoUndo: Recoverability-Constrained Self-Evolution for LLM Agent Harnesses
**Authors:** Tanmay Sah et al.
**Venue:** arXiv preprint, 2026 (arXiv:2608.28363)

## Summary
Evaluates capability recovery and intervention. Demonstrates counterfactual state evaluation and intervention-conditioned capability preservation in agents.""",

    # Source: 05_archive/create_lit_files.py
    "freshctx.md": """# FreshCtx: Runtime freshness guard

**Title:** FreshCtx: Runtime freshness guard
**Authors:** Hyperwise-LLC
**Venue:** Open Source / GitHub, 2026

## Summary
An open-source runtime freshness guard that fingerprints data sources and revalidates them before action execution. If evidence is stale, the action is blocked (fail-closed behavior).""",

    # Source: 05_archive/create_lit_files.py
    "gupta_mumick_1993.md": """# Maintaining Views Incrementally

**Title:** Maintaining Views Incrementally
**Authors:** Ashish Gupta, Inderpal Singh Mumick, V.S. Subrahmanian
**Venue:** SIGMOD 1993

## Summary
Seminal paper on Incremental View Maintenance (IVM). Discloses methods to update database views incrementally rather than recomputing them from scratch. Evaluated as Candidate 6.""",

    # Source: 05_archive/update_refs4.py
    "horma_2026.md": """# HORMA (Hierarchical Organize-and-Retrieve Memory Agent)

**Title:** HORMA: Hierarchical Organize-and-Retrieve Memory Agent
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026

## Summary
A framework that implements a hierarchical memory structure for LLM agents. Improves reasoning quality and reduces latency/token usage in long-horizon tasks. Evaluated alongside PABU for semantic state minimization.""",

    # Source: 05_archive/create_more_lit_files.py
    "loopharness.md": """# LoopHarness

**Title:** Safety Does Not Compose: Non-Decaying Loop State for Autonomous LLM Agents
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026

## Summary
Proposes persistent, non-decaying loop-level safety state and calls the mechanism LoopHarness.""",

    # Source: 05_archive/update_refs5.py
    "monitoring_web_agents.md": """# Monitoring Web Agents Without Internal Signals

**Title:** Monitoring Web Agents Without Internal Signals: Observable Trajectories and Key-Step Supervision
**Authors:** [Authors]
**Venue:** arXiv preprint, September 2026

## Summary
Proposes a framework for prefix-level risk prediction that relies entirely on externally observable interactions (macro and micro features) between the agent and its environment, bypassing the need for internal model signals.""",

    # Source: 05_archive/update_refs4.py
    "pabu_2026.md": """# PABU (Progress-Aware Belief Update)

**Title:** PABU: Progress-Aware Belief Update
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026

## Summary
A belief-state framework that explicitly models task progress. Discards task-irrelevant information to maintain a compact state representation, reducing token usage.""",

    # Source: 05_archive/create_lit_files.py
    "paint.md": """# PAINT: Proactive Agent Interventions

**Title:** When to Ask for Help: Proactive Interventions in Autonomous RL
**Authors:** [Authors]
**Venue:** ICML 2022

## Summary
Focuses on reversibility estimation and proactive intervention in autonomous reinforcement learning. Evaluated as Candidate 2 for the prior-art chart.""",

    # Source: 05_archive/create_lit_files.py
    "planfence.md": """# Fresh Memory, Stale Plans

**Title:** Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory
**Authors:** Evan Chen, Shiqiang Wang, Christopher G. Brinton
**Venue:** arXiv preprint, 2026 (arXiv:2609.03340)

## Summary
Introduces PlanFence to prevent "stale-plan execution." Before executing an action, the system validates the specific data dependencies; if they are stale, the action is blocked or replanned.""",

    # Source: 05_archive/create_lit_files.py
    "rail.md": """# RAIL: Recoverability-Aware Intervention Learning

**Title:** Recoverability-Aware Intervention Learning
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026 (arXiv:2608.05080)

## Summary
Discloses recoverability-aware intervention learning. Evaluated as a potential mechanism for intervention-conditioned future capability preservation.""",

    # Source: 05_archive/update_refs5.py
    "semantic_checkpointing_mechanisms.md": """# Semantic Checkpointing Mechanisms for Stateless LLM Agents

**Title:** Semantic Checkpointing Mechanisms for Stateless LLM Agents
**Authors:** [Authors]
**Venue:** 2025

## Summary
An architectural pattern designed to overcome the statelessness of LLMs by persisting critical context, reasoning, and decision states in external storage. Allows state reconstruction without persisting hidden reasoning, reducing bloat.""",

    # Source: 05_archive/update_refs6.py
    "semantic_consensus.md": """# Semantic Consensus Framework (SCF)

**Title:** Semantic Consensus Framework (SCF)
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026

## Summary
A process-aware middleware designed to detect and resolve "Semantic Intent Divergence" (semantic conflicts) between cooperating agents in real-time, improving reliability in enterprise multi-agent LLM systems.""",

    # Source: 05_archive/update_refs3.py
    "silent_semantic_violations.md": """# Silent Semantic Violations

**Title:** Demystifying and Checking Silent Semantic Violations in Large Distributed Systems
**Authors:** [Authors]
**Venue:** OSDI 2022

## Summary
Refers to a class of bugs or failures in complex systems where the system remains operational and does not trigger explicit error signals, but behaves in a way that violates its intended logic or constraints. In LLM agents, this refers to failures where the agent produces output that is syntactically valid but semantically incorrect or inconsistent.""",

    # Source: 05_archive/update_refs4.py
    "skilltv_bench.md": """# SkillTV-Bench

**Title:** SkillTV-Bench
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026

## Summary
A benchmark introduced in August 2026 to evaluate AI models acting as judges for long-horizon agent trajectories, focusing on skill-aware verification. Flagged as Unverified - Level 3.""",

    # Source: 05_archive/create_lit_files.py
    "sparse_evidence_alerting.md": """# Sparse-Evidence Early-Alerting

**Title:** Sparse-Evidence Early-Alerting
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026

## Summary
Addresses early failure prediction where evidence of failure is sparse (only present in a few turns) or delayed. Typically involves attention-based models to pinpoint failure-indicating turns.""",

    # Source: 05_archive/create_more_lit_files.py
    "state_aware_runtime.md": """# State-Aware Runtime

**Title:** State-Aware Runtime
**Authors:** Xiwei Chen
**Venue:** Working paper, Version 4 dated Aug. 17, 2026

## Summary
Explicitly discusses canonical state, bounded state views, proposals, speculative future states, validation, commit, rollback/compensation and audit traces.""",

    # Source: 05_archive/update_refs4.py
    "state_saturation_trap.md": """# State Saturation Trap

**Title:** State Saturation Trap
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026

## Summary
A phenomenon identified in agent monitoring where sustained difficulty causes an agent's modeled frustration to saturate, turning monitoring systems into constant, unhelpful alarms. Flagged as Unverified - Level 3.""",

    # Source: 05_archive/create_more_lit_files.py
    "statefork_waypoint.md": """# Toward Systems Foundations for Agentic Exploration

**Title:** Toward Systems Foundations for Agentic Exploration (StateFork / Waypoint)
**Authors:** Columbia DAPLab
**Venue:** arXiv preprint, 2025 (arXiv:2510.05556)

## Summary
Discloses systems foundations (CRIU plus OverlayFS) for branching and checkpointing/restoring agent execution states.""",

    # Source: 05_archive/update_refs6.py
    "toctou_idempotency.md": """# TOCTOU and Idempotency-Key Literature

**Title:** TOCTOU and Idempotency-Key Literature
**Authors:** Various
**Venue:** General Systems Research

## Summary
Foundational systems research literature covering Time-of-Check to Time-of-Use (TOCTOU) race conditions and idempotency keys, critical for ensuring safe execution semantics in environments subject to staleness or concurrency.""",

    # Source: 05_archive/create_more_lit_files.py
    "toolchain_crc.md": """# ToolChain-CRC

**Title:** ToolChain-CRC: Conformal Risk Control for Agentic AI Under Retrieval and Tool-Use Drift
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026 (arXiv:2606.18467)

## Summary
Uses conformal risk control over trajectories of actions/observations to stop risky runs.""",

    # Source: 05_archive/update_refs7.py
    "us12202518b2.md": """# US12202518B2 (Nvidia, 2025)

**Title:** Safety decomposition architecture for autonomous machine applications
**Authors:** Nvidia
**Venue:** US Patent, 2025

## Summary
Uses "safety decomposition" for ASIL compliance in trajectory selection. Does not cover failure risk decomposition for warning systems.""",

    # Source: 05_archive/update_refs7.py
    "us12296849b2.md": """# US12296849B2 (2024)

**Title:** Method and system for feasibility-based operation of an autonomous agent
**Authors:** [Inventors]
**Venue:** US Patent, 2024

## Summary
Scores policies based on feasibility for agents in an environment; focuses on intention estimation, not risk isolation or decomposition.""",

    # Source: 05_archive/update_refs7.py
    "us12441366b2.md": """# US12441366B2 (Nvidia, 2025)

**Title:** Task-relevant failure detection for trajectory prediction in machines
**Authors:** Nvidia
**Venue:** US Patent, 2025

## Summary
Detects failures in trajectory predictors using cost probability distributions and anomaly detection for autonomous vehicles. Does not isolate trajectory risk from task-difficulty risk or focus on failure risk decomposition for warning systems.""",

    # Source: 05_archive/update_refs7.py
    "us12450494b1.md": """# US12450494B1 (2025)

**Title:** Validating autonomous artificial intelligence (AI) agents using generative AI
**Authors:** [Inventors]
**Venue:** US Patent, 2025

## Summary
Maps actions to risk categories based on task sensitivity, but does not separate trajectory-dependent risk from task-difficulty risk.""",

    # Source: 05_archive/update_refs5.py
    "us20110161048a1.md": """# US20110161048A1

**Title:** Threshold-violation-from-baseline-deviation
**Authors:** [Inventors]
**Venue:** US Patent Application, 2011

## Summary
A granted patent covering general residual-anomaly-scoring and threshold violation from baseline deviation.""",

    # Source: 05_archive/update_refs7.py
    "us20200174481a1.md": """# US20200174481A1 (Waymo, 2020)

**Title:** Probabilistic risk assessment for trajectory evaluation
**Authors:** Waymo
**Venue:** US Patent Application, 2020

## Summary
Evaluates trajectory risk using heat maps and overlap probabilities for autonomous vehicles. No task-difficulty decomposition.""",

    # Source: 05_archive/update_refs7.py
    "us20230192139a1.md": """# US20230192139A1

**Title:** Method and system for addressing failure in an autonomous agent
**Authors:** [Inventors]
**Venue:** US Patent Application, 2023

## Summary
Covers failure detection and response in autonomous vehicles. Does not cover trajectory-dependent risk decomposition.""",

    # Source: 05_archive/update_refs7.py
    "us63_841_017.md": """# US #63/841,017 (pending)

**Title:** System and Method for Predictive Failure Detection in AI Agent Workflows
**Authors:** [Inventors] (PredictAgent project)
**Venue:** US Patent Application (Pending)

## Summary
Covers predictive failure detection for AI agents, but focuses on cross-user contamination analysis rather than trajectory-dependent decomposition.""",

    # Source: 05_archive/create_lit_files.py
    "verified_tool_calls.md": """# Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures

**Title:** Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures
**Authors:** Isham Kalappurackal Mansoor, Abhishek Phadke, Pratip Rana
**Venue:** arXiv preprint, 2026 (arXiv:2608.02645)

## Summary
Addresses non-atomic tool failures (e.g., timeout-after-dispatch, partial success) via a verify-before-retry approach. Implements postcondition verification rather than blind retries to prevent duplicate side effects.""",

    # Source: 05_archive/update_refs5.py
    "weakly_supervised_alerting.md": """# Weakly Supervised Early Failure Alerting

**Title:** When Evidence is Sparse: Weakly Supervised Early Failure Alerting in Dialogs and LLM-Agent Trajectories
**Authors:** [Authors]
**Venue:** arXiv preprint, 2026

## Summary
Introduces a two-stage method to identify potential failures in multi-turn interactions before they conclude. Uses an attention-based failure predictor to find sparse turn-level evidence of failure from overall trajectory labels.""",

    # Source: 05_archive/update_refs7.py
    "wo1994029983a1.md": """# WO1994029983A1 (1994)

**Title:** Performance monitoring and failure isolation in communications networks
**Authors:** [Inventors]
**Venue:** WIPO Patent Application, 1994

## Summary
Isolates equipment failures in networks through error distribution analysis. Unrelated to trajectory or task-difficulty risk decomposition.""",

}

# ----------------------------------------------------------------------
# 2. Historical Table Additions (Markdown Table Rows)
# ----------------------------------------------------------------------
TABLE_ADDITIONS = [
    {
        "source": "05_archive/update_refs.py",
        "content": """| 27 | RAIL | arXiv:2608.05080 | [Authors] | arXiv 2026 | VERIFIED |
| 28 | PAINT | ICML 2022 | [Authors] | ICML 2022 | VERIFIED |
| 29 | Doyle 1979 | AI 12(2) | Jon Doyle | Artif. Intell. 1979 | VERIFIED |
| 30 | de Kleer 1986 | AI 28(2) | Johan de Kleer | Artif. Intell. 1986 | VERIFIED |
| 31 | BLIP | arXiv:2608.25210 | [Authors] | arXiv 2026 | VERIFIED |
| 32 | Gupta/Mumick 1993 | SIGMOD 1993 | Ashish Gupta et al. | SIGMOD 1993 | VERIFIED |
| 33 | ERR | arXiv:2601.22352 | [Authors] | arXiv 2026 | VERIFIED |
| 34 | RTDR | arXiv:2608.02464 | [Authors] | arXiv 2026 | VERIFIED |"""
    },
    {
        "source": "05_archive/update_refs2.py",
        "content": """| 35 | Verified Tool Calls | arXiv:2608.02645 | Isham Kalappurackal Mansoor et al. | arXiv 2026 | VERIFIED |
| 36 | PlanFence | arXiv:2609.03340 | Evan Chen et al. | arXiv 2026 | VERIFIED |
| 37 | FreshCtx | Open Source | Hyperwise-LLC | GitHub 2026 | VERIFIED |
| 38 | Sparse-Evidence Alerting | arXiv 2026 | [Authors] | arXiv 2026 | VERIFIED |"""
    },
    {
        "source": "05_archive/update_refs3.py",
        "content": """| 39 | E-valuator | arXiv:2512.03109 | [Authors] | arXiv 2025 | VERIFIED |
| 40 | Silent Semantic Violations | OSDI 2022 | [Authors] | OSDI 2022 | VERIFIED |"""
    },
    {
        "source": "05_archive/update_refs4.py",
        "content": """| 41 | Crab | arXiv 2025 | [Authors] | arXiv 2025 | VERIFIED |
| 42 | HORMA | arXiv 2026 | [Authors] | arXiv 2026 | VERIFIED |
| 43 | PABU | arXiv 2026 | [Authors] | arXiv 2026 | VERIFIED |
| 44 | SkillTV-Bench | arXiv 2026 | [Authors] | arXiv 2026 | FLAGGED (Unverified) |
| 45 | Evo-Bench | arXiv 2026 | [Authors] | arXiv 2026 | FLAGGED (Unverified) |
| 46 | State Saturation Trap | arXiv 2026 | [Authors] | arXiv 2026 | FLAGGED (Unverified) |"""
    },
    {
        "source": "05_archive/update_refs5.py",
        "content": """| 47 | Semantic Checkpointing Mechanisms | 2025 | [Authors] | 2025 | VERIFIED |
| 48 | Weakly Supervised Alerting | arXiv 2026 | [Authors] | arXiv 2026 | VERIFIED |
| 49 | Monitoring Web Agents Without Internal Signals | arXiv 2026 | [Authors] | Sept 2026 | VERIFIED |
| 50 | AgentTrajectorySentinel | HF Space 2026 | [Authors] | 2026 | VERIFIED |
| 51 | DECIDER | 2026 | [Authors] | 2026 | VERIFIED |
| 52 | DA-LCE | AAAI 2026 | [Authors] | AAAI 2026 | VERIFIED |
| 53 | US20110161048A1 | US Patent 2011 | [Inventors] | 2011 | VERIFIED |"""
    },
    {
        "source": "05_archive/update_refs6.py",
        "content": """| 54 | CoAgent | arXiv 2026 | [Authors] | 2026 | VERIFIED |
| 55 | DPBench | arXiv 2026 | Hasan et al. | 2026 | VERIFIED |
| 56 | Semantic Consensus (SCF) | arXiv 2026 | [Authors] | 2026 | VERIFIED |
| 57 | TOCTOU / idempotency-key | Gen. Systems | Various | - | VERIFIED |"""
    },
    {
        "source": "05_archive/update_refs7.py",
        "content": """| 58 | US12441366B2 | Nvidia 2025 | Nvidia | 2025 | VERIFIED |
| 59 | US12202518B2 | Nvidia 2025 | Nvidia | 2025 | VERIFIED |
| 60 | US20230192139A1 | US App 2023 | Various | 2023 | VERIFIED |
| 61 | US63/841,017 | US App Pending | PredictAgent | - | VERIFIED |
| 62 | US20200174481A1 | Waymo 2020 | Waymo | 2020 | VERIFIED |
| 63 | US12450494B1 | US Patent 2025 | Various | 2025 | VERIFIED |
| 64 | US12296849B2 | US Patent 2024 | Various | 2024 | VERIFIED |
| 65 | WO1994029983A1 | WIPO 1994 | Various | 1994 | VERIFIED |"""
    },
]

# ----------------------------------------------------------------------
# 3. Full Bibliographic Entries Additions
# ----------------------------------------------------------------------
FULL_ENTRIES_ADDITIONS = [
    {
        "source": "05_archive/update_refs.py",
        "content": """### [27] RAIL

Title: Recoverability-Aware Intervention Learning
Authors: [Authors]
Venue: arXiv preprint, 2026
arXiv: 2608.05080

IEEE format:
  [Authors], "Recoverability-Aware Intervention Learning," arXiv preprint arXiv:2608.05080, 2026.

Claim alignment: Discloses recoverability-aware intervention learning. Level 1 — verified.

### [28] PAINT

Title: When to Ask for Help: Proactive Interventions in Autonomous RL
Authors: [Authors]
Venue: ICML 2022
arXiv: N/A

IEEE format:
  [Authors], "When to Ask for Help: Proactive Interventions in Autonomous RL," in Proc. ICML, 2022.

Claim alignment: Reversibility estimation + proactive intervention. Candidate 2. Level 1 — verified.

### [29] Doyle 1979 (TMS)

Title: A Truth Maintenance System
Authors: Jon Doyle
Venue: Artificial Intelligence, Vol. 12, pp. 231-272, 1979

IEEE format:
  J. Doyle, "A Truth Maintenance System," Artif. Intell., vol. 12, no. 3, pp. 231-272, 1979.

Claim alignment: Justification-based belief revision. Candidate 4. Level 1 — verified.

### [30] de Kleer 1986 (ATMS)

Title: An Assumption-based TMS
Authors: Johan de Kleer
Venue: Artificial Intelligence, Vol. 28, No. 2, pp. 127-162, 1986

IEEE format:
  J. de Kleer, "An Assumption-based TMS," Artif. Intell., vol. 28, no. 2, pp. 127-162, 1986.

Claim alignment: Assumption-based truth maintenance. Candidate 4. Level 1 — verified.

### [31] BLIP

Title: BLIP: Minimal verifiable provenance for black-box LLMs
Authors: [Authors]
Venue: arXiv preprint, 2026
arXiv: 2608.25210

IEEE format:
  [Authors], "BLIP: Minimal verifiable provenance for black-box LLMs," arXiv preprint arXiv:2608.25210, 2026.

Claim alignment: Minimal verifiable provenance for black-box LLMs. Candidate 5. Level 1 — verified.

### [32] Gupta/Mumick 1993 (IVM)

Title: Maintaining Views Incrementally
Authors: Ashish Gupta, Inderpal Singh Mumick, V.S. Subrahmanian
Venue: SIGMOD 1993

IEEE format:
  A. Gupta, I. S. Mumick, and V. S. Subrahmanian, "Maintaining Views Incrementally," in Proc. SIGMOD, 1993.

Claim alignment: Incremental view maintenance. Candidate 6. Level 1 — verified.

### [33] ERR

Title: Recoverability Has a Law: The ERR Measure for Tool-Augmented Agents
Authors: [Authors]
Venue: arXiv preprint, 2026
arXiv: 2601.22352

IEEE format:
  [Authors], "Recoverability Has a Law: The ERR Measure for Tool-Augmented Agents," arXiv preprint arXiv:2601.22352, 2026.

Claim alignment: ERR measure for tool-augmented agents. Level 1 — verified.

### [34] RTDR

Title: Real-Time Detection and Repair of LLM Agent Failures
Authors: [Authors]
Venue: arXiv preprint, 2026
arXiv: 2608.02464

IEEE format:
  [Authors], "Real-Time Detection and Repair of LLM Agent Failures," arXiv preprint arXiv:2608.02464, 2026.

Claim alignment: Real-time detection and repair. Level 1 — verified."""
    },
    {
        "source": "05_archive/update_refs2.py",
        "content": """### [35] Verified Tool Calls

Title: Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures
Authors: Isham Kalappurackal Mansoor, Abhishek Phadke, Pratip Rana
Venue: arXiv preprint, 2026
arXiv: 2608.02645

IEEE format:
  I. K. Mansoor, A. Phadke, and P. Rana, "Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures," arXiv preprint arXiv:2608.02645, 2026.

Claim alignment: Addresses non-atomic tool failures via postcondition verification. Level 1 — verified.

### [36] PlanFence

Title: Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory
Authors: Evan Chen, Shiqiang Wang, Christopher G. Brinton
Venue: arXiv preprint, 2026
arXiv: 2609.03340

IEEE format:
  E. Chen, S. Wang, and C. G. Brinton, "Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory," arXiv preprint arXiv:2609.03340, 2026.

Claim alignment: Validates specific records to prevent stale-plan execution. Level 1 — verified.

### [37] FreshCtx

Title: FreshCtx: Runtime freshness guard
Authors: Hyperwise-LLC
Venue: Open Source / GitHub, 2026

IEEE format:
  Hyperwise-LLC, "FreshCtx: Runtime freshness guard," GitHub repository, 2026.

Claim alignment: Prevents AI agents from executing actions based on stale evidence. Level 1 — verified.

### [38] Sparse-Evidence Alerting

Title: Sparse-Evidence Early-Alerting
Authors: [Authors]
Venue: arXiv preprint, 2026

IEEE format:
  [Authors], "Sparse-Evidence Early-Alerting," arXiv preprint, 2026.

Claim alignment: Early failure prediction based on sparse evidence. Level 1 — verified."""
    },
    {
        "source": "05_archive/update_refs3.py",
        "content": """### [39] E-valuator

Title: E-valuator: Reliable Agent Verifiers with Sequential Hypothesis Testing
Authors: [Authors]
Venue: arXiv preprint, 2025
arXiv: 2512.03109

IEEE format:
  [Authors], "E-valuator: Reliable Agent Verifiers with Sequential Hypothesis Testing," arXiv preprint arXiv:2512.03109, 2025.

Claim alignment: Converts black-box verifier scores into a decision rule with provable false alarm rate control using sequential hypothesis testing (e-processes). Level 1 — verified.

### [40] Silent Semantic Violations

Title: Demystifying and Checking Silent Semantic Violations in Large Distributed Systems
Authors: [Authors]
Venue: OSDI 2022

IEEE format:
  [Authors], "Demystifying and Checking Silent Semantic Violations in Large Distributed Systems," in Proc. OSDI, 2022.

Claim alignment: Identifies failures where systems break semantic guarantees without apparent anomalies or error signals. Level 1 — verified."""
    },
    {
        "source": "05_archive/update_refs4.py",
        "content": """### [41] Crab

Title: Crab: Checkpoint-and-Restore for Agent SandBoxes
Authors: [Authors]
Venue: arXiv preprint, 2025

IEEE format:
  [Authors], "Crab: Checkpoint-and-Restore for Agent SandBoxes," arXiv preprint, 2025.

Claim alignment: OS-visible state minimization (87% reduction). Level 1 — verified.

### [42] HORMA

Title: HORMA: Hierarchical Organize-and-Retrieve Memory Agent
Authors: [Authors]
Venue: arXiv preprint, 2026

IEEE format:
  [Authors], "HORMA: Hierarchical Organize-and-Retrieve Memory Agent," arXiv preprint, 2026.

Claim alignment: Hierarchical memory for context minimization. Level 1 — verified.

### [43] PABU

Title: PABU: Progress-Aware Belief Update
Authors: [Authors]
Venue: arXiv preprint, 2026

IEEE format:
  [Authors], "PABU: Progress-Aware Belief Update," arXiv preprint, 2026.

Claim alignment: Task-relevant context minimization. Level 1 — verified.

### [44] SkillTV-Bench

Title: SkillTV-Bench
Authors: [Authors]
Venue: arXiv preprint, 2026

IEEE format:
  [Authors], "SkillTV-Bench," arXiv preprint, 2026.

Claim alignment: Flagged as Unverified (Level 3).

### [45] Evo-Bench

Title: Evo-Bench
Authors: [Authors]
Venue: arXiv preprint, 2026

IEEE format:
  [Authors], "Evo-Bench," arXiv preprint, 2026.

Claim alignment: Flagged as Unverified (Level 3).

### [46] State Saturation Trap

Title: State Saturation Trap
Authors: [Authors]
Venue: arXiv preprint, 2026

IEEE format:
  [Authors], "State Saturation Trap," arXiv preprint, 2026.

Claim alignment: Flagged as Unverified (Level 3)."""
    },
    {
        "source": "05_archive/update_refs5.py",
        "content": """### [47] Semantic Checkpointing Mechanisms

Title: Semantic Checkpointing Mechanisms for Stateless LLM Agents
Authors: [Authors]
Venue: 2025

### [48] Weakly Supervised Alerting

Title: When Evidence is Sparse: Weakly Supervised Early Failure Alerting in Dialogs and LLM-Agent Trajectories
Authors: [Authors]
Venue: arXiv preprint, 2026

### [49] Monitoring Web Agents Without Internal Signals

Title: Monitoring Web Agents Without Internal Signals: Observable Trajectories and Key-Step Supervision
Authors: [Authors]
Venue: arXiv preprint, Sept 2026

### [50] AgentTrajectorySentinel

Title: AgentTrajectorySentinel
Authors: [Authors]
Venue: Hugging Face Space / Technical Notes, 2026

### [51] DECIDER

Title: DECIDER (Model Disagreement)
Authors: [Authors]
Venue: 2026

### [52] DA-LCE

Title: Difficulty-Aware Learning Curve Extrapolation
Authors: [Authors]
Venue: AAAI 2026

### [53] US20110161048A1

Title: Threshold-violation-from-baseline-deviation
Authors: [Inventors]
Venue: US Patent Application, 2011"""
    },
    {
        "source": "05_archive/update_refs6.py",
        "content": """### [54] CoAgent

Title: CoAgent: Concurrency Control for Multi-Agent Systems
Authors: [Authors]
Venue: arXiv preprint, 2026

### [55] DPBench

Title: DPBench: Structural Determinants of Multi-Agent LLM Coordination Under Simultaneous Resource Contention
Authors: Hasan & BusiReddyGari
Venue: arXiv preprint, 2026

### [56] Semantic Consensus (SCF)

Title: Semantic Consensus Framework
Authors: [Authors]
Venue: arXiv preprint, 2026

### [57] TOCTOU / idempotency-key

Title: TOCTOU and Idempotency-Key Literature
Authors: Various
Venue: Foundational systems research"""
    },
    {
        "source": "05_archive/update_refs7.py",
        "content": """### [58] US12441366B2

Title: Task-relevant failure detection for trajectory prediction in machines
Authors: Nvidia
Venue: US Patent, 2025

### [59] US12202518B2

Title: Safety decomposition architecture for autonomous machine applications
Authors: Nvidia
Venue: US Patent, 2025

### [60] US20230192139A1

Title: Method and system for addressing failure in an autonomous agent
Authors: Various
Venue: US Patent Application, 2023

### [61] US63/841,017

Title: System and Method for Predictive Failure Detection in AI Agent Workflows
Authors: PredictAgent
Venue: US Patent Application (Pending)

### [62] US20200174481A1

Title: Probabilistic risk assessment for trajectory evaluation
Authors: Waymo
Venue: US Patent Application, 2020

### [63] US12450494B1

Title: Validating autonomous artificial intelligence (AI) agents using generative AI
Authors: Various
Venue: US Patent, 2025

### [64] US12296849B2

Title: Method and system for feasibility-based operation of an autonomous agent
Authors: Various
Venue: US Patent, 2024

### [65] WO1994029983A1

Title: Performance monitoring and failure isolation in communications networks
Authors: Various
Venue: WIPO Patent Application, 1994"""
    },
]

# ----------------------------------------------------------------------
# 4. Capability and Verification Prior Art Tables
# ----------------------------------------------------------------------
USER_TABLE_ADDITIONS = [
    {
        "source": "05_archive/update_refs4.py",
        "content": """\n\n## Capability and Verification Candidates\n
| Candidate                          | Mechanism Investigated                                   | Directly Verified References                             | Exact Collision                                       | Remaining Uncertainty          | Status     |
| ---------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------- | ------------------------------ | ---------- |
| Semantic checkpointing             | Task-relevant semantic state storage                     | Crab (2025)                                              | OS-visible state minimization, 87% reduction          | None                           | ❌ KILLED   |
| Semantic state minimization        | Minimal sufficient context, progress-dependent retention | Semantic checkpointing (2025), HORMA (2026), PABU (2026) | Task-relevant context, 22.17% token usage             | None                           | ❌ KILLED   |
| Post-restore divergence prediction | Stochastic regeneration + side effects, replay-or-fork   | ACRFence (2026-03)                                       | Records irreversible effects, enforces replay-or-fork | Predictive vs. reactive timing | ❌ KILLED   |
| EvoUndo                            | Effect contracts, recovery verification                  | EvoUndo paper (2025)                                     | Effect-based recovery, contract verification          | None                           | ❌ KILLED   |
| E-valuator                         | Silent semantic violations, task-progress preservation   | E-valuator paper (2025)                                  | Semantic violation detection, progress tracking       | None                           | ❌ KILLED   |
| SkillTV-Bench                      | [Unverified — Level 3]                                   | [Not directly inspected]                                 | [Flagged as unverified]                               | [Level 3 status]               | ⚠️ FLAGGED |
| Evo-Bench                          | [Unverified — Level 3]                                   | [Not directly inspected]                                 | [Flagged as unverified]                               | [Level 3 status]               | ⚠️ FLAGGED |
| State Saturation Trap              | [Unverified — Level 3]                                   | [Not directly inspected]                                 | [Flagged as unverified]                               | [Level 3 status]               | ⚠️ FLAGGED |
| [Ninth axis]                       | [Specify]                                                | [Specify]                                                | [Specify]                                             | [Specify]                      | [Status]   |"""
    },
    {
        "source": "05_archive/update_refs5.py",
        "content": """## Capability and Verification Candidates

| Candidate                          | Mechanism Investigated                                   | Directly Verified References                             | Exact Collision                                       | Remaining Uncertainty          | Status     |
| ---------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------- | ------------------------------ | ---------- |
| 1. Intervention-conditioned future-capability preservation | Estimate Ĉ_π(T_I(Z_t),G) without executing intervention | EvoUndo (2608.25210), AgentRewind, DreamGuard, CORA/ToolChain-CRC | Joint elements disclose all components except unexecuted estimation; that gap is obvious mechanical substitution (swap training label, reuse known estimator/gate) | None significant | ❌ KILLED |
| 2. Recovery-Option Preservation / Recovery Frontier | Preserve future recovery/control options; safety boundary crossing | Viability kernels, reachability-based safety, control-barrier functions (classical control theory); PAINT | Structurally identical to decades-old control-theory primitive | None significant | ❌ KILLED |
| 3. Capability-Gap Diagnosis | Diagnose specific capability deficit causing failure | — | No ground-truth deficit labels exist in dataset (unfalsifiable); live-execution testing required is out of project scope | Feasibility, not prior art | ❌ KILLED |
| 4. Decision-Support Integrity / selective revalidation | Justification/dependency graph, invalidate only affected subgraph | Doyle (1979) TMS, de Kleer (1986) ATMS | Identical computational pattern to classical Truth Maintenance Systems | None significant | ❌ KILLED |
| 5. Minimal observable support / provenance | Minimal sufficient subset of evidence supporting an LLM output/action | Database why-provenance/witness theory; BLIP (2608.25210, verified) | BLIP discloses minimal-subset-for-black-box-LLM-output as its core contribution | None significant | ❌ KILLED |
| 6. Action-Admissibility Invariance | Minimal recomputation needed after state change | Gupta/Mumick/Subrahmanian (1993) Incremental View Maintenance | Identical delta-recomputation objective | None significant | ❌ KILLED |
| 7. Semantic Execution Checkpointing / state minimization | Determine necessary/reconstructable/disposable agent state | Crab, StateFork/Waypoint, EvoUndo, 2025 "Semantic Checkpointing Mechanisms for Stateless LLM Agents", HORMA, PABU | Crab: 87% checkpoint-traffic reduction via semantics-aware selection; semantic checkpointing literature already stores task-relevant meaning; HORMA/PABU already do minimal-sufficient-context retention | None significant | ❌ KILLED |
| 8. Post-restore action divergence prediction | Predict whether regenerated action diverges from checkpoint-time action before restoration | ACRFence | ACRFence already performs reactive replay-or-fork detection of exactly this divergence; predictive framing is an obvious timing shift | None significant | ❌ KILLED |
| 9. dyn_comp as generic mechanism / residual-risk decomposition | Static-vs-dynamic model subtraction + threshold | Biostatistics landmarking/dynamic-prediction literature; general residual-anomaly-scoring patent (video anomaly detection); RAIL (2608.05080, verified — different domain, not direct collision); Weakly Supervised Early Failure Alerting; "Monitoring Web Agents Without Internal Signals" (Sept 2026); AgentTrajectorySentinel; DECIDER (model disagreement); DA-LCE (difficulty conditioning); US20110161048A1 (2011, threshold-violation-from-baseline-deviation, granted patent) | Individual components (partial-prefix prediction, difficulty conditioning, residual/deviation scoring, FAR-constrained thresholding) each independently disclosed across multiple recent and older references; obviousness-by-combination risk is substantial even though no single reference discloses the exact combination verbatim | Exact combination not found disclosed verbatim; formal legal obviousness determination not made | NARROW CANDIDATE — SUBSTANTIAL RISK, NOT KILLED, NOT CONFIRMED |"""
    },
]

# Helper function to regenerate literature docs if ever needed
def write_literature_files(target_dir=r"01_research/docs/literature"):
    """Optionally writes out all literature files to target directory."""
    os.makedirs(target_dir, exist_ok=True)
    for filename, content in LITERATURE_DOCS.items():
        path = os.path.join(target_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"Successfully wrote {len(LITERATURE_DOCS)} literature files to {target_dir}.")

if __name__ == "__main__":
    print(f"Loaded {len(LITERATURE_DOCS)} literature payloads, {len(TABLE_ADDITIONS)} table blocks, {len(FULL_ENTRIES_ADDITIONS)} entry blocks, {len(USER_TABLE_ADDITIONS)} prior-art blocks.")

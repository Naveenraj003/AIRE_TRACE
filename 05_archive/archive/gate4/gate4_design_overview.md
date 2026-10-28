# Gate 4: AIRE-Trace Design Overview

## Research Objective
To answer the core research question: **Do comparative performance claims for online agent-failure warning methods remain consistent when different methods are evaluated under identical information, target, alert, calibration, lead-time, and compute constraints?** AIRE-Trace standardizes the evaluation protocol for warning methods, shifting the focus from proposing new detector architectures to comparing existing method families (Heuristic, Classical ML, and Sequence-based) fairly under unified operational constraints.

## Scientific Contribution
A standardized, prospective, prefix-only evaluation protocol for online agent-failure warning. The protocol fixes information visibility (checkpoint horizons), failure-target definitions (canonical outcome mapping), alert semantics (eventual failure given a prefix), calibration procedures (FAR constraints), lead-time measurements, and compute accounting. The system produces a rigorous Pairwise Direction Consistency (PDC) ranking stability analysis to quantify how sensitive comparative claims are to specific evaluation metrics.

## System Overview
AIRE-Trace is an evaluation harness and methodology, not a standalone foundation model. It includes:
1. **Data Ingestion & Normalization**: Translates raw Tracebench (TerminalBench) and τ²-Bench trajectories into canonical formats.
2. **Leakage-Safe Preprocessing**: Generates episode-symmetric, outcome-independent prefixes (e.g., $t \in [1, \min(T_i, 30)]$) while strictly sanitizing terminal outcome leakage.
3. **Method Families**: Wraps heuristic (H), tabular machine learning (M), and temporal sequence models (S) into a unified inference and evaluation contract.
4. **Calibration & Evaluator**: Isolates threshold calibration to the CALIBRATION split to maximize recall subject to a 5% FAR target. The evaluator computes both prospective metrics (Mode A on TerminalBench) and eventual-outcome diagnostics (Mode B on τ²-Bench).
5. **Statistical Layer**: Employs episode-cluster bootstrapping to generate valid confidence intervals and conducts the primary metric-sensitivity analysis (PDC).

## Assumptions
- **Hardware Constraints**: The system must run on an RTX 2050 (4GB VRAM). The sequence model (S) must be a lightweight GRU/1D-CNN, not a massive transformer.
- **Data Availability**: The TerminalBench dataset provides sufficient training data and failure-onset annotations to support the primary Mode A evaluation. τ²-Bench serves strictly as a Mode B evaluation-only diagnostic.
- **Protocol Immutability**: Rules 1-11 of the frozen protocol are non-negotiable. Code must enforce these rules, not just document them.
- **Threshold Validity**: The CALIBRATION set is representative enough to select stable operating points for the TEST set.

## Constraints
- **Zero Data Leakage**: No test data or post-onset data from failed episodes can influence training, threshold selection, or model selection. Terminal events must be fully sanitized.
- **Episode-Level Statistics**: All statistical tests, aggregation metrics (via episode-balanced weighting), and false-alarm calculations must be tied to the episode, never the prefix.
- **Cost Limitations**: Zero paid API usage. Only local execution is permitted for all mandatory methods.

## Out-of-Scope
- Proposing a new foundation model or state-of-the-art detector as the headline contribution.
- Exact reproduction of PrefixGuard, AgentForesight, or Trajectory Guard.
- Expanding beyond the two datasets (TerminalBench, τ²-Bench) or adding more than the 3 mandatory + 1 optional method families.
- Building a multi-user, public-facing hosted dashboard.
- Any claims of being "first" or that prior methods are fundamentally "wrong."

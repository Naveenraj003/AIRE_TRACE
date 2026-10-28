# Detecting Silent Failures in Multi-Agentic AI Trajectories (Nov 2025)

**Category:** Failure Warning / Monitoring Systems
**arXiv:** [2511.04032](https://arxiv.org/abs/2511.04032)
**Published:** November 2025

---

## What the Paper Is

Introduces the **task of anomaly detection in multi-agentic AI trajectories** as a formal research problem (first systematic study). Targets "silent failures" — drift, cycles, and missing details in outputs — which are difficult to detect because they don't produce hard errors.

### Contributions
1. A **dataset curation pipeline** capturing user behavior, agent non-determinism, and LLM variation
2. Two benchmark datasets: **4,275 trajectories** (primary) and **894 trajectories** (secondary), from real multi-agentic systems
3. Benchmarking of anomaly detection methods:
   - **Supervised XGBoost**: up to **98% accuracy**
   - **Semi-supervised SVDD**: up to **96% accuracy**
   - Comparable performance between the two approaches

## What It Solves

- Provides the first public benchmark datasets specifically for anomaly detection in multi-agent AI trajectories
- Demonstrates that silent failures are detectable with high accuracy even without step-level labels
- Establishes a baseline methodology for evaluating anomaly detection approaches

## What It Lacks

- Focuses on relatively simple anomaly types (drift, cycles) — does not handle complex cascading failures
- Datasets are from specific multi-agent architectures; generalizability is unclear
- 98% accuracy is on a labeled dataset — real-world deployment performance would likely be lower
- Does not address cross-agent or cross-framework transfer
- No calibrated false-alarm control; pure accuracy metrics

## Relevance to AIRE-TRACE

- Our project targets similar silent failures but goes further: prefix-level detection, calibrated thresholds, and cross-dataset transfer
- The SVDD (Support Vector Data Description) approach is a one-class method — compatible with our Rule (train H/M/S/L only on healthy/successful prefixes, not post-onset failure data)
- Their dataset (4,275 trajectories) is smaller than what AIRE-TRACE targets from TerminalBench + τ²-Bench combined
- **Key gap we address**: this paper has no calibration, no threshold control, no mode labeling — AIRE-TRACE explicitly handles all three
- Datasets could potentially be used as an external evaluation corpus (subject to license and our split rules)

---

## Key Terms
`silent failures` · `drift` · `cycle detection` · `SVDD` · `XGBoost` · `anomaly detection` · `multi-agent`

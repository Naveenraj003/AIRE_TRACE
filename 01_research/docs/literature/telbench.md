# OAT: Tracing Agentic Failure from the Flow of Success (July 2026)
# → Already stored in oat_tracing_failure.md

# TELBench: Where Do Deep-Research Agents Go Wrong? Span-Level Error Localization (June 2026)

**Category:** Benchmarks / Datasets — Contrastive Learning / Trajectory Representations
**arXiv:** [2606.02060](https://arxiv.org/abs/2606.02060)
**Published:** June 2026

---

## What the Paper Is

TELBench is a **1,000-instance benchmark** for identifying error spans in deep-research agent trajectories, along with **DRIFT**, a claim-centric auditing framework.

### Data Collection
- 2,790 real trajectories from **2 agent frameworks**, **3 backbone models**, **3 benchmarks**
- Raw logs converted into **semantic spans**
- Error spans annotated via **LLM-assisted expert review**
- 4 span types: normal exploration, failed searches, tentative hypotheses, harmless noise

### DRIFT Framework
- **Claim-centric auditing**: tracks agent claims, checks support in trajectory evidence
- Marks spans where unsupported or conflicting claims affect the answer path
- Improves span-level error localization and **first-error accuracy by up to 30 percentage points**

## What It Solves

- Provides **process-level reliability evaluation** beyond final-answer success rates
- Enables span-level error localization (finer granularity than step-level)
- DRIFT shows that claim tracking outperforms simple step-scoring for deep-research agents

## What It Lacks

- Focused on deep-research agents (search + synthesis) — not general tool-using or CLI agents
- LLM-assisted annotation introduces model bias in labeling
- Span-level granularity is different from step-level granularity used in most other work
- No online/real-time variant — purely post-hoc analysis

## Relevance to AIRE-TRACE

- Span-level localization is more granular than our checkpoint-level evaluation — could inspire a future extension
- DRIFT's claim-tracking approach is relevant for hallucination-type failures in our taxonomy
- The 2,790-trajectory collection methodology (multiple frameworks, models, benchmarks) mirrors our multi-dataset design
- **Key distinction**: TELBench is for deep-research agents; AIRE-TRACE targets general tool-using agents on TerminalBench/τ²-Bench — different but related
- The "harmless noise" span category (not all deviations are failures) is relevant to our sanitization step — we must not flag harmless exploration as onset of failure

---

## Key Terms
`span-level` · `error localization` · `DRIFT` · `claim tracking` · `deep-research agents` · `benchmark`

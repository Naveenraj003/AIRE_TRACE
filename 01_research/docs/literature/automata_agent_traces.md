# Automata from Agent Traces: Failure and Next-Step Prediction (Aug 2026)

**Category:** Failure Warning / Monitoring Systems
**arXiv:** [2608.23670](https://arxiv.org/abs/2608.23670)
**Published:** August 2026

---

## What the Paper Is

Proposes collapsing an entire trace corpus into a single **compact Finite-State Machine (FSM)** that serves as a structural substrate for both:
1. **Next-step prediction** — FSM-state context outperforms Agent Workflow Memory on every ground-truth-matched dataset
2. **Failure prediction** — per-state behavioral features reach held-out AUROC up to **0.94**; an online monitor ranks failing runs above passing ones from a partial trace, triggering early stopping before completion

### Key Results
- FSMs are compact: **7–43 states** across 12 public datasets
- FSMs replay held-out data at **≥0.997 fitness** with near-identical topology across splits
- FSMs build in **milliseconds**
- Behavioral topology appears shaped more by the **deployment harness** than by the LLM → model-agnostic structural primitive

## What It Solves

- Makes agent behavioral structure interpretable and auditable via finite automata
- Provides a unified substrate for both prediction tasks (next-step + failure) without separate architectures
- Offers a model-agnostic approach — the FSM reflects the deployment harness, not the LLM internals

## What It Lacks

- Compression into a single FSM may lose within-episode temporal dynamics for longer/more variable tasks
- Does not provide calibrated false-alarm guarantees
- Fitness ≥ 0.997 is a replay metric, not a causal or interventional measure
- How the FSM handles novel task distributions or out-of-distribution LLMs is not evaluated

## Relevance to AIRE-TRACE

- FSM approach could serve as an alternative monitor architecture alongside our echo-state-network approach
- 7–43 state compactness on typical datasets contrasts with PrefixGuard's 187-state DFA on TerminalBench — suggests our benchmark may be at the complex end of the behavioral spectrum
- AUROC 0.94 is a strong claim that sets a high bar; our protocol needs to evaluate against this on same benchmarks
- The deployment-harness-shaped topology insight is consistent with our Rule 9 (features must be computable identically on both datasets) — FSM nodes represent harness states, not model-specific states

---

## Key Terms
`finite-state machine` · `FSM` · `next-step prediction` · `failure prediction` · `behavioral topology` · `model-agnostic`

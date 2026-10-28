# PrefixGuard: From LLM-Agent Traces to Online Failure-Warning Monitors (May 2026)

**Category:** Failure Warning / Monitoring Systems
**arXiv:** [2605.06455](https://arxiv.org/abs/2605.06455)
**Authors:** Huang et al.
**Published:** May 2026

---

## What the Paper Is

PrefixGuard is a **trace-to-monitor framework** for online failure-warning in LLM agent deployments. It operates in two phases:

1. **Offline — StepView Induction**: Induces deterministic typed-step adapters from raw trace samples, converting heterogeneous trace events into a typed, structured representation
2. **Online — Supervised Monitor Training**: Learns an event abstraction and prefix-risk scorer from terminal outcomes (success/failure labels)

Post-hoc, it can extract compact **Deterministic Finite Automata (DFAs)** from trained monitors for formal/finite-state audit.

### Key Results

| Benchmark       | AUPRC  | DFA States |
|-----------------|--------|------------|
| WebArena        | 0.900  | 29         |
| τ²-Bench        | 0.710  | 20         |
| SkillsBench     | 0.533  | 151        |
| TerminalBench   | 0.557  | 187        |

- Average improvement of **+0.137 AUPRC** over raw-text controls
- LLM judges are substantially weaker under the same prefix-warning protocol
- Derives an **observability ceiling** on AUPRC — separating monitor error from failures that leave no evidence in the observed prefix
- "First-alert diagnostics": strong AUROC ranking does not guarantee deployment utility (WebArena ranks well but fails low-false-alarm alerts; τ²-Bench and TerminalBench retain actionable early alerts)

## What It Solves

- Provides a systematic, practical recipe for synthesizing lightweight prefix monitors from raw agent traces without hand-authored schemas
- Enables online (real-time) failure warnings at prefix time, not just post-hoc
- Derives an observability ceiling which bounds what any prefix monitor can achieve (separates monitor quality from fundamental trace opacity)

## What It Lacks

- StepView induction depends on sufficient trace samples; brittle with very small corpora
- DFA becomes large (151–187 states) on complex benchmarks — may not be practically useful for formal audit in those settings
- Does not produce calibrated probability estimates with statistical guarantees (compare to e-valuator)
- No cross-agent transfer experiments — unclear whether monitors trained on one agent transfer to another
- AUPRC on SkillsBench and TerminalBench (0.533, 0.557) is only marginally better than chance

## Relevance to AIRE-TRACE

- **Critical reference**: PrefixGuard is a primary baseline system our protocol explicitly mentions (Rule 7: never pool PrefixGuard literature-reported numbers with locally measured numbers as if directly comparable)
- The AUPRC numbers on τ²-Bench and TerminalBench are the key literature baselines AIRE-TRACE must beat or match and cite separately
- The **observability ceiling** concept is directly relevant — we need to compute this for our benchmark to bound expectations
- PrefixGuard's typed-step abstraction (StepView) is conceptually similar to our canonical schema; the comparison will be a key positioning argument
- DFA compactness on τ²-Bench (20 states) suggests the benchmark may have less behavioral diversity than TerminalBench (187 states) — important for our split/checkpoint design

---

## Key Terms
`prefix monitor` · `StepView` · `AUPRC` · `DFA extraction` · `observability ceiling` · `online failure warning`

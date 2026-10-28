# TRACES: Proactive Safety Auditing for Multi-Turn LLM Agents (May 2026)

**Category:** Failure Warning / Monitoring Systems
**arXiv:** [2605.27690](https://arxiv.org/abs/2605.27690)
**Published:** May 2026

---

## What the Paper Is

TRACES is a **representation-based proactive auditor** that learns **prefix-level trajectory risk states** from the **hidden representations** of an observer LLM. Unlike detection methods that operate on observable events, TRACES works on LLM internals.

### Key Design Choices
- Induces **latent mechanism features** from per-step hidden representations of an observer LLM
- Models their **temporal evolution** to estimate whether a partial trajectory is drifting toward unsafe behavior
- Trained with **weak trajectory-level supervision** (not step-level risk annotations) → produces dense prefix-level risk estimates
- These risk states can also **guide safer agent training** (not just auditing)

### Results
- Improves both full-trajectory safety prediction and **proactive risk discrimination** across multiple agent safety benchmarks

## What It Solves

- Enables **proactive** (rather than reactive/post-hoc) safety auditing during trajectory unfolding
- Sidesteps the cost of step-level risk annotation by using weak supervision
- Links auditing to training: risk states can help train a safer agent

## What It Lacks

- Requires access to **internal LLM hidden representations** of the observer model — not available for black-box APIs
- Observer LLM adds computational cost at every step (unlike sub-millisecond monitors)
- Focuses primarily on safety/unsafe behavior, not general task failure modes (tool misuse, hallucination, etc.)
- The weak supervision approach may miss subtle step-level failure points

## Relevance to AIRE-TRACE

- **Major distinction**: AIRE-TRACE uses observable step telemetry only (consistent with black-box deployment); TRACES requires internal representations → different applicability regime
- TRACES's temporal evolution modeling is conceptually similar to our echo-state-network's memory of sequential states
- The weak-supervision approach (trajectory-level labels → prefix-level estimates) directly parallels our H/M/S/L monitor training from terminal outcomes
- **Important constraint reminder**: our Rule 2 prohibits features at checkpoint `t` depending on events with `step_index > t` — TRACES's architecture should be checked against this when comparing
- The "proactive vs. reactive" framing is consistent with our Mode A (TerminalBench) vs. Mode B (τ²-Bench) evaluation design

---

## Key Terms
`proactive auditing` · `hidden representations` · `weak supervision` · `trajectory risk states` · `safety auditing` · `prefix-level`

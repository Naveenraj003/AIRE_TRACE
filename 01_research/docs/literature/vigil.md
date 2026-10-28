# VIGIL: A Reflective Runtime for Self-Healing LLM Agents (Oct 2025)

**Category:** Failure Warning / Monitoring Systems
**arXiv:** [2512.07094](https://arxiv.org/abs/2512.07094)
**Published:** October 2025 (submitted Dec 2025)

---

## What the Paper Is

VIGIL (Verifiable Inspection and Guarded Iterative Learning) is a **reflective runtime** that supervises a sibling agent and performs **autonomous maintenance** rather than task execution. It is a meta-level self-repair system rather than a detection-only monitor.

### Architecture
- Ingests **behavioral logs** and appraises each event into a structured **emotional representation** (EmoBank)
- Maintains an **EmoBank** with decay and contextual policies
- Derives an **RBT (Reflection Behavior Tree) diagnosis** sorting recent behavior into: Strengths, Opportunities, Failures
- Generates **guarded prompt updates** (preserving core identity semantics) and **read-only code proposals**
- Uses a **state-gated pipeline** — illegal transitions produce explicit errors rather than LLM improvisation

### Demonstrated Capability
- In a reminder latency case study: identified elevated lag, proposed prompt and code repairs, and when its own diagnostic tool failed (schema conflict), surfaced the internal error, produced a fallback diagnosis, and emitted a repair plan → **meta-level self-repair**

## What It Solves

- Enables self-healing without human intervention for identified failure modes
- Introduces the concept of **meta-level self-repair** in deployed agent runtimes
- Uses structured emotional representation to capture qualitative behavioral degradation patterns
- State-gated pipeline prevents the LLM from hallucinating state transitions during diagnosis

## What It Lacks

- **Evaluated only on a single case study** (reminder latency) — very limited empirical validation
- The EmoBank / "emotional representation" framing is novel but not well-grounded in existing ML theory
- No benchmark comparison; no AUROC, AUPRC, or F1 numbers
- Self-repair actions (prompt updates, code proposals) are not validated for correctness or safety
- Scalability to complex, multi-step task agents is undemonstrated

## Relevance to AIRE-TRACE

- VIGIL represents the **repair layer** of the detection-repair pipeline; AIRE-TRACE focuses primarily on reliable detection (the prerequisite for repair)
- Our echo-state-network + CUSUM alarms + rollback-repair (from RT Detection paper) is a simpler, more empirically validated repair pipeline
- VIGIL's "guarded prompt updates" is conceptually related to our post-alert intervention design — but VIGIL does not have the statistical rigor we require
- A key contrast for our paper: VIGIL requires a sibling agent runtime (expensive) vs. AIRE-TRACE's μs-scale monitors
- The RBT diagnosis (Strengths, Opportunities, Failures) is reminiscent of failure taxonomy — could be cited when motivating our failure categorization approach

---

## Key Terms
`self-healing` · `reflective runtime` · `EmoBank` · `meta-level repair` · `state-gated pipeline` · `behavioral logs`

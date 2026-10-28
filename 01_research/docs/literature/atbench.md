# ATBench: A Diverse and Realistic Agent Trajectory Benchmark for Safety Evaluation and Diagnosis (Apr 2026)

**Category:** Benchmarks / Datasets
**arXiv:** [2604.02022](https://arxiv.org/abs/2604.02022)
**Published:** April 2026
**Authors:** Li, Yu et al.
**Ref ID:** [B3]

---

## What the Paper Is

ATBench is a **trajectory-level benchmark** for structured, diverse, and realistic evaluation of **agent safety**. It addresses three key limitations of existing trajectory-level benchmarks: insufficient interaction diversity, coarse observability of safety failures, and weak long-horizon realism.

### Key Stats
- **1,000 trajectories** (503 safe, 497 unsafe)
- **Averaging 9.01 turns**, 3.95k tokens per trajectory
- **1,954 invoked tools** from pools spanning **2,084 available tools**
- **Long-context delayed-trigger protocol**: risk emerges across multiple stages, not just at a single step

### Three-Dimensional Risk Taxonomy
1. **Risk Source** — where the risk originates (user instruction, tool output, environment)
2. **Failure Mode** — how the failure manifests (instruction violation, hallucination, invalid invocation, etc.)
3. **Real-World Harm** — the downstream consequence of the failure

### Quality Controls
- Rule-based + LLM-based filtering
- Full human audit of all 1,000 trajectories

### Evaluation Results
- Challenging even for frontier LLMs (GPT-5 variants, Claude models)
- Enables taxonomy-stratified analysis and cross-benchmark comparison

## What It Solves

- Provides a richly annotated, human-audited benchmark for structured agent safety evaluation
- The three-dimensional taxonomy enables fine-grained analysis of failure patterns
- Delayed-trigger protocol captures realistic multi-step risk emergence

## What It Lacks

- Focused on **safety** failures specifically (harmful actions, policy violations) — not general task-completion failures
- 1,000 trajectories is modest for training monitors; primarily a test benchmark
- No online/real-time evaluation protocol; post-hoc only
- Tool pool diversity (2,084 tools) may not generalize to CLI-only or API-only environments

## Relevance to AIRE-TRACE

- ATBench's **three-dimensional taxonomy** could be used to extend our failure categorization beyond simple success/failure
- The **delayed-trigger protocol** is relevant to our onset-anchored analysis (Rule 1 prohibits onset-anchored checkpoints) — ATBench's protocol of multi-stage risk is exactly what makes onset detection hard
- Could serve as a **third evaluation corpus** alongside TerminalBench and τ²-Bench for cross-domain transfer analysis
- ATBench's human audit methodology could validate our sanitization invariant (Rule 6)
- **Priority 7 enhancement**: Cross-domain transfer analysis would include ATBench; however, ATBench's safety focus differs from our general failure-monitoring focus — must label separately

---

## Key Terms
`safety benchmark` · `three-dimensional taxonomy` · `delayed-trigger` · `trajectory-level` · `long-horizon` · `risk emergence`

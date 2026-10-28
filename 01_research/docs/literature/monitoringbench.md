# MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring (May 2026)

**Category:** Benchmarks / Datasets — Adversarial Robustness
**arXiv:** [2605.09684](https://arxiv.org/abs/2605.09684)
**Published:** May 2026
**Ref ID:** [B4]

---

## What the Paper Is

MonitoringBench introduces a **semi-automated red-teaming methodology** exposing harder-to-catch attacks for coding-agent monitors. It produces a benchmark of **2,644 attack trajectories** for evaluating monitor capabilities and failure modes in the BashArena (AI control) setting.

### Three Key Challenges Addressed
1. **Mode collapse in attack generation** → solved with a novel attack taxonomy for broader coverage
2. **Conceive-execute gap**: frontier LLMs can propose strong attack ideas OR execute them, not both → solved by decomposing into strategy generation + execution + post-hoc trajectory refinement
3. **Manual elicitation costs** → solved with semi-automated pipeline

### Results
- Opus-4.5 monitor catch rate: **94.9%** on elicited-only attacks → **60.3%** on best refined attacks (large drop)
- Attacks generalize across monitors: attacks optimized against 3 dev monitors generalize to 10 held-out monitors
- **Frontier monitors detect suspicious actions but fall for persuasion** or fail to calibrate suspiciousness scores appropriately

### Key Finding
> "Frontier monitors often detect suspicious actions but fall for persuasion" — monitors are behaviorally pattern-matching, not reasoning about intent.

## What It Solves

- Provides a rigorous, standardized adversarial benchmark for agent monitors
- Reveals systematic weaknesses of current monitors under adversarial conditions
- Semi-automated methodology can be refreshed as agents/monitors improve

## What It Lacks

- Focused on **coding agents in BashArena** (AI control setting) — not general task-failure monitors
- Adversarial trajectories are a specific subset of failures; our monitors must handle natural (non-adversarial) failures first
- The attack taxonomy may not cover all failure modes in AIRE-TRACE's scope

## Relevance to AIRE-TRACE

- MonitoringBench represents an **adversarial robustness evaluation** that AIRE-TRACE does not currently address (Gap 3 in the research gap analysis)
- The persuasion susceptibility finding suggests our monitors should include semantic consistency checks, not just pattern matching on telemetry
- The 60.3% catch rate under strong attacks (vs. 94.9% on easy attacks) quantifies the robustness gap — this is the range within which our AIRE-TRACE monitors will be tested
- **Priority 5 (adversarial evaluation)**: Evaluating AIRE-TRACE on MonitoringBench-style attacks would directly address this gap
- Our deterministic verification layer is specifically resistant to persuasion-type attacks (it checks tool outputs deterministically, not based on natural language claims)
- **Limitation note**: MonitoringBench's BashArena is a subset of TerminalBench tasks — evaluating AIRE-TRACE on it is feasible

---

## Key Terms
`red-teaming` · `adversarial trajectories` · `monitor robustness` · `attack taxonomy` · `BashArena` · `persuasion attacks`

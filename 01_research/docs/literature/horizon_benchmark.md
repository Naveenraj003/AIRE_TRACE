# HORIZON: Cross-Domain Diagnostic Benchmark for Long-Horizon Agent Failures (Apr 2026)

**Category:** Benchmarks / Datasets
**arXiv:** [2604.11978](https://arxiv.org/abs/2604.11978)
**Published:** April 2026
**Leaderboard:** https://xwang2775.github.io/horizon-leaderboard/
**Ref ID:** [B5]

---

## What the Paper Is

HORIZON is a **cross-domain diagnostic benchmark** for systematically studying long-horizon failure behaviors in LLM-based agents, with a focus on **horizon-dependent degradation patterns**.

### Key Stats
- **3,100+ trajectories** across **4 representative agentic domains**
- Evaluates state-of-the-art agents: GPT-5 variants and Claude models
- Uses a **trajectory-grounded LLM-as-a-Judge pipeline** for scalable, reproducible failure attribution
- **Human validation**: inter-annotator κ=0.61; human-judge κ=0.84 agreement

### Key Findings
- LLM agents perform strongly on short/mid-horizon tasks but **break down on long-horizon tasks** requiring extended, interdependent action sequences
- Long-horizon failures are **poorly characterized** in existing work → principled diagnosis has been lacking
- Cross-domain analysis enables identification of **horizon-specific failure patterns** vs. task-type-specific patterns

## What It Solves

- Provides a systematic methodology for diagnosing long-horizon agent failures across multiple domains
- Trajectory-grounded LLM-as-Judge pipeline achieves high human agreement (κ=0.84) for scalable annotation
- Enables cross-domain comparison and horizon-dependent degradation analysis

## What It Lacks

- No online/real-time monitoring component — post-hoc diagnostic only
- LLM-as-Judge pipeline still depends on LLM quality and alignment
- The 4 agentic domains may not cover CLI/terminal environments specifically
- 3,100+ trajectories is a good size but biased toward frontier model behaviors

## Relevance to AIRE-TRACE

- HORIZON's **cross-domain diagnostic** approach validates our Mode A vs. Mode B separation (TerminalBench ≠ τ²-Bench — they have different failure patterns)
- The **horizon-dependent degradation** finding is directly relevant to our post-onset prefix analysis: failures in longer trajectories may be detectable earlier as a function of horizon length
- HORIZON's LLM-as-Judge pipeline (κ=0.84) sets a benchmark for ground truth quality — our deterministic state-based verification on TerminalBench achieves "perfect" agreement (deterministic), which is better
- **Priority 7 (cross-domain transfer)**: HORIZON is a natural third benchmark for AIRE-TRACE alongside TerminalBench and τ²-Bench
- 3,100+ trajectories provides significantly more data than TerminalBench (89 tasks) — episode-level split would give many more TRAIN examples
- The LLM-as-Judge pipeline could be adapted to provide ground truth for AIRE-TRACE cases where deterministic verification is unavailable

---

## Key Terms
`long-horizon failures` · `cross-domain` · `trajectory-grounded LLM-as-Judge` · `horizon-dependent degradation` · `diagnostic benchmark`

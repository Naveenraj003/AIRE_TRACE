# Wang et al. — A Survey for LLM Agent Trajectory Analysis (2026)

**Category:** Survey Papers (Foundational)
**Published:** IEEE Transactions on Software Engineering, 2026
**Authors:** Junjie Wang et al.
**Link:** [computer.org](https://computer.org)

---

## What the Paper Is

A comprehensive survey of the rapidly evolving field of LLM-based agent trajectory analysis, covering literature from early 2025 through April 2026. The survey is organized along **five primary dimensions**:

1. **Failure Taxonomy** — Classification of failure types in LLM agent systems (tool misuse, hallucination, plan drift, cascading failures, etc.)
2. **Failure Attribution** — Methods for pinpointing responsible agent and decisive error step
3. **System Enhancement & Optimization** — Trajectory-informed repair and improvement techniques
4. **Trajectory Monitoring & Analysis Tools** — Software infrastructure for observing and debugging agent runs
5. **Datasets & Benchmarks** — Evaluation resources for failure attribution and repair

## What It Solves

- Provides the first systematic taxonomy and structured literature map for agent trajectory analysis
- Connects failure attribution to concrete enhancement strategies, making it actionable for practitioners
- Catalogs available benchmarks and identifies gaps (e.g., step-level attribution accuracy remains limited, benchmark diversity is insufficient)
- Traces evolution from simple LLM prompting to causal inference, fine-tuned tracer models, and dynamic intervention

## What It Lacks

- Not empirical — no new method or experiment; purely survey/review
- Coverage limited to pre-April 2026 literature; several key August 2026 papers (DUOTRACE, FailFast, RT-Detection) are not included
- Step-level attribution remains identified as an unsolved open challenge, not resolved in the paper itself
- Lacks direct guidance on calibration, threshold selection, or cross-dataset transfer

## Relevance to AIRE-TRACE

- **High strategic value**: establishes the canonical taxonomy our project should position itself against
- The 5-dimension framework maps well to our own components: prefix monitors → dimension 4, calibration → dimension 3, benchmark evaluation → dimension 5
- Open challenges listed (step-level accuracy, benchmark diversity) are precisely what AIRE-TRACE is designed to address on TerminalBench and τ²-Bench
- The survey's failure taxonomy should be cross-referenced against our `eventual_success`/`eventual_failure` canonical mapping to ensure AIRE-TRACE covers all identified failure modes
- Authors maintain a curated GitHub repository — should be tracked for new additions

---

## Key Terms
`trajectory analysis` · `failure taxonomy` · `failure attribution` · `LLM agents` · `survey`

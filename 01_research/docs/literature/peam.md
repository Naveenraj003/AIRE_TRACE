# PEAM: Parametric Embodied Agent Memory (May 2026)

**Category:** Contrastive Learning / Trajectory Representations
**arXiv:** [2605.27762](https://arxiv.org/abs/2605.27762)
**Published:** May 2026

---

## What the Paper Is

PEAM is a **Parametric Embodied Agent Memory** framework for Minecraft agents that transforms agent memory from inference-time retrieval into **parameter-resident skills** internalized through experience.

### Architecture
- Slow deliberative **LLM** for open-ended reasoning + fast **parametric module** (reflexive execution)
- Fast module: **multimodal Mixture-of-Experts LoRA** with per-category physically isolated adapters → **continual learning without catastrophic forgetting**
- **Failure as first-class training signal**: failure-correction trajectory pairs internalized via **joint behavioral-cloning + contrastive objective** — learns not just what succeeds but how corrected actions differ from failed ones
- **Parameterization-worthiness score**: decides which experience to internalize
- **Scale-free self-triggered consolidation**: decides *when* to internalize without hand-tuned thresholds

## What It Solves

- Avoids catastrophic forgetting in continual learning through physically isolated LoRA adapters
- Makes failure-correction pairs first-class training data via contrastive objective
- Self-triggered consolidation removes need for task-specific threshold tuning

## What It Lacks

- **Minecraft-specific** — embodied, vision-based environment with very different structure from LLM API agents
- Requires continuous interaction with environment for consolidation
- Parametric memory approach requires fine-tuning the agent model itself — not applicable to black-box API agents
- No evaluation on TerminalBench, τ²-Bench, or similar

## Relevance to AIRE-TRACE

- **Low direct applicability** (Minecraft + embodied AI), but methodologically interesting
- The **failure-correction contrastive objective** (learning how corrected actions differ from failed ones) is a potential technique for the repair/enhancement layer after detection
- The **parameterization-worthiness score** is conceptually similar to deciding which failure episodes are worth adding to training — relevant to our active learning extension ideas
- **Important protocol check**: using failure-correction pairs as training signal violates our Rule 8 (never train H/M/S/L on post-onset prefixes of failed episodes) — PEAM is fine for the agent itself, not for our monitors

---

## Key Terms
`parametric memory` · `LoRA` · `continual learning` · `failure-correction pairs` · `contrastive objective` · `Minecraft`

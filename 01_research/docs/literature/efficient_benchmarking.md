# Efficient Benchmarking of AI Agents (March 2026)

**Category:** Evaluation Methodology
**arXiv:** [2603.23749](https://arxiv.org/abs/2603.23749)
**Published:** March 2026
**Ref ID:** [E2]

---

## What the Paper Is

Studies whether **small task subsets can preserve agent rankings** at substantially lower evaluation cost, exploiting that rank-order prediction is more stable than absolute score prediction under distribution shift.

### Key Setup
- 8 benchmarks, 33 agent scaffolds, 70+ model configurations
- Studies **scaffold-driven distribution shift**: performance depends on the framework wrapping the underlying model

### Key Findings
1. **Absolute score prediction degrades** under scaffold-driven distribution shift
2. **Rank-order prediction remains stable** — this asymmetry can be exploited
3. **Mid-range difficulty filter (30–70% historical pass rates)** reduces evaluation tasks by **44–70%** while maintaining high rank fidelity
4. Random sampling exhibits high variance across seeds; mid-range filter is more reliable
5. Greedy task selection underperforms mid-range filter under distribution shift

### Theoretical Basis
- Motivated by **Item Response Theory (IRT)** — tasks with intermediate difficulty most discriminate between agents

## What It Solves

- Dramatic reduction in evaluation cost while preserving ranking accuracy
- Principled task selection for benchmark efficiency
- Demonstrates that leaderboard rankings are robust to scaffold changes even when absolute scores shift

## What It Lacks

- Only studied for task success/failure ranking — not for prefix-level monitoring
- The 44–70% task reduction assumes a stable historical pass-rate distribution
- Does not address within-task episode-level variability

## Relevance to AIRE-TRACE

- **PDC/ranking-stability analysis justification**: this paper directly supports our use of rank-order metrics (PDC) rather than absolute score metrics, since rank-order is stable under distribution shift
- The **scaffold-driven shift** finding implies that absolute AUROC/AUPRC numbers may shift when the same monitor is tested on a different agent framework — our PDC metric is more informative than absolute values across frameworks
- The **mid-range difficulty filter** (30–70% pass rates) is relevant to our checkpoint selection — evaluating at checkpoints where outcomes are genuinely uncertain (not dominated by easy or impossible tasks) gives the most informative signal
- IRT motivation for task selection could be applied to our benchmark: if we have episodes with 30–70% failure rates at a given checkpoint, those are the most diagnostic episodes for monitor evaluation

---

## Key Terms
`efficient benchmarking` · `rank-order stability` · `scaffold distribution shift` · `Item Response Theory` · `task selection` · `mid-range difficulty`

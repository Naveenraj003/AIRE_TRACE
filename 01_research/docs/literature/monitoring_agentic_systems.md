# Monitoring Agentic Systems Before They're Reliable (June 2026)

**Category:** Related Technical Approaches — Monitoring Methodology
**arXiv:** [2606.02494](https://arxiv.org/abs/2606.02494)
**Published:** June 2026 — Accepted to Workshop on Agentic Software Engineering (AgenticSE) at ACM CAIS 2026
**Authors:** Marisa Ferrara Boston, Glen Hanson, Effi Georgala, JD Hudgens, Heather Frase

---

## What the Paper Is

A **monitoring and triage methodology** for agentic systems in early production, where **structural defects** (not task-level errors) dominate the failure landscape. The core argument: standard task-level error detection is infeasible when the system itself isn't fully integrated.

### Methodology
- Decomposes evaluation across:
  - **3 dimensions**: Quality, Suitability, Efficiency
  - **3 scopes**: Within-run, Cross-run, Structural
- Uses **variance (CV = coefficient of variation)** as the primary characterization signal
- Severity classification adapted from **FMEA (Failure Mode and Effects Analysis)** and MIL-STD-882E
- Routes findings through severity classification → concentrates human attention on high-priority issues

### Key Results (220 runs, 120 document bundles, controlled error injection)
- Within-run monitors surface deterministic stage defects: **CV = 0.02**
- Cross-run monitors surface stochastic integration consequences: **CV = 1.25, 24% at L2 severity**
- Structural monitor identifies integration gap with perfect consistency: **CV = 0.00**
- Injected task-level errors **indistinguishable from clean baselines** → confirms structural defects mask task-level signal
- Automated triage routes **97%** of findings to automated tracking; only **2%** to human investigation

### Maturity-Staging Model
- Stage 1: Structural characterization
- Stage 2: Error detection
- Stage 3: Reliability tracking

## What It Solves

- Provides a practical monitoring methodology for systems that are not yet reliable enough for task-level monitoring
- Shows that structural defects mask task-level failures — monitors must be scoped appropriately
- FMEA-based triage reduces human review burden by 50×

## What It Lacks

- Evaluated on a **synthetic testbed** (not a standard agent benchmark)
- Calibrations are domain-specific; direct transfer requires re-calibration
- The structural monitoring approach requires knowing the system's intended architecture — not always available
- Does not address online/real-time monitoring; primarily cross-run and structural

## Relevance to AIRE-TRACE

- The **maturity-staging model** is directly relevant to AIRE-TRACE deployment: we should expect to operate in Stage 1 (structural characterization) before reliable episode-level detection
- The finding that structural defects mask task-level signal is consistent with our two-tier architecture (deterministic verification layer catches structural issues; statistical monitor catches subtle drift)
- CV-based scope characterization is a useful diagnostic tool for understanding our benchmark's variance structure
- FMEA-based severity routing is compatible with our alert threshold procedure — could be used to classify alerts by intervention priority
- **AGENTS.md Rule 2 alignment**: "Leakage guards run before every experiment" — structural integrity checks must precede task-level metrics, consistent with this paper's Stage 1 requirements

---

## Key Terms
`structural defects` · `FMEA` · `CV-based characterization` · `maturity-staging` · `triage` · `pre-reliable deployment`

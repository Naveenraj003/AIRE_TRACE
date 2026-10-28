# E-valuator: Reliable Agent Verifiers with Sequential Hypothesis Testing (Dec 2025)

**Category:** Threshold Calibration / False Alarm Control
**arXiv:** [2512.03109](https://arxiv.org/abs/2512.03109)
**Published:** December 2025

---

## What the Paper Is

E-valuator converts **any black-box verifier score** (LLM judge, process-reward model) into a **decision rule with provable false alarm rate control**, using sequential hypothesis testing.

### Core Technical Approach
- Frames success/failure prediction as **sequential hypothesis testing**
- Builds on **e-processes** (a generalization of likelihood ratios for sequential testing)
- The test remains **statistically valid at every step** of the trajectory — valid under optional stopping
- Enables **online monitoring** over arbitrarily long sequences

### Results
- Evaluated on **6 datasets and 3 agents**
- Provides greater **statistical power** and better **false alarm rate control** than alternative strategies
- Can be used to **quickly terminate problematic trajectories** and save tokens
- **Model-agnostic**: wraps any existing verifier heuristic

## What It Solves

- Converts heuristic verifier scores into decisions with **statistical guarantees on false alarm rate**
- Works online without knowing when the trajectory will end (optional stopping validity)
- Is model-agnostic — wraps any existing scorer

## What It Lacks

- The statistical guarantee depends on the **null hypothesis being correctly specified** (what counts as a "healthy run")
- E-processes are mathematically complex — implementation is non-trivial
- No specific evaluation on TerminalBench or τ²-Bench
- Requires a calibration set to estimate the null distribution
- The false alarm guarantee is marginal (over the distribution), not conditional

## Relevance to AIRE-TRACE

- **Extremely high relevance to our calibration/threshold procedure** (Section 8 of our protocol)
- E-valuator's statistical guarantees on false alarm rate are exactly what our threshold procedure aspires to — could be incorporated as a principled wrapper around our echo-state-network scores
- The **e-process framework** is a clean replacement for our CUSUM-based alarms with stronger theoretical guarantees
- Key protocol check: e-valuator requires a calibration set — our protocol already has a dedicated CALIBRATION split for exactly this purpose
- Combining e-valuator with our deterministic verification layer could yield a two-tier system: statistical alarm + deterministic confirm = very low false alarm
- **Critical reminder (Rule 5)**: Never select or adjust threshold using TEST data — e-valuator's sequential test must be calibrated on CALIBRATION only
- Should evaluate e-valuator as an alternative/complement to CUSUM in our ablation study

---

## Key Terms
`sequential hypothesis testing` · `e-processes` · `false alarm control` · `optional stopping` · `statistical guarantees` · `online monitoring`

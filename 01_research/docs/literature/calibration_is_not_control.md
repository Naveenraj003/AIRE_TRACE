# Calibration Is Not Control: Why LLM-Agent Oversight Needs Intervention (June 2026)

**Category:** Failure Warning / Monitoring Systems — Threshold Calibration / Theory
**arXiv:** [2606.21399](https://arxiv.org/abs/2606.21399)
**Published:** June 2026

---

## What the Paper Is

A **conceptual and empirical critique** of scalar risk prediction as the basis for agent oversight. The core argument: calibrating a scalar risk score does NOT fix the fundamental problem of intervention control.

### Key Concepts

- **Target Error**: The mismatch between predicting "how likely is the agent to fail?" vs. the correct decision object "would intervening improve the outcome?"
- **Intervention Advantage**: Expected utility gain from intervening rather than continuing — the true decision object for oversight
- **Prefix Branching**: A same-prefix counterfactual protocol that executes candidate actions from identical trajectory states to measure intervention advantage
- **Action-Conditioned Control**: Uses both the prefix AND the available action to predict outcome → significantly reduces control regret

### Results

| Method | Regret on ALFWorld |
|--------|-------------------|
| Scalar routing (baseline) | 0.506 |
| Recalibrated scalar | ~0.506 (unchanged!) |
| Simple action-conditioned controller | **0.110** |

- Recalibrating the same scalar score improves prediction metrics but **leaves control regret unchanged**
- Action-conditioned control reduces regret substantially in strong interactive regimes
- Gains shrink when interventions are weak or scalar routing already captures intervention-relevant information

## What It Solves

- Identifies a fundamental conceptual flaw in how agent oversight is framed in most existing work (including PrefixGuard, AgentForesight)
- Proposes intervention advantage as the correct optimization target
- Introduces prefix branching as a new evaluation protocol

## What It Lacks

- Very abstract/conceptual — limited evaluation settings (mainly ALFWorld)
- "Available interventions" must be pre-defined — unclear how to generalize to open-ended agentic tasks
- Prefix branching is expensive (requires re-running trajectories from same prefix with different actions)

## Relevance to AIRE-TRACE

- **Critically important conceptual challenge to our threshold calibration procedure**: Our Section 8 threshold procedure freezes a threshold chosen on CALIBRATION set — but this paper argues the threshold alone is insufficient if it's not action-conditioned
- However, our CUSUM alarms are inherently action-adjacent (they fire based on step-level observations, which are tied to actions taken) — partially addressing the target error
- The **intervention advantage** concept maps to our repair layer: when we flag and rollback-repair, the question is precisely whether repair improves outcome → our 45% recovery rate (from RT Detection paper) is empirical evidence of positive intervention advantage
- **Calibration decomposition finding** (recalibration doesn't fix control regret) is a significant result that our paper should acknowledge, especially in the calibration sections
- The prefix branching protocol could be used as an additional evaluation for our monitor-plus-repair pipeline

---

## Key Terms
`target error` · `intervention advantage` · `action-conditioned control` · `prefix branching` · `calibration` · `control regret`

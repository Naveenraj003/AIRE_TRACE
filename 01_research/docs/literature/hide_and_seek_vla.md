# Hide-and-Seek in Trajectories: Discovering Failure Signals for VLA Runtime Monitoring (May 2026)

**Category:** Failure Warning / Monitoring Systems
**arXiv:** [2605.30834](https://arxiv.org/abs/2605.30834)
**Published:** May 2026

---

## What the Paper Is

A framework for **Vision-Language-Action (VLA) model failure detection** using coarsely supervised learning. Targets embodied AI (robotics) rather than software/API agents.

### Method: Hide-and-Seek
- Combines **inter-trajectory** and **intra-trajectory contrastive objectives**
- Localizes **failure-indicative actions** from trajectory-level supervision only (no step-level annotation)
- Induces temporally structured failure signals
- Uses **conformal prediction** for practical accuracy-timeliness trade-off

### Evaluated On
- LIBERO, VLABench benchmarks
- Real-world robotic platform
- Three VLA policies: OpenVLA, π₀, π₀.₅

### Results
- State-of-the-art multi-task failure detection
- Good generalization to both **seen and unseen tasks**

## What It Solves

- Failure detection for embodied/robotic VLA models during execution
- Avoids costly action resampling or external models
- Uses conformal prediction for principled threshold control

## What It Lacks

- Focused entirely on **robotic/embodied AI** — not evaluated on LLM software agents
- VLA failure modes (physical action errors, robot collisions) are structurally different from LLM agent failures (tool misuse, hallucination)
- Limited transfer to non-embodied settings

## Relevance to AIRE-TRACE

- **Low direct relevance** for AIRE-TRACE's LLM agent focus, but methodologically interesting
- The **inter+intra contrastive objective** is related to Trajectory Guard's hybrid contrastive+reconstruction loss — both approaches to learning from trajectory-level labels
- **Conformal prediction** for threshold control is a principled alternative to our CUSUM/calibration approach — worth comparing in our threshold calibration section
- The "failure-indicative action localization" concept (identifying which specific steps are failure-critical from coarse supervision) parallels our checkpoint-level anomaly scoring
- Note: Our Rule 9 (features must be computable identically on both datasets) would exclude VLA-specific features from any shared model

---

## Key Terms
`VLA models` · `contrastive learning` · `conformal prediction` · `embodied AI` · `coarse supervision` · `runtime monitoring`

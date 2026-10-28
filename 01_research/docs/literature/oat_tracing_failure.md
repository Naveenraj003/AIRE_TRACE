# OAT: Tracing Agentic Failure from the Flow of Success (July 2026)

**Category:** Failure Warning / Monitoring Systems
**arXiv:** [2607.12747](https://arxiv.org/abs/2607.12747)
**Published:** July 2026

---

## What the Paper Is

OAT (One-class Anomaly Tracing) proposes **unsupervised failure attribution**: training **exclusively on successful trajectories** and identifying error steps at inference time given a failure trajectory.

### Core Technical Approach
- Casts failure attribution as **one-class learning** with **neural controlled differential equations (Neural CDEs)**
- Models the **dynamical pattern of successful trajectories** in latent space
- At inference time: each step in a failure trajectory gets an **anomaly score** based on deviation from success dynamics
- The set of high-anomaly steps forms the identified error set

### Results
- Trained on only **100 successful trajectories** (extremely data-efficient)
- **200–5000× faster** than prompting-based baselines
- **+20% F1** in-domain over baselines; **+7% F1** out-of-distribution
- Consistently outperforms LLM judge baselines on both in-domain and OOD datasets

## What It Solves

- Eliminates the need for **any failure annotations** — trains only on successes
- Dramatically reduces computational cost versus LLM judge approaches
- Shows that dynamical modeling (continuous-time differential equations) captures sequential trajectory structure better than discrete step scoring

## What It Lacks

- Only 100 training trajectories — performance on highly variable, longer episodes is unclear
- Neural CDEs have higher implementation complexity than standard RNNs or transformers
- No false-alarm rate calibration or threshold procedure described
- OOD gain (+7% F1) is modest — transfer is limited
- Does not distinguish between different failure categories — only anomaly scoring, not attribution

## Relevance to AIRE-TRACE

- **Direct methodological overlap**: OAT's one-class learning on successful trajectories aligns perfectly with our Rule 8 (never train on post-onset prefixes of failed episodes)
- Our echo-state-network approach is a lighter-weight alternative to Neural CDEs for the same one-class objective
- OAT's anomaly score per step → our checkpoint-level AUROC/AUPRC metrics
- The 100-trajectory training efficiency claim should be tested on our benchmark to understand sample complexity
- **Key difference**: OAT is post-hoc (analyzes complete failure trajectories); AIRE-TRACE is online (prefix-only, real-time detection) — this is an important positioning distinction
- OAT does not evaluate on TerminalBench or τ²-Bench, creating an opportunity for our paper

---

## Key Terms
`one-class learning` · `neural CDE` · `unsupervised failure attribution` · `successful trajectories` · `anomaly scoring` · `dynamical systems`

# AIRE-Trace Research Foundations

*(Evidence level: LEVEL 1 — DIRECTLY OBSERVED. Recovered exactly from the original `PROJECT_CONTROL.md` artifact).*

## 1. Research Gap
Attribution asks: "where or why did this already-failed run go wrong?" Warning asks: "what is the probability of eventual failure, given only the prefix, while the outcome remains unknown?" Existing prospective methods address the second but do not cross-compare each other under one standardized protocol.

## 2. Novelty Claim
A standardized, prospective, prefix-only evaluation protocol for online agent-failure warning—fixing information visibility, failure-target definition, alert semantics, calibration procedure, false-alarm constraints, lead-time measurement, and compute accounting. Instead of proposing another failure detector, our system standardizes how different methods are evaluated and compared.

## 3. Hypotheses
The project does not predetermine a directional hypothesis (e.g., "Method X will win"). The tested hypothesis is whether method rankings shift substantially across ranking/calibration/operational metrics or remain stable, and whether learned warning behavior transfers between datasets.

## 4. Experimental Philosophy
- Checkpoints are outcome-independent and episode-symmetric.
- Calibration isolation: Test set remains untouched until final evaluation.
- Statistical unit is the episode, not the prefix.
- Metric-sensitivity analysis emphasizes ranking stability (PDC) over absolute numbers.

## 5. Feature/Trace Definition
Prefix-only feature vectors. Features must be computable, with the same definition and information boundary, on both datasets for the primary transferable model.

## 6. Failure Taxonomy
Not explicitly a failure categorization taxonomy; focused on `eventual_failure` / `eventual_success` outcomes mapped canonically from each dataset's native success criteria.

## 7. Prediction Target
Probability of eventual failure given a prefix up to checkpoint *t*, while the actual outcome remains unknown.

## 8. Risks
- Insufficient TerminalBench episodes for a 3-way split.
- Lack of feature overlap between the two datasets.
- Checkpoint horizon creating a dataset-dependent observation bias.
- VRAM limitations (RTX 2050, 4GB) for Sequence and LLM models.

## 9. Evidence Required
- Gate 1 empirical dataset statistics (episode counts, class balance, trajectory lengths).
- Bootstrapped confidence intervals for all comparative claims.
- Explicit mapping definitions for outcome and failure onset.

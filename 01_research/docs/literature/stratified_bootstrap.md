# Stratified Bootstrap Test Package (Dec 2025)

**Category:** Threshold Calibration / Statistical Methods
**arXiv:** [2512.15057](https://arxiv.org/abs/2512.15057)
**Published:** December 2025
**Ref ID:** [T3]

---

## What the Paper Is

Introduces the **Stratified Bootstrap Test (SBT)** — a nonparametric, resampling-based framework for assessing the **stability of group-specific ranking patterns** in multivariate data.

### Two Components
1. **Non-containment index**: Quantifies ranking robustness — measures whether a group's top-ranked items remain highest-scoring across bootstrap samples
2. **Stratified bootstrap test**: Formal statistical inference by testing ordering hypotheses among population means; approximates null distribution without distributional assumptions

### Applications
- Survey analysis and item response assessment
- Fairness auditing in AI systems
- Ranking consistency and detection of adversarial response patterns

## What It Solves

- Nonparametric ranking stability assessment with no distributional assumptions
- Provides formal inference (p-values, confidence intervals) for ranking hypotheses
- Enables detection of aberrant or adversarial patterns in ranked data

## What It Lacks

- Primarily designed for survey/rating data, not sequential time-series
- May need adaptation for episode-level resampling (where within-episode data is correlated)
- No specific implementation for agent trajectory evaluation

## Relevance to AIRE-TRACE

- Directly supports our **episode-cluster bootstrap** for ranking-stability analysis
- The **non-containment index** is structurally similar to our PDC (Probability of Direction Consistency) metric — both measure whether relative rankings are stable across resampling
- The **stratified resampling** (by group/episode) is exactly our Rule: "never compute bootstrap CI by resampling prefixes directly — always resample at the episode level"
- Formal inference (null distribution approximation without assumptions) is what we need for our Holm-Bonferroni correction on multiple monitor comparisons
- The adversarial pattern detection application maps to MonitoringBench robustness evaluation

---

## Key Terms
`stratified bootstrap` · `non-containment index` · `ranking stability` · `nonparametric inference` · `fairness auditing` · `resampling`

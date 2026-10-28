# Rethinking Evaluation in the Era of Time Series Foundation Models: Information Leakage Challenges (Oct 2025)

**Category:** Data Leakage / Methodological Foundations
**arXiv:** [2510.13654](https://arxiv.org/abs/2510.13654)
**Published:** October 2025
**Ref ID:** [L2]

---

## What the Paper Is

Identifies and characterizes **two kinds of information leakage** in time-series foundation model evaluation that produce overly optimistic performance estimates:

### Two Types of Leakage
1. **Train-test sample overlaps**: Multi-purpose reuse of datasets causes direct test contamination
2. **Temporal overlap of correlated series**: Train and test series are temporally correlated even without direct overlap — the model has implicitly seen related patterns

### Key Argument
Standard evaluation methodologies for TSFMs (Time Series Foundation Models) risk producing optimistic estimates that fail to generalize to real-world settings. The authors call for principled evaluation methodologies analogous to those needed for LLMs.

## What It Solves

- Precisely characterizes the two leakage types that corrupt time-series evaluation
- Calls for community adoption of principled leakage-prevention methodologies
- Directly analogizes to LLM evaluation integrity problems

## What It Lacks

- Does not provide a concrete algorithm for leakage prevention (compare to DataSAIL)
- Focused on foundation models, not task-specific agent evaluation

## Relevance to AIRE-TRACE

- **Both leakage types map directly to our protocol**:
  - Type 1 (train-test sample overlaps) → our task-disjoint TRAIN/CALIBRATION/TEST split (no episode appears in two splits)
  - Type 2 (temporal overlap of correlated series) → our prohibition on splitting prefixes from one episode across splits (Rule 3: whole episode goes to exactly one split)
- This paper provides the **theoretical justification** for why our split rules exist — we can cite it to explain why simple random splitting of prefixes would be leaky
- The "optimistic estimates" finding validates our concern that papers without task-disjoint splitting report inflated numbers
- Our `assert_no_split_leakage` guard is exactly the runtime enforcement of the leakage prevention this paper calls for

---

## Key Terms
`information leakage` · `train-test overlap` · `temporal correlation` · `time-series evaluation` · `foundation models` · `evaluation integrity`

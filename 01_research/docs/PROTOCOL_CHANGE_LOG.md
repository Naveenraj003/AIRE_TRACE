# AIRE-Trace Protocol Change Log

**New Log Format Mandate:** All new entries in this log MUST use the following format:

```markdown
## YYYY-MM-DD HH:MM — EVENT-ID

Type: DECISION
Track: IEEE-RESEARCH | FUTURE-RESEARCH

### Event
What happened.

### Motivation
Why it was done or considered.

### Evidence
Exact file, command, artifact, test output, or user decision supporting the event.

### Decision
What was decided.

### Files Affected
Exact files changed, if any.

### Result
Observed result only. Do not convert assumptions into results.

### Scientific Impact
Whether the event affects: protocol, implementation, evaluation, statistics.

### Status
PROPOSED | IN PROGRESS | COMPLETED | FROZEN | REJECTED | BLOCKED

### Next Action
The next concrete action, if any.
```

---

## Frozen Scientific Protocol Principles
Unless a new contradiction is discovered or an explicit scientific decision is made, do not change:
- train/calibration/test semantics
- prospective prefix-only semantics
- frozen thresholds during test
- FAR definition
- Recall definition
- episode-level statistics
- episode-cluster bootstrap
- leakage guards
- exclusion accounting
- dataset split definitions
- existing validated results
- manuscript scientific claims

Any future change that could affect scientific validity must be recorded as a decision gate before implementation and logged here.

---

## 2026-09-06 17:30 — AMD-001: Canonical Paired Recall@FAR Testing in statistical_testing.py

Type: DECISION (PROTOCOL AMENDMENT)  
Track: IEEE-RESEARCH  

### Event
Extended canonical evaluation tool `src/evaluation/statistical_testing.py::compute_paired_bootstrap_test` to natively support threshold-based `Recall_at_FAR` testing using true joint episode-cluster resampling.

### Motivation
Initial significance tests used ad-hoc split-sampling scripts (`run_m2_bootstrap.py`, `run_m3_bootstrap.py`) that resampled success and failure episodes independently and froze the failure denominator, artificially understating variance. A canonical, unified tool was required.

### Evidence
- File: `src/evaluation/statistical_testing.py`
- Test: `tests/evaluation/test_statistical_testing.py::test_compute_paired_bootstrap_test_recall_at_far` (Pytest 3/3 passing)
- Regression Verification: Gate X AUROC/AUPRC test (`scratch/run_stats.py`) confirmed numerically identical before and after (Diff: 0.0312, Bootstrap Mean: 0.0320, p_adj: 0.0999).

### Decision
Approve additive extension of `compute_paired_bootstrap_test`. Mark legacy ad-hoc bootstrap outputs as SUPERSEDED. Establish v2 outputs (`dyn_comp_vs_m1_bootstrap_k30_v2*.json`) as canonical Level-1 artifacts.

### Files Affected
- `src/evaluation/statistical_testing.py`
- `tests/evaluation/test_statistical_testing.py`
- `RESEARCH_LOG.md`

### Result
- Preserves identical null-centering two-sided p-value formula: $\Delta^{(b)}_0 = \Delta^{(b)}_* - \Delta_{\text{obs}}$; $p = (1 + \sum [|\Delta^{(b)}_0| \ge |\Delta_{\text{obs}}|]) / (B + 1)$.
- Emits comprehensive diagnostic telemetry: observed FAR, bootstrap mean FAR, 95% CI on FAR.
- Validated on 416 full TEST ($p = 0.000999$ at $B=1,000$; $p = 9.999 \times 10^{-5}$ at $B=10,000$).

### Scientific Impact
Strengthens statistical rigour of prospective warning evaluation without altering frozen evaluation semantics.

### Status
COMPLETED / FROZEN


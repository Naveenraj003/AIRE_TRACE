# Gate 3.4 Final Verdict

**Date:** 2026-08-04  
**Auditor Role:** Independent Final Reviewer  

---

## 1. Evaluation of Criteria

1. **Artifact integrity**: **PASS**. Executed JSON and CSV outputs are 100% internally consistent. 36/36 metrics, all thresholds, and PDC values (0.7667) match perfectly. Independent reconstruction verified the math.
2. **Scientific reproducibility**: **PASS**. The pipeline runs deterministically with seed=42. While there are deviations from the original written protocol (e.g., S1 being an RF, uniform training weights), the code and executed JSON artifacts are fully reproducible as-is.
3. **Protocol compliance**: **DEVIATIONS DETECTED**. Several high-severity deviations exist, most notably S1 acting as a Random Forest (Classical ML) rather than a Sequence model, and the omission of episode-balanced sample weights during training. However, per the authoritative rule, executed artifacts and code outrank the narrative protocol.
4. **Documentation consistency**: **FAILING**. `RESEARCH_LOG.md`, `DECISION_LOG.md`, and report narratives contain stale pre-reconciliation metrics (e.g., claiming S1 AUROC is 0.7635 instead of 0.6016) and broken evidence links due to report consolidation.
5. **Repository cleanliness**: **PASS**. The repository is logically structured, though minor cleanup of bytecode caches and temporary scripts is advised. No destructive actions are required to advance.
6. **Traceability**: **PARTIAL**. While canonical artifacts have a clear lineage, the decision log suffers from broken links to consolidated reports, and Gate 0 lacks formal log entries.
7. **Remaining blocking issues**: **NONE**. No finding invalidates the math or prevents progression, provided the protocol is formally amended to reflect the executed reality.

---

## 2. Classification of Findings

*Note: A finding is BLOCKING only if it invalidates scientific results or prevents Gate 4 from beginning. Documentation defects alone are NOT BLOCKING.*

### BLOCKING
- *None.*

### HIGH
- **F-2 / D-10**: Incompatible failure/success breakdowns for TEST episodes (4,270/2,803 vs 3,936/3,137). Needs documentation correction.
- **F-3 / A-2 / D-6**: Stale pre-reconciliation metrics in `RESEARCH_LOG.md` (e.g., S1 AUROC=0.7635).
- **F-4 / A-4 / D-7**: Stale pre-reconciliation metrics in `DECISION_LOG.md` marked as [FROZEN].
- **F-6 / D-2 / A-12**: Protocol drift. S1 is a Random Forest (M-family), not a Sequence model (S-family).
- **F-7 / D-4 / A-13**: Protocol violation. Training does not use episode-balanced sample weights (Rule 11).
- **F-1 / D-9 / A-3**: Split count inconsistencies (Gate 1 vs manifest: 31,035 vs 31,016 TRAIN).
- **A-5**: Broken evidence links in `DECISION_LOG.md` referencing deleted sub-reports.

### MEDIUM
- **F-5 / D-11**: Report generation claims $B=500$ bootstrap, but actual execution used $B=100$.
- **D-3**: Holm multiple-comparison correction is not implemented (Rule 7).
- **A-1**: Missing decision/evidence fields in `RESEARCH_LOG.md` for earlier gates.
- **A-6**: Stale statuses in `PROJECT_CONTROL.md` ("BLOCKED", "Not started").
- **A-10**: Undocumented file locations (e.g., `docs/` folder) in `AGENTS.md` section 5.

### LOW
- **F-8**: Minor status staleness in documents.
- **D-1**: Empty episode filtering (17,642 episodes) was not documented as a formal protocol decision.
- **A-7, A-8, A-9**: Missing ROADMAP dates, missing sub-gate roadmap entries, and undocumented Gate 0.
- **Cleanliness Findings**: Residual `__pycache__` folders and `scratch/` temporary scripts.

### INFORMATIONAL
- **D-5**: Post-onset training exclusion is not enforced in code, but is moot because TerminalBench currently lacks onset annotations.
- **Cleanliness Findings**: Derived JSON subsets (`pdc_summary.json` and `calibrated_thresholds.json`) are valid convenience artifacts.

---

## 3. Specific Questions

**1. Are the executed baseline results scientifically valid?**  
**TRUE.** The baseline results are mathematically correct and internally consistent representations of the models and weights that were actually executed.

**2. Are the JSON/CSV artifacts internally consistent?**  
**TRUE.** Artifact reconstruction confirmed a 100% match across all metrics, thresholds, and independent PDC calculations.

**3. Does any discrepancy require rerunning experiments?**  
**FALSE.** Under the authoritative rule, executed artifacts are Rank 1 and source code is Rank 2. Discrepancies between the executed reality and the narrative protocol mean the protocol must be amended to match reality, not the other way around.

**4. Does the Random Forest S1 implementation block Gate 4?**  
**FALSE.** It is the canonical reality. It only requires a protocol amendment to formally acknowledge that S1 is a tabular ensemble baseline (M-family variant), altering the experiment from H/M/S to H/M/M'.

**5. Does the missing Rule 11 sample-weighted training invalidate existing baseline results or simply require protocol reconciliation?**  
**Simply requires protocol reconciliation.** The executed code defines the canonical reality. The protocol must be amended to state that uniform prefix weighting was used for training.

**6. Does the bootstrap B=100 versus B=500 discrepancy invalidate point estimates?**  
**FALSE.** Bootstrap iterations only affect the width of confidence intervals, not the point estimates. The point estimates are valid, and B=100 is the canonical executed reality.

**7. Are stale documentation metrics sufficient reason to fail Gate 3.4?**  
**FALSE.** Documentation defects do not invalidate the reproducibility of the canonical JSON/CSV artifacts. They must be fixed, but they do not fail the gate outright.

**8. Can Gate 4 begin after documenting remaining deviations?**  
**TRUE.** Once the protocol and logs are amended to reflect the executed reality, all conflicts are resolved and the project can safely proceed.

---

## 4. Final Verdict

**PASS WITH REQUIRED AMENDMENTS**

The following amendments must be implemented before the repository is considered fully canonical and ready for Gate 4:

1. **Amend Protocol Section 6**: Formally update the protocol to document that S1 is implemented as a Random Forest classifier (Classical ML), evaluating H vs M vs M'.
2. **Amend Protocol Rule 11**: Update the protocol to formally state that baseline training utilized uniform prefix weighting, matching the executed `model.fit()` implementation.
3. **Correct Stale Metrics**: Update `RESEARCH_LOG.md` (lines 75–87) and `DECISION_LOG.md` (line 70) to reflect the canonical executed metric values (e.g., S1 AUROC = 0.6016, PDC = 0.7667).
4. **Reconcile Split Counts**: Update `RESEARCH_LOG.md` to reflect the canonical `dataset_manifest.json` split counts (e.g., TRAIN=31,016) and resolve the TEST failure/success breakdown discrepancy (4,270/2,803 vs 3,936/3,137).
5. **Acknowledge $B=100$**: Update the protocol or reports to formally state that $B=100$ bootstrap iterations were used.
6. **Fix Evidence Links**: Update `DECISION_LOG.md` to point broken sub-report evidence links to their surviving, consolidated gate report equivalents.
7. **Document Episode Filtering**: Add a formal protocol or decision log note regarding the filtration of the 17,642 empty episodes.

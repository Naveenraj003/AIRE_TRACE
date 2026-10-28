# AGENTS.md — AIRE-Trace Project Rules

This file governs anyone or anything (human or AI coding assistant) implementing this
project. It is deliberately short. **Full rule text and rationale live in
`AIRE-Trace_Frozen_Protocol_and_Plan.md` — this file is a condensed enforcement
checklist, not a replacement for it.** When in doubt, read the referenced rule in full
before writing code that touches it.

---

## 0. Before touching any code

1. Read `AIRE-Trace_Frozen_Protocol_and_Plan.md` in full. Do not skim it.
2. Confirm Gate 1 (real dataset inspection) is complete. If any Gate 1 item in that
   document's Section 7 is still unchecked, **stop and complete it before writing
   ingestion, prefix-generation, or modeling code.** Coding ahead of Gate 1 is the
   single most likely way this project silently reintroduces a leakage bug that was
   already found and fixed once during protocol design.
3. If a decision required by the protocol isn't in the document, do not invent one and
   proceed silently. Add it to `RESEARCH_LOG.md` as an open question and flag it to the
   author before proceeding.

## 1. Absolute prohibitions (never do these, no exceptions)

- **Never** let a feature at checkpoint `t` depend on any event with `step_index > t`.
  (Protocol Rule 2.)
- **Never** split prefixes from one episode across TRAIN/CALIBRATION/TEST — the whole
  episode goes to exactly one split. (Rule 3.)
- **Never** let a terminal event's content or field names disclose the episode outcome
  to a monitor, including at the final checkpoint. (Rules 2, 6.)
- **Never** train or calibrate H/M/S/L on post-onset prefixes of a failed episode.
  Post-onset prefixes are evaluation-only. (Rule 8.)
- **Never** select or adjust an alert threshold using TEST data, under any
  circumstance. (Section 8, threshold procedure step 5.)
- **Never** use onset-anchored or outcome-dependent checkpoints in the primary
  evaluation. Checkpoint selection must be outcome-independent and episode-symmetric.
  (Rule 1.)
- **Never** present a τ²-Bench (Mode B) AUROC/AUPRC/calibration number next to a
  TerminalBench (Mode A) one as though they measure the same thing. Label every metric
  with its mode. (Section 4's evaluation-mode table.)
- **Never** let a feature enter the shared M/S/L model unless it's computable
  identically on both datasets. TerminalBench-only features go in a
  TerminalBench-only diagnostic model, never the primary transferable one. (Rule 9.)
- **Never** consume a dataset's native success/failure field directly — always route
  through the canonical `eventual_success`/`eventual_failure` mapping first. (Rule 10.)
- **Never** pool literature-reported numbers (PrefixGuard, AgentForesight, Trajectory
  Guard) with locally measured numbers as if directly comparable. Keep them visibly
  separate in every table. (Rule 7.)
- **Never** compute a bootstrap CI by resampling prefixes directly — always resample
  at the episode level. (Rule 7.)
- **Never** report PDC without its coverage figure, and never average an all-tied pair
  into the overall PDC mean. (Section 8, ranking-stability rules.)
- **Never** change a frozen protocol decision inside implementation code without
  updating the protocol document first and logging the amendment in
  `RESEARCH_LOG.md`. Frozen decisions change by deliberate amendment, not by whatever
  turned out to be convenient while coding.

## 2. Workflow rules

- **Frozen protocol beats implementation convenience.** If a rule makes the code
  harder to write, that is not grounds to quietly relax it.
- **Every data-derived decision is logged, not just implemented.** When Gate 1 or
  later inspection resolves an open item (onset semantics, feature overlap, checkpoint
  horizon K, etc.), write the finding and the reasoning to `RESEARCH_LOG.md` before
  moving on — the eventual paper's Methodology section should be reconstructed from
  this log, not from reading the code after the fact.
- **No scope creep without an explicit, written amendment.** The out-of-scope list in
  `PRD.md` Section 6 is binding. If something on it starts looking necessary, that's a
  signal to stop and raise it explicitly, not to add it quietly.
- **Reproducibility is mandatory, not aspirational.** Every experiment run must record
  its seed, its exact code version/commit, and its exact config (checkpoint horizon,
  thresholds, feature set) alongside its results.
- **Leakage guards run before every experiment, not just once during development.**
  Two guards already exist as a starting point (`assert_no_feature_leakage`,
  `assert_no_split_leakage`), but "documented rule" and "runtime-enforced invariant"
  are not the same thing — the full set of protocol rules should eventually have a
  corresponding runtime check, not just the two already drafted. At minimum, add
  equivalent enforced checks for: the sanitization invariant (Rule 6 — no
  outcome-bearing content in any event a monitor can see, checked programmatically, not
  just assumed from the sanitize function having been called), the canonical-outcome
  mapping (Rule 10 — no code path consumes a native outcome field directly), Mode A/B
  applicability (Section 4 — no metric value leaves the evaluator unlabeled with its
  mode), test-threshold immutability (Section 8 — threshold value is frozen and
  provably untouched by any TEST-set computation), post-onset training exclusion
  (Rule 8 — no post-onset prefix reaches a training or calibration call), common-
  feature compatibility (Rule 9 — the primary transferable model's feature set is
  provably a subset of both datasets' available fields), and PDC coverage reporting
  (Section 8 — PDC is never emitted without its paired coverage value). A rule that
  only lives in documentation provides no protection against a later refactor that
  silently breaks it.
- **`dataset_prep.py` is preliminary/untrusted, not evidence that ingestion is already
  correct.** It was drafted against assumed schemas before Gate 1 and is referenced
  throughout `TECHNICAL_DESIGN.md` as a starting sketch. Do not treat its existence as
  proof that canonical-schema, sanitization, split, or prefix logic is already
  protocol-compliant — it must be re-validated against real data during Gate 1 and
  patched to match actual schemas before being trusted for any real run.
- **If a real dataset contradicts an assumption in the protocol document** (e.g. a
  field doesn't mean what was assumed), stop, do not route around it silently, and
  update the protocol document's relevant rule with the corrected finding before
  proceeding.

## 3. Ambiguity handling

If an implementation question isn't resolved by the protocol document, the PRD, or the
technical design:
1. Check `RESEARCH_LOG.md` — it may already be answered there from a prior Gate 1
   finding.
2. If genuinely unresolved, do not silently pick the most convenient option. State the
   ambiguity, propose the most defensible default consistent with the protocol's
   existing principles (e.g. "outcome-independent," "episode-level," "TEST never
   touched before freeze"), and flag it for explicit confirmation before it becomes
   load-bearing for results.

## 4. Document precedence and the old Research Bible

If any two documents in this project conflict, resolve in this order:

```
AIRE-Trace_Frozen_Protocol_and_Plan.md   (scientific source of truth)
              ↓
           PRD.md                        (what the software must deliver)
              ↓
          AGENTS.md                      (this file — what must never be violated)
              ↓
     TECHNICAL_DESIGN.md                 (how the system is organized)
              ↓
      RESEARCH_LOG.md                    (what real data forced us to decide)
              ↓
             Code
```

**The original `AI_Agent_Reliability_Final_Project_Research_Bible.md` is quarantined,
not deleted.** It predates the frozen protocol and still contains an incompatible
research direction — language describing a novel reliability-assessment *methodology/
algorithm* as the contribution, and an older experiment plan (synthetic traces,
recovery experiments, cross-agent generalization, baseline-beating detector) that the
project deliberately moved away from. **Do not use the Bible's research-direction,
contribution-statement, or experiment-plan sections to make any implementation
decision** — they are superseded. Its schema/database/risk-catalog sections that the
frozen protocol document did not explicitly supersede may still be useful as reference
material, but even those should be cross-checked against the frozen protocol before
use, never trusted standalone.

## 5. File map (for anything navigating this project)

- `AIRE-Trace_Frozen_Protocol_and_Plan.md` — scientific source of truth. Read first.
- `PRD.md` — what the system must do.
- `TECHNICAL_DESIGN.md` — how it's structured; explicit Gate-1-pending markers.
- `RESEARCH_LOG.md` — running record of every data-derived decision (start this before
  writing ingestion code).
- `dataset_prep.py` — ingestion/normalization/leakage-guard code, currently with
  placeholder field mappings pending Gate 1 schema inspection.
- `AI_Agent_Reliability_Final_Project_Research_Bible.md` — **quarantined**, see
  Section 5. Reference only, never authoritative for implementation decisions.

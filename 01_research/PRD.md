# AIRE-Trace — Product Requirements Document

**Source of truth for all scientific rules, definitions, and gates:**
`AIRE-Trace_Frozen_Protocol_and_Plan.md`. This PRD defines *what the system must do*;
it does not restate protocol rules — it references them by number. If anything here
appears to conflict with the protocol document, the protocol document wins.

---

## 1. Purpose

AIRE-Trace is a research evaluation system that answers one question: **do comparative
performance claims for online agent-failure warning methods remain consistent when
those methods are evaluated under a common, standardized protocol?** It is not a new
failure detector — it is the harness that lets several detector types be compared
fairly, plus the empirical result of running that comparison.

## 2. Problem

Recent work on predicting AI-agent failures from partial execution traces (PrefixGuard,
AgentForesight, Trajectory Guard, and others) each uses its own dataset, prefix
definition, calibration procedure, and metrics. Reported comparative claims between
method types (heuristic vs. classical ML vs. learned sequence models vs. LLM judges)
are not directly comparable across these papers. No existing work cross-evaluates these
method families under one fixed protocol. See the protocol document's Section 2
(Novelty audit trail) for the full citation-level gap analysis.

## 3. Target users

- **Primary:** the student author, for final-year submission and IEEE-track paper.
- **Secondary:** an evaluator/examiner assessing both the software artifact and the
  paper.
- **Tertiary (design-for, not build-for):** a researcher who wants to plug in a new
  warning method and get directly comparable metrics against H/M/S — this shapes the
  software's modularity even though building a public-facing tool for this audience is
  out of scope.

## 4. Core value proposition

Instead of one more failure-warning model, AIRE-Trace delivers a **reusable evaluation
harness plus a controlled empirical answer**: every method receives identical
information, is scored against identical failure-target and alert definitions, and the
resulting comparison is either stable across metrics or it isn't — and the system shows
which.

## 5. Primary workflow

1. Load a raw trajectory dataset (τ²-Bench or TerminalBench).
2. Normalize into the canonical trace schema, apply outcome mapping and terminal-event
   sanitization (protocol Rules 6, 10).
3. Generate leakage-safe prefixes per the frozen checkpoint policy (Rules 1, 8).
4. Split episodes into TRAIN/CALIBRATION/TEST (TerminalBench only, per Section 4's
   resolved dataset roles).
5. Fit trainable methods M/S (and L, if implemented) on TRAIN; H is training-free and
   is used as-is. Calibrate alert thresholds for all applicable methods, including H,
   on CALIBRATION per the
   frozen threshold procedure (Section 8).
6. Evaluate on TerminalBench TEST (Mode A, full prospective metrics) and on τ²-Bench
   (Mode B, eventual-outcome diagnostic) — see Section 4's evaluation-mode table.
7. Run the metric-sensitivity / ranking-stability analysis (PDC, coverage, raw
   pairwise-direction table).
8. Produce result tables/figures for the paper, and display them in a lightweight
   results app.

## 6. Functional scope

**In scope (build these):**
- Dataset ingestion + normalization for τ²-Bench and TerminalBench.
- Leakage-safe prefix generation with all guards from protocol Rules 1–11 enforced in
  code, not just documentation (see the leakage-guard functions already drafted in
  `dataset_prep.py`).
- H (heuristic), M (classical ML), S (sequence model) monitors — mandatory.
- L (local open-weight semantic monitor) — optional, contingent on hardware; the
  system must run and produce valid results with L entirely absent.
- Common evaluator computing: AUROC, AUPRC, Brier/ECE, FAR, prospective Recall@FAR, raw
  Recall, lead time, alert burden, compute cost — each tagged with its correct
  Mode A/Mode B applicability (Section 4's table).
- Ranking-stability analysis: raw pairwise-direction table, PDC + coverage per pair,
  overall PDC over informative pairs (Section 8).
- Episode-cluster bootstrap for all confidence intervals (Rule 7).
- Results storage (local files/lightweight DB — not a hosted service) and a results
  app: tables, comparison charts, ranking-stability visualization. This is a thin
  front end over the pipeline, not the product itself.
- Research log capturing every data-derived decision made during Gate 1 (onset
  semantics, feature mapping, checkpoint horizon, etc.) as it's made.

**Explicitly out of scope (do not build, do not let scope creep back in):**
- A new detector architecture as the headline contribution.
- Foundation-model training.
- Reproducing PrefixGuard, AgentForesight, or Trajectory Guard's actual
  implementations — their published numbers are cited as reference points only.
- More than 2 datasets, more than 3 mandatory method families.
- Any paid API calls or paid agent-run generation (zero-cost constraint).
- A public-facing hosted product, user accounts, or multi-user features.
- Any claim of being "first" at agent reliability evaluation, or that existing methods
  are "wrong."

## 7. Hardware / cost constraints

- Development machine: RTX 2050, 4GB VRAM. M and S must run within this budget.
- Zero paid API usage for the core H/M/S study. L, if attempted, uses a local
  open-weight model only (see protocol document, method-families table).
- All datasets are static, pre-recorded trajectories — no paid agent execution
  required (protocol Section 4).

## 8. Success criteria

- **Software:** a working pipeline that, given the two raw datasets, reproducibly
  produces every metric applicable to that dataset's evaluation mode (Section 4's Mode
  A/B table — τ²-Bench cannot produce prospective Recall@FAR or lead time, and its
  AUROC/AUPRC/Brier/ECE are Mode B diagnostics, not the Mode A prospective versions;
  acceptance tests must not expect a metric a dataset's mode cannot support) with every
  protocol rule enforced as
  a runtime check, not just a design intention.
- **Research:** a defensible answer to the core research question (protocol Section 1)
  — either "the ranking is stable" or "the ranking is metric-sensitive," both are valid
  outcomes — supported by the raw pairwise table, PDC, and calibration/lead-time
  results.
- **Paper:** a submission-ready IEEE-formatted paper within the 8-week window (protocol
  Section 11), grounded in the frozen protocol, with <13% similarity and no fabricated
  citations.
- **Demonstration:** a working results app usable in a live final-year defense within
  the 5-month window.

## 9. Acceptance criteria (per component)

- Leakage guards (`assert_no_feature_leakage`, `assert_no_split_leakage`) pass on every
  run before any model is fit or scored — a failing guard blocks the pipeline, it does
  not warn and continue.
- Every reported CI is episode-cluster bootstrapped (Rule 7) — no prefix-level
  pseudo-replication anywhere in the codebase.
- Every AUROC/AUPRC/calibration number is labeled with its Mode (A or B) in all output
  — no unlabeled metric ever reaches a table or figure.
- The threshold-selection procedure (Section 8) runs exactly once per method on
  CALIBRATION, is frozen, and TEST is never touched before that freeze.
- PDC, coverage, and the raw pairwise-direction table are all present in the output —
  PDC is never reported without its coverage figure.

## 10. Dependencies / research constraints

This PRD assumes the frozen protocol document's Gate 1 (real dataset inspection) has
been completed and its outputs (onset semantics, feature mapping, checkpoint horizon,
canonical outcome fields) are available before implementation of ingestion/prefix
generation begins. Building ahead of Gate 1 risks exactly the kind of
assumption-baked-into-code problem the protocol was designed to prevent.

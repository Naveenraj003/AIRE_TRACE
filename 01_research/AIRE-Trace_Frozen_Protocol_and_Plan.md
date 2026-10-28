# AIRE-Trace — Frozen Protocol & Action Plan
**Status: research question, scope, datasets, and evaluation protocol are FROZEN.**
Nothing below changes without a deliberate, documented amendment — not a quiet edit.

This document supersedes Sections 1, 8, 15–25 of the original Research Bible. Keep the
Bible's schema/database/risk sections; they still apply. This file is the single source
of truth for *what the contribution is* and *what the rules are*.

---

## 1. Frozen research position

**Contribution (paste as-is into the paper draft later):**

> A standardized, prospective, prefix-only evaluation protocol for online agent-failure
> warning — fixing information visibility, failure-target definition, alert semantics,
> calibration procedure, false-alarm constraints, lead-time measurement, and compute
> accounting — applied to representative heuristic, classical-ML, and sequence-based
> methods (with an optional semantic/LLM-monitor extension, hardware permitting).
> Full prospective evaluation (AUROC, AUPRC, calibration, prospective Recall@FAR, lead
> time) is performed on TerminalBench, where failure-onset annotations exist; a
> secondary eventual-outcome diagnostic evaluation is performed on τ²-Bench as an
> independently sourced generalization check, using metrics that do not require an
> onset boundary. We determine whether comparative warning performance remains
> consistent under the common protocol on TerminalBench, and whether learned warning
> behavior transfers to τ²-Bench, including a metric-sensitivity analysis.
>
> **Protocol validity note:** the protocol and its core claim are valid on H/M/S alone.
> L is a reference extension, not a load-bearing component of the contribution — the
> paper must not describe the optional extension as a settled fourth mandatory family until L is confirmed running.
> **Dataset-mode note:** TerminalBench is the primary benchmark (core prospective
> claim); τ²-Bench is secondary (external-transfer diagnostic, evaluation-only) — see
> Section 4's evaluation-mode table. Never present a τ²-Bench AUROC/AUPRC number next
> to a TerminalBench one as though they answer the same question, and never assume the
> two datasets' native "failure" fields mean the same thing without the canonical
> outcome mapping in Rule 10.

**Core research question:**

> Do comparative performance claims for online agent-failure warning methods remain
> consistent when different methods are evaluated under identical information, target,
> alert, calibration, lead-time, and compute constraints?

**Primary comparison unit (clarifies what "comparative performance claims" means):**
the metric-sensitivity experiment is fundamentally about *ranking stability* — does the
ordering of H/M/S (e.g. H < M < S) stay the same across AUROC, AUPRC, calibration, and
Recall@FAR, on TerminalBench (Mode A)? That ordering is the primary comparative object.
Absolute per-method scores are reported separately and support the ranking claim but
are not themselves the central question. This sharpens the paper's actual thesis to:
*are published-style comparative conclusions about warning methods robust to a common
evaluation protocol and metric definition?*

**The one sentence for your guide/examiner when asked "what is your innovation":**

> "Instead of proposing another failure detector, our system standardizes how different
> online agent-failure warning methods are evaluated. Under the common prospective
> protocol, every method receives exactly the same partial information, the same
> failure definition and alert constraints, and is scored on common accuracy,
> calibration, false-alarm, lead-time, and cost metrics."
>
> **Scope of this sentence:** "same partial information" describes the common
> prospective protocol (Mode A, TerminalBench) — it is not a claim that τ²-Bench (Mode
> B) is evaluated under an equivalent information condition, since onset isn't
> observable there. Don't let this sentence get quoted out of the Mode A/B context.
>
> **Also do not say "all methods are trained under the same conditions"** — H is
> training-free; M/S(/L) optimize a weighted training objective. The accurate claim is
> narrower and still correct: *all methods are evaluated under the same information,
> target, alert, threshold-selection, and scoring protocol* — sameness is a property of
> the evaluation, not of each method's internal optimization procedure.

**The conceptual boundary that protects this from every adjacent paper — must appear
near-verbatim in the paper's Related Work:**

> Attribution asks: "where or why did this already-failed run go wrong?" Warning asks:
> "what is the probability of eventual failure, given only the prefix, while the outcome
> remains unknown?" Existing standardized-evaluation work (AgentProcessBench, ProcBench/
> ProcCtrlBench, Who&When Pro) addresses the first question. Prospective methods
> (PrefixGuard, AgentForesight, Trajectory Guard) address the second, but do not
> cross-compare each other under one protocol. This work does.

---

## 2. Novelty audit trail (what was checked, and why the gap survives)

| Work | What it does | Why it doesn't close this gap |
|---|---|---|
| AgentRx (2602.02475) | Post-hoc critical-failure-step localization | Retrospective, full-trajectory only |
| AgentBoard, AgentBench, GAIA, HAL | Outcome / process benchmarking | No prospective warning, no protocol standardization |
| TRAIL | Annotated trace error taxonomy | Descriptive dataset, not a warning method |
| AgentForesight (2605.08715) | RL-trained 7B online auditor | A warning *method*, not a cross-method protocol |
| PrefixGuard (2605.06455) | Prefix-based warning monitors, 4 benchmarks | A warning *method family*, doesn't cross-compare against AgentForesight/Trajectory Guard |
| Trajectory Guard (2601.00516) | Lightweight real-time sequence anomaly detector | Same — single method, own benchmark, own metrics |
| "Why Heuristics Beat LLMs" (TRAIL) | Heuristic vs LLM judge, single study | Single comparison, not a standardized reusable protocol |
| False-success study (2606.09863) | Lightweight vs LLM judge on τ²-Bench/AppWorld | Targets false-success detection at task end, not mid-trajectory prospective risk |
| AgentProcessBench, ProcBench/ProcCtrlBench | Standardize step-quality / process-defect labeling | Step-quality labeling ≠ prospective failure-risk warning |
| Who&When Pro (2607.09996) | 12,326 trajectories, controlled failure injection, attribution protocols | Explicitly retrospective — trajectories are failures *by construction* |

**Conclusion:** no existing work cross-compares heuristic / classical-ML / sequence / LLM-judge
warning methods under one fixed protocol for prospective, prefix-only failure risk. This
gap has been checked against the closest four neighbors twice over three rounds. Stop
searching unless a new paper explicitly claims this exact framing.

---

## 3. Frozen scope

**In scope:**
- Trace ingestion + normalization (τ²-Bench, TerminalBench)
- Leakage-safe prefix generation
- Three mandatory method families + one optional extension: Heuristic (H), Classical ML (M), Sequence model (S) — mandatory; Semantic/LLM monitor (L) — optional, not a fourth mandatory family
- Common evaluator: AUROC, AUPRC, calibration (Brier/ECE), Recall@fixed-FAR, lead time, compute cost
- Metric-sensitivity experiment (do rankings change across metrics?)
- A lightweight results app (not the original 7-page dashboard)

**Explicitly out of scope (do not let this creep back in):**
- New detector architecture as the headline contribution
- Foundation-model training
- Reproducing AgentForesight-7B or PrefixGuard exactly
- More than 2 primary datasets
- More than 3 mandatory method families (L is the one permitted optional extension)
- The original 7-page React dashboard before the paper is submitted
- Any claim of being "first" at agent reliability, or that existing methods are "wrong"

---

## 4. Frozen datasets

| Role | Dataset | Access | Prospective onset-relative lead time available? |
|---|---|---|---|
| **Secondary — external-transfer diagnostic (Mode B)**, evaluation-only | τ²-Bench | `github.com/sierra-research/tau-bench` → `historical_trajectories/` (static, no paid agent runs) | No — outcome-only, no step-level onset label. |
| **Primary — training + calibration source, and the core prospective (Mode A) evaluation benchmark** | TerminalBench | `Contextbench/Tracebench` on HuggingFace (has `incorrect_stages` annotations) | Yes — contributes full lead-time analysis. |

**Unambiguous role statement (fixes a prior wording conflict):** TerminalBench is the
primary benchmark for the core paper claim — it alone supports full prospective
evaluation. τ²-Bench is secondary: an independently sourced external-transfer
diagnostic, evaluation-only, with zero influence on training or thresholds. If asked
"which dataset is primary," the answer is unambiguously TerminalBench.

**Role clarification (resolves former Gate 3):** τ²-Bench has no onset label, so it
cannot supply the onset-bounded prefixes Rule 8 requires for training/calibration
without inventing a proxy boundary. Resolved policy: **all model fitting and threshold
calibration for H/M/S(/L) happens on TerminalBench only** (its own held-out TEST split
provides secondary in-benchmark evaluation); τ²-Bench is **evaluation-only**, receiving
the frozen models and frozen thresholds with zero influence on either.

**Evaluation-mode separation (NEW — closes a real conflation risk, not a wording
nicety).** Without an onset label, τ²-Bench cannot distinguish pre-onset from
post-onset prefixes. A late prefix in a failed τ²-Bench trajectory may already contain
obvious post-failure evidence, so scoring AUROC/AUPRC/calibration across *all* its
prefixes measures something different from TerminalBench's genuinely pre-onset-only
numbers — even though both would be labeled "AUROC." These must never be placed in the
same table row as equivalent quantities. Two explicitly named evaluation modes:

- **Mode A — Prospective-warning evaluation (TerminalBench only).** Only pre-onset and
  onset prefixes are eligible (post-onset excluded, per Rule 8). Supports: AUROC,
  AUPRC, Brier, ECE, FAR, prospective Recall@FAR, lead time. This is the evaluation the
  contribution statement's "prospective, prefix-only" language actually describes.
- **Mode B — Eventual-outcome diagnostic (τ²-Bench).** All prefixes selected by the
  **same finalized outcome-independent checkpoint policy as Mode A** (Rule 1/Gate 2),
  without onset-based exclusion — not every raw step of the source trajectory. If Mode
  A and Mode B used different checkpoint constructions, the transfer comparison would
  conflate task-definition differences with checkpoint-construction differences,
  making results harder to interpret. Supports: FAR, raw Recall, alert burden.
  AUROC/AUPRC/Brier/ECE *can* still be computed here, but must be reported under a
  different name — "eventual-outcome ranking/calibration under partial traces" — and
  never described as measuring prospective warning or placed in direct comparison with
  TerminalBench's Mode A numbers.

| Metric | τ²-Bench (Mode B) | TerminalBench (Mode A) |
|---|---|---|
| AUROC / AUPRC | Eventual-outcome diagnostic only | Prospective |
| Brier / ECE | Eventual-outcome diagnostic only | Prospective |
| FAR | ✓ | ✓ |
| Prospective Recall@FAR | Not identifiable — no onset boundary | ✓ |
| Raw Recall | ✓ | ✓ |
| Lead time | ✗ | ✓ |
| Alert burden | ✓ | ✓ |

What τ²-Bench actually validates, precisely: *whether learned warning behavior,
trained and thresholded entirely on TerminalBench, transfers to an independently
sourced trajectory distribution with known eventual outcomes* — not "the same
prospective-warning result reproduced on a second dataset." Say it this way in the
paper. This distinction resolves a further consequence: τ²-Bench's calibration numbers
(if reported) confirm calibration of *eventual-outcome risk over available partial
trajectories*, not "prospective reliability" — don't let the two get conflated in the
Results section either. **Interpretation discipline for later (not a protocol change, but keep this distinction
ready for the Discussion section):** if τ²-Bench transfer looks weak, distinguish
*representation transfer* (do the same trace features mean roughly the same thing
across datasets — this is what Rule 9's feature-compatibility check partly guards) from
*predictive transfer* (does a model that learned well on TerminalBench still
rank/risk-score τ²-Bench outcomes effectively, given compatible features). "Retry/error
signals mean different things across environments" and "the model just doesn't
generalize despite compatible semantics" are different findings and call for different
follow-up — don't collapse them into one vague "transfer was weak" sentence.

Remaining dependency on data: confirm in Gate 1 that
TerminalBench actually contains enough episodes to support a real three-way
TRAIN/CALIBRATION/TEST split; if not, this policy needs revisiting.

Gate before implementation: download one real file from each, inspect actual field
names, confirm `incorrect_stages` in Tracebench is genuinely a step index. Do not trust
assumed schemas.

---

## 5. Frozen evaluation protocol (eleven rules — correctness constraints, not style choices)

1. **Checkpoints — outcome-independent, episode-symmetric (AMENDED).** The earlier
   anchor-then-stride design was rejected: forcing checkpoints at `t_onset`/`t_onset−1`
   uses ground truth the evaluator only has in hindsight. That is not feature leakage
   (the monitor still only sees `e_1…e_t`) but it is *evaluation-opportunity* leakage —
   failing episodes would get a guaranteed near-onset scoring point that successful
   episodes have no equivalent of, which contradicts the word "prospective."

   **Primary schedule (frozen in principle, one parameter pending Gate 1):** checkpoint
   selection must be identical in construction for every episode regardless of outcome,
   and must not use `failure_onset_step` or (to minimize evaluator-side future-information
   use as well) ideally not `T` either. Candidate: score the first 30 valid checkpoints by
   **absolute step index** (t = 1…30, or t = 1…T when T ≤ 30) rather than a schedule
   relative to total trajectory length. This must not be locked until trajectory-length
   distributions for both datasets are inspected (Gate 1) — if one dataset is
   predominantly short and the other long, a fixed absolute window could silently become
   a dataset-dependent observation window, which would need to be stated as an explicit
   scope limitation ("early warning within the first 30 steps") rather than discovered
   after the fact.

   **Secondary diagnostic analysis (not part of the primary prospective claim):**
   onset-anchored checkpoints (t = t_onset, t = t_onset − 1) may still be used, but only
   as a separately labeled fine-grained probe of behavior immediately around failure
   onset — never mixed into the primary AUROC/AUPRC/Recall@FAR/calibration/lead-time
   results.
2. **Feature leakage.** X_t = f(e_1, …, e_t) only. No future event, future-derived
   statistic, final outcome, onset label, or future-dependent metadata may enter the
   feature vector.
3. **Episode-level split.** All prefixes of one episode stay in exactly one of
   {train, calibration, test}. Never split prefixes of the same episode across sets.
4. **Calibration isolation.** Calibration fit only on calibration episodes. Test set
   untouched until final evaluation — no test-derived threshold, feature choice, or
   checkpoint rule.
5. **Alert timing.** Valid alert: t_alert ≤ t_failure_onset →
   lead_time = t_failure_onset − t_alert (0 at onset). Alerts after onset are "late
   detections": counted toward raw recall, excluded from the lead-time distribution,
   reported separately.
6. **Terminal-event sanitization.** Outcome fields (`episode_outcome`,
   `failure_onset_step`, `terminal_reason`, `reward`) are extracted into
   evaluation-only metadata *before* sanitization, then stripped from the event stream
   the monitor sees — including at t = T. This is what makes t = T a legitimate
   checkpoint instead of forcing a t = T−1 cutoff. **Explicit schema invariant:** the
   retained terminal marker may indicate *that* a step is terminal (`action_type =
   TERMINAL`) but must never indicate *what the outcome was* — no `TERMINAL_FAILURE`,
   no `terminal_reason` field, no content that discloses success/failure, even
   implicitly.
7. **Statistical unit = episode, not prefix.** Prefixes from one episode are correlated,
   not independent observations. Every bootstrap CI (AUROC, AUPRC, calibration,
   Recall@FAR, lead time) must resample at the episode level, never the prefix level.
   Apply multiple-comparison correction (e.g. Holm) once H/M/S(/L) are compared across
   several metrics. Literature-reported numbers (PrefixGuard, AgentForesight, Trajectory
   Guard) are cited as reference points and must never be pooled with locally measured
   numbers as if directly comparable — different hardware, different implementations.
   **Aggregation approach — FROZEN default: episode-balanced prefix weighting.** For
   prefix-level metrics (AUROC, AUPRC, Brier, ECE), each episode i with n_i scored
   prefixes gets each of its prefixes weighted 1/n_i, so every episode contributes one
   total unit of weight regardless of length — a 30-prefix episode does not outweigh a
   5-prefix episode. Uncertainty still comes from episode-level cluster bootstrap. This
   choice is deliberate, not a coding convenience: it matches the estimand already
   implicit in FAR/Recall being episode-level ("how well does the monitor perform
   across episodes, regardless of length?") rather than the alternative estimand
   ("how well does it rank a randomly selected checkpoint?"), keeping every metric
   consistent about what population quantity is being measured.
8. **Task-definition leakage (training/calibration objective).** Distinct from Rules
   2–4: even when the monitor only *sees* steps 1…t at inference, training/calibration
   on post-onset prefixes of failed episodes teaches the model to recognize
   already-obvious collapse, not prospective risk. Frozen rule: for model fitting and
   calibration, **failed episodes contribute prefixes only through onset** (t ≤
   t_onset); successful episodes contribute all valid prefixes. Post-onset prefixes
   (t > t_onset) are evaluation-only — they feed the late-detection/raw-recall
   analysis, never the training or calibration objective. Three prefix types now exist,
   each answering a different question:

   | Prefix type | t vs. onset | Role |
   |---|---|---|
   | Pre-onset | t < t_onset | Genuine prospective-warning training + evaluation |
   | Onset | t = t_onset | Valid zero-lead warning; training + evaluation |
   | Post-onset | t > t_onset | Evaluation-only diagnostic (late detection); excluded from training/calibration |
9. **Cross-dataset feature compatibility.** Since training/calibration happens only on
   TerminalBench (Section 4) while τ²-Bench is evaluated with the frozen model, any
   feature used by M/S(/L) must be computable, with the same definition and information
   boundary, on **both** datasets. A feature available only on TerminalBench (e.g. a
   timing field τ²-Bench's format may lack) cannot silently enter the shared model — it
   must either be dropped from the common feature set or reserved as a
   TerminalBench-only diagnostic reported separately, never mixed into the primary
   cross-dataset comparison. **Resolution (frozen now):** the common-feature model
   (features computable on both datasets) is the primary transferable model and the one
   whose τ²-Bench result is reported as the transfer/generalization claim. A
   richer, TerminalBench-only feature set may additionally be trained and reported, but
   strictly as a TerminalBench-internal diagnostic — never used to produce a τ²-Bench
   number, since that would compare a richly-featured model's performance against a
   deliberately impoverished input representation and mislabel the gap as
   "generalization failure." Confirm actual field overlap during Gate 1 inspection.
10. **Canonical outcome definition (NEW — closes a target-definition gap the
    cross-dataset transfer claim depends on).** The protocol fixes "failure-target
    definition" as one of its stated contributions, but that requires one
    benchmark-independent binary target, not two datasets' native fields silently
    assumed to mean the same thing. Frozen principle: define
    `eventual_success` / `eventual_failure` as *the benchmark's own native
    success/failure determination under its stated evaluation criteria* (e.g.
    TerminalBench's reward/pass criterion, τ²-Bench's task-completion reward), then
    explicitly map each dataset's native outcome field to this canonical target before
    any modeling or evaluation step — never consume a native field directly without
    going through this mapping. This matters specifically because the frozen
    TerminalBench model is transferred to τ²-Bench: if the two datasets' native
    "failure" concepts differ in what they actually certify, a weak transfer result
    would be confounded with target mismatch rather than genuine generalization
    failure, undermining the transfer claim in Section 4. **Scope constraint:** the
    mapping standardizes the *representation* of each benchmark's own official outcome
    determination — it must not invent a new failure definition merely to make the two
    datasets more comparable; each dataset's native success criterion is preserved,
    only its encoding is unified. The exact field-to-target mapping is decided at Gate
    1 from real schemas; the existence and necessity of the mapping step, and this
    scope constraint, are frozen now.
11. **Training-objective weighting vs. evaluation weighting — must be a conscious,
    stated choice, not an inherited default.** Rule 7 freezes episode-balanced
    weighting for the *evaluation* estimand (AUROC/AUPRC/Brier/ECE). That does not
    automatically apply to *training* M/S — training and evaluation optimize different
    things, and naively training on every eligible prefix with equal weight lets
    longer episodes dominate the learned model even though evaluation treats all
    episodes equally, a training/evaluation objective mismatch. **Frozen default:**
    training also uses episode-balanced sample weighting (each episode's eligible
    prefixes weighted 1/n_i, matching Rule 7's evaluation estimand), chosen for
    consistency between what the model is optimized for and what it is scored on. If
    this default is changed to prefix-weighted training for a specific reason
    discovered during implementation, document the reason explicitly — do not let the
    choice happen silently as a side effect of whatever the training loop's default
    behavior is.

**One-paragraph version for the paper's Methodology section:**

> Checkpoints are evaluated according to an outcome-independent, episode-symmetric
> schedule (candidate: the first 30 valid steps by absolute index, or all steps when
> T ≤ 30; final form pending trajectory-length distribution inspection — see Gate 2).
> At checkpoint t, a monitor accesses only steps 1…t; terminal events are stripped of
> outcome-bearing content prior to feature computation at every checkpoint, including
> t = T. Splitting is performed at the episode level across three disjoint sets. An
> alert at t is valid iff t ≤ t_onset, giving lead_time = t_onset − t_alert (0 at
> onset); alerts after t_onset are excluded from lead-time analysis and reported as
> late detections. Trajectories without a known failure-onset label contribute to
> AUROC/AUPRC/calibration/FAR only.

---

## 6. Frozen method families

| Code | Family | Notes |
|---|---|---|
| H | Heuristic monitor | Rule-based: retry count, tool-error rate, repeated actions, latency trend. **Training-free** — no fitted parameters; only its alert threshold is calibrated (on CALIBRATION episodes, per the frozen threshold procedure in Section 8). Pipeline must not force H through a meaningless training phase. |
| M | Classical ML | Logistic regression / XGBoost over engineered features. Trained on TRAIN, threshold calibrated on CALIBRATION. |
| S | Sequence monitor | Small GRU/1D-CNN over the feature time series. Trained on TRAIN, threshold calibrated on CALIBRATION. |
| L | Semantic/LLM monitor | Optional. Local open-weight model only. Project must survive without it. Likely training-free (prompted, not fine-tuned) — threshold calibration still applies. |

Reference-only (cited, never re-implemented): PrefixGuard, AgentForesight, Trajectory Guard.

---

## 7. Remaining gates before implementation

Three of the original four gate topics are now resolved by decisions frozen above.
Two genuine data-dependent gates remain, plus the L hardware decision.

1. **[GATE — data-dependent] Episode counts, label availability, and length
   distributions.** Count *episodes*, not prefixes, in τ²-Bench `historical_trajectories`
   and Tracebench. This determines statistical power and whether CIs will be stable.
   Confirm which fraction of episodes are failures (class balance) and, for Tracebench,
   whether `incorrect_stages` has a deterministic, defensible onset definition (first
   incorrect stage? first irreversible error? — do not assume; inspect and decide
   explicitly). **Also plot trajectory-length distributions for both datasets** — this
   directly decides the final form of the checkpoint schedule (Gate 2). **Also compute:
   what fraction of Tracebench's failed episodes have onset occurring after the
   candidate 30-step horizon** — if a large share of true failures only manifest past
   step 30, the primary schedule is measuring "early warning within the first 30
   steps," and that must become an explicit, stated scope limitation rather than an
   unstated one. **Also compute the complementary breakdown for TerminalBench: what
   fraction of failed episodes have onset within the candidate horizon (genuinely
   evaluable for prospective warning) vs. no eligible pre-onset/onset checkpoint at all
   under the horizon (effectively unusable for the prospective claim)** — this tells
   you directly whether the chosen horizon leaves enough usable prospective-warning
   observations, not just what fraction is excluded. **Also confirm TerminalBench has enough episodes to support a real
   three-way TRAIN/CALIBRATION/TEST split** — now load-bearing, since Section 4 makes
   TerminalBench the sole training/calibration source for both datasets. **Also confirm
   feature-field overlap between τ²-Bench and TerminalBench** per Rule 9. **Also
   confirm the exact native success/failure field in each dataset (reward value?
   explicit status field? task-completion flag?) and write the canonical
   `eventual_success`/`eventual_failure` mapping explicitly per Rule 10, before either
   dataset's outcomes are consumed by any code.**

2. **[GATE — data-dependent] Primary checkpoint schedule finalized against real length
   distributions.** Per Rule 1: confirm whether "first 30 steps by absolute index" is
   safe to use as the primary schedule, or whether it creates a dataset-dependent
   observation-window bias (e.g. if τ²-Bench trajectories are mostly short and
   TerminalBench mostly long). If biased, define the fallback online sampling policy
   before implementation, not during. The *principle* is already frozen (deterministic,
   outcome-independent, identical construction per episode) — only the exact horizon K
   is pending.

3. **[RESOLVED] τ²-Bench training/calibration policy.** Closed by the dataset-role
   decision in Section 4: TerminalBench is the sole training/calibration source;
   τ²-Bench is evaluation-only. No further decision needed — only the residual data
   check folded into Gate 1 above (TerminalBench episode sufficiency, feature overlap).

4. **[Hardware decision, not a data gate] L's status**: reference-only from the start,
   or attempted contingent on a confirmed local model + VRAM budget test. Whichever is
   chosen, the contribution statement (Section 1) must match — already softened above
   to not overclaim.

## 8. Metric hierarchy (headline metric deferred until Gate 1 is closed)

**Metric unit taxonomy (frozen now — no data dependency):**

| Metric | Natural unit | Notes |
|---|---|---|
| AUROC / AUPRC | Prefix-level scores | Ranking metric over all scored checkpoints; episode-aware at inference, not an episode-level decision |
| Brier / ECE | Prefix-level probabilities | Same as above |
| FAR | Episode | An episode is a false alarm iff it eventually succeeds and received ≥1 alert (any t) |
| Recall@FAR | Episode | A failed episode is "recalled" iff it received ≥1 valid alert (t ≤ t_onset) at the frozen threshold |
| Lead time | Failed episode | Earliest valid alert's t, per Rule 5 |
| Alert burden | Episode (secondary) | Count of alerts per episode — reported separately, never folded into FAR/Recall, since two episodes can share identical FAR/Recall while differing sharply in alert frequency |

Do not conflate prefix-level ranking metrics with episode-level operational metrics when implementing the evaluator — they answer different questions and need separate code paths. **Also do not conflate τ²-Bench (Mode B, eventual-outcome diagnostic) and TerminalBench (Mode A, prospective) values for the same metric name — see Section 4's evaluation-mode table. An AUROC from each dataset answers a different question and must be labeled and reported as such.**

**Ranking-stability statistic (frozen now — this is the core comparative object per
Section 1, and needs a reproducible definition, not an intuition; CORRECTED TWICE —
the first draft's worked example had wrong arithmetic; this draft fixes an unhandled
2–2 modal-direction split and a denominator inconsistency in the first correction).**
"Does the H/M/S ordering stay consistent across metrics?" is ambiguous until
operationalized. With 3 mandatory methods there are C(3,2) = 3 method pairs (H–M, H–S,
M–S); with 4 primary Mode A metrics (AUROC, AUPRC, Recall@FAR, ECE — all oriented
higher-is-better, i.e. ECE's sign flipped for comparison purposes only, which does not
imply it measures the same property as the discrimination metrics AUROC/AUPRC — note
this explicitly in the paper) that gives up to 3 × 4 = 12 pairwise-method × metric
comparisons.

**Step 1 — the raw pairwise-direction table is itself a first-class reported result,
not just an input to a summary statistic.** Report the full table (3 pairs × 4
metrics, each cell = winner or tie) in the paper regardless of what the summary
statistic says — a clean 50% PDA can hide a genuinely important finding (metrics
splitting evenly, no stable conclusion existing at all), and the table prevents that
from being hidden.

| Pair | AUROC | AUPRC | Recall@FAR | ECE |
|---|---|---|---|---|
| H vs M | | | | |
| H vs S | | | | |
| M vs S | | | | |

**Step 2 — point-estimate comparison, with an explicit tie rule (frozen, tolerance
value set during implementation before results are seen, never after):** for each
pair and metric, the point estimates are compared; if equal within the predefined
tolerance, that cell is a metric-level tie; otherwise the higher-is-better direction
(ECE reversed) determines the winner.

**Step 3 — Pairwise Direction Consistency (PDC), replacing PDA (RETIRED — PDA's
exclusion of no-majority pairs was a real design flaw, not just an edge case: it let
the exact pair demonstrating maximal instability contribute nothing to the headline
number, which could make the statistic look reassuring while hiding the specific
problem it exists to surface).** For each method pair, among that pair's non-tied
metrics (W wins + L losses, W+L ≤ 4): `PDC_pair = max(W, L) / (W+L)`. With 4 non-tied
metrics: 4–0 → 1.00, 3–1 → 0.75, 2–2 → 0.50. No special-casing, no exclusion — a 2–2
split scores 0.50, correctly the worst possible value, rather than disappearing.

**Coverage (FIX — a prior draft let PDC be computed from as little as 1 non-tied
metric and reported as if equally strong as a 4/4 case).** Report
`Coverage_pair = (W+L) / 4` alongside every PDC_pair. `PDC = 1.00, Coverage = 0.25`
(one informative metric, three ties) must never be presented as equivalent evidence to
`PDC = 1.00, Coverage = 1.00`.

**Overall PDC (FIX — the previous draft's "mean across the 3 pairs" was undefined
when a pair has W+L = 0, i.e. all 4 metrics tied for that pair):** PDC_overall = mean
of PDC_pair **over pairs with W+L > 0 only** (informative pairs). Report the
informative-pair count explicitly alongside it (e.g. `PDC_overall = 0.92 over 2/3
informative pairs`) — an all-4-tied pair is a genuine result (identical performance
under every metric for that pair) and is excluded from the mean rather than forced
into it, but its existence must never be silently dropped from the report.

**Secondary statistic:** Kendall's τ or Spearman correlation between the per-metric
rankings, reported alongside PDC and the raw table — not a replacement for either.

**Terminology guard:** PDC measures internal consistency of comparative conclusions
*across the four evaluation metrics under this protocol* — it does not measure
agreement with any specific prior published ranking. State it as "metric/ranking
consistency under the common protocol," not "replication of prior published
rankings" — the paper is not claiming to reproduce any specific paper's numbers.

**Ranking vs. evidence strength are two separate things, not one blended "tie"
concept:** the point-estimate rules above (Steps 2–3) determine the ranking, PDC, and
raw table entirely on their own — CI overlap never redefines a win as a tie.
Separately, report evidence strength from the episode-cluster bootstrap (Rule 7): for
each pairwise win, state precisely whether the bootstrap 95% CI for the paired
difference excludes zero ("point-estimate win with bootstrap interval excluding
zero") or includes it ("point-estimate win with bootstrap interval containing zero")
— avoid looser phrasing like "statistically separated" that implies a specific test
without naming it. Both are valid, reportable outcomes; the protocol does not require
every win to be statistically significant to be meaningful, but must never present an
interval-containing-zero win as equivalent in strength to an interval-excluding-zero
one.

**Lead time is explicitly excluded from the primary ranking-stability statistic** (not
merely omitted by oversight) — it exists only in Mode A, is measured at the
failed-episode level rather than matching AUROC/AUPRC/Recall@FAR/ECE's broader
population, and rewards earlier alarms in a way that isn't comparable to
discrimination/calibration quality. Lead time remains a separate operational analysis.

**Threshold-selection procedure for Recall@fixed-FAR (frozen now — fully reproducible, no data dependency; CORRECTED from a previous round's error):**

1. Fit the model on TRAIN episodes only.
2. On CALIBRATION episodes only, evaluate every candidate threshold's episode-level FAR
   (episode = false alarm iff it eventually succeeds and received ≥1 alert at that
   threshold) and episode-level recall. Among thresholds with calibration FAR ≤ target
   FAR, select the one that **maximizes calibration-set recall** — not simply the
   highest threshold satisfying the constraint. ("Highest threshold satisfying the
   constraint" is the most conservative choice consistent with the constraint, not the
   best one for the stated headline metric — it can leave achievable recall on the
   table. This was wrong in an earlier draft of this rule and is corrected here.) Ties
   in recall are broken by lower achieved FAR; if still tied, by the higher threshold.
3. Freeze that threshold.
4. Apply the frozen threshold, unchanged, to TEST episodes. Report both the resulting
   test-set Recall and the resulting test-set FAR (which may drift slightly from the
   calibration-set FAR — report this drift, don't hide it).
5. Test episodes are never used to choose or adjust the threshold, under any
   circumstance.

Do not paste the checkpoint-schedule paragraph below into the actual paper yet — it is explicitly provisional. Once Gate 2 closes, regenerate it from the final frozen schedule rather than hand-editing this one.

Do not pick the headline result before seeing the data. The current structure:

- **Primary scientific question:** does standardization change the comparative
  conclusions across method families? — answered primarily from TerminalBench (Mode A,
  the only dataset supporting full prospective evaluation).
- **Primary operational metric (likely):** Recall@fixed-FAR — deployable warning
  systems are judged on missed failures under a controlled false-alarm budget.
- **Early-warning metric:** lead time — TerminalBench (Mode A) only.
- **Supporting diagnostic metrics:** AUROC, AUPRC, Brier/ECE, compute (wall-clock
  latency + peak memory + throughput for locally measured methods; literature
  numbers kept visibly separate, never pooled).
- **τ²-Bench's role:** a secondary generalization check (Mode B, eventual-outcome
  diagnostic) — evidence about transfer, not a second instance of the primary
  prospective result. Do not let it silently inflate the paper's headline claim.
- **Headline result:** not predetermined. Two candidate story shapes exist —
  "Method X wins under fixed-FAR on TerminalBench, and this transfers to τ²-Bench"
  vs. "rankings shift substantially across ranking/calibration/operational metrics,
  and/or transfer is weaker than in-benchmark performance" — and the actual data
  decides which one the abstract tells.

**Correct sequence from here:** inspect real data → close Gate 1 (episode counts,
class balance, onset definition, TerminalBench sufficiency, feature overlap) → close
Gate 2 (checkpoint horizon) → decide L's status (item 4) → formalize exact metric
definitions → freeze the headline metric → write the master implementation spec.
Not before.

## 9. Other open items (lower stakes, resolve opportunistically)

- [ ] Exact stride formula for checkpoints beyond the anchor set (`len // 30` vs. log-spaced) — **superseded**, see Gate 2 in Section 7 instead.
- [ ] Target IEEE venue — confirm with advisor whether "submitted" satisfies the requirement, since genuine publication cannot be guaranteed inside 2 months
- [ ] Number of seeds / bootstrap iterations (episode-level, per Rule 7)
- [ ] Precise wording guard: never imply "nobody compared heuristics and LLMs" — the claim is narrower ("no common reusable prospective-warning protocol across method families"). Same caution applies to internal novelty-audit language ("checked against the closest neighbors") — useful for viva defense, but the eventual paper should hedge with "to the best of our knowledge," not assert exhaustiveness.
- [x] **Multi-alert collapsing — DECIDED.** Lead time is defined by the earliest valid alert on the episode (smallest t with a valid alert). No debouncing/persistence requirement by default — that would add an unneeded hyperparameter. Alert frequency / alert burden may be reported as a separate secondary statistic if chatter turns out to matter, but does not change the primary lead-time definition.
- [x] **False-alarm rate unit — DECIDED.** FAR is defined at the **episode level**: a successful episode counts as one false alarm if it received *any* alert, regardless of how many. This prevents a long, chattier successful episode from being penalized proportionally more than a short one under the primary metric. Alert frequency/workload per episode may be reported separately as a secondary diagnostic.
- [x] **Episode-length weighting in aggregate metrics — DECIDED.** Frozen as episode-balanced prefix weighting (1/n_i per prefix) for AUROC/AUPRC/Brier/ECE, per Rule 7. Bootstrap dependence (resample whole episodes) was already fixed; this closes the remaining point-estimate weighting question.
- [ ] **Prospective recall vs. raw recall — must both exist as distinct reported outputs, not collapsed into one number.** Prospective recall = failed episodes alerted at t ≤ t_onset (the actual early-warning claim). Raw recall = failed episodes alerted at any t, including post-onset late detections. These will differ, and conflating them overstates the early-warning result. Neither needs to be *the* headline metric, but the evaluator must compute and report both.
- [ ] **Terminology caution:** `failure_onset_step` is a provisional name, not a confirmed semantic. Do not finalize it as "failure onset" in the paper until Gate 1 confirms what Tracebench's `incorrect_stages` actually annotates (first incorrect step vs. first irreversible/decisive error vs. first human-flagged deviation). The eventual field name may need to become `first_incorrect_step` or `decisive_error_step` instead — decide from the real annotation semantics, not the source field's name.

---

## 10. Immediate next actions (no coding — verification and decisions only)

1. Clone `sierra-research/tau-bench`, locate `historical_trajectories/`, **count episodes**, check class balance, **plot trajectory-length distribution**, open one file to read real structure.
2. Load `Contextbench/Tracebench` split, **count episodes**, check class balance, **plot trajectory-length distribution**, print one row, and decide the operational definition of failure onset from `incorrect_stages` before calling it a label.
3. Close Gate 2 and decide L's status (Section 7, item 4) using what Gate 1's inspection reveals.
4. Start a research log now (per the Bible's Section 51 policy) — record these inspection findings as the first entries, so the eventual Methodology section is reconstructed from notes, not from memory of code.
5. Only once 1–4 are done does the headline metric get frozen (Section 8) and implementation begin.

---

## 11. Timeline anchor (unchanged from the trimmed plan, restated for reference)

- **Weeks 1–2:** ingestion, schema, prefix generation, leakage guards, H/M baselines
- **Weeks 3–4:** S monitor, common evaluator, main experiment on both datasets
- **Weeks 5–6:** metric-sensitivity experiment, calibration, error analysis, stats, writing starts
- **Weeks 7–8:** full draft, revision, similarity check, submission
- **Months 3–5:** lightweight results app, documentation, demo prep — after the paper is submitted, not before

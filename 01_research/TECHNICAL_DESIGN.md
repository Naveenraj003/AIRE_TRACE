# AIRE-Trace — Technical Design

**Status: architecture and module contracts frozen. Dataset-specific implementation
parameters (marked 🔲 TBD — Gate 1 throughout) are intentionally not filled in yet.**
Filling them in before Gate 1's real-data inspection would mean building against
assumed schemas — the protocol document explicitly forbids this
(`AIRE-Trace_Frozen_Protocol_and_Plan.md`, dataset section: "Do not trust assumed
schemas"). This document does not restate protocol rules; it references them by
number and shows where each is enforced in code. **`dataset_prep.py`, referenced
throughout below, is a preliminary sketch written before Gate 1 — treat it as
untrusted starting material, not as evidence those modules are already correct; see
`AGENTS.md` Section 2.**

---

## 1. Pipeline architecture

```
τ²-Bench raw files          TerminalBench raw files
        │                            │
        ▼                            ▼
┌───────────────┐            ┌───────────────┐
│ Ingestion (A)  │            │ Ingestion (B)  │   ── dataset-specific parsers
└───────┬───────┘            └───────┬───────┘
        │                            │
        └──────────────┬─────────────┘
                        ▼
              Canonical Trace Schema        ── Run + Event dataclasses
                        │
                        ▼
              Outcome Mapping (Rule 10)      ── native field → eventual_success/failure
                        │
                        ▼
              Terminal Sanitization (Rule 6) ── strip_terminal_leakage()
                        │
                        ▼
              Episode-level Split (Rule 3)   ── TerminalBench only: TRAIN/CALIB/TEST
                        │                        τ²-Bench: evaluation-only pool
                        ▼
              Prefix Generation (Rule 1)      ── outcome-independent checkpoint policy
                        │
                        ▼
              Feature Extraction (Rules 2,9)  ── leakage-safe, cross-dataset compatible
                        │
        ┌───────────────┼───────────────┬───────────────┐
        ▼               ▼               ▼               ▼
    H (heuristic)   M (classical ML)  S (sequence)   L (optional, local LLM)
        │               │               │               │
        └───────────────┴───────┬───────┴───────────────┘
                                 ▼
                    Threshold Calibration (Section 8)
                    ── CALIBRATION episodes only, frozen threshold
                                 ▼
                    Common Evaluator
                    ── Mode A (TerminalBench TEST): full prospective metrics
                    ── Mode B (τ²-Bench): eventual-outcome diagnostic metrics
                                 ▼
                    Statistical Layer (Rule 7)
                    ── episode-cluster bootstrap, PDC + coverage, raw pairwise table
                                 ▼
                    Results Storage  →  Results App (thin UI)
```

## 2. Module contracts

### 2.1 Ingestion (`ingestion/tau2.py`, `ingestion/terminalbench.py`)
Reads raw source files, produces `Run` + `List[Event]` in the canonical schema
(already sketched in `dataset_prep.py`). Dataset-specific; each source gets its own
parser rather than one parser trying to handle both.

- 🔲 TBD — Gate 1: exact τ²-Bench `historical_trajectories/` JSON field names.
- 🔲 TBD — Gate 1: exact Tracebench HF row schema (`steps`, `incorrect_stages` format).

### 2.2 Outcome Mapping (`canonical/outcome.py`)
Implements protocol Rule 10. One function per dataset:
`map_tau2_outcome(raw) -> eventual_success: bool` and
`map_terminalbench_outcome(raw) -> eventual_success: bool`, each documented with the
native field it reads and the benchmark's own success criterion it preserves.

**Provenance requirement (do not discard the native field after mapping):** the
canonical `Run` record stores both `eventual_success` (the mapped canonical target)
*and* the raw native outcome value it was derived from (e.g. `native_outcome_raw`),
plus which mapping rule/version produced it. `AGENTS.md`'s prohibition is on
*modeling/evaluation code consuming the native field directly* — it is not a
requirement to delete the native field's provenance. Keeping it lets the mapping be
demonstrated and re-validated later ("this dataset's native reward field was mapped to
`eventual_success` under this exact rule") without re-parsing raw source files.

- 🔲 TBD — Gate 1: which native field in each dataset is the authoritative
  success/failure determination (reward value? explicit status field? task-completion
  flag?).

### 2.3 Sanitization (`canonical/sanitize.py`)
Implements protocol Rule 6. `strip_terminal_leakage(raw_event) -> cleaned_event`,
applied to every event at ingestion, not just the last one. Already drafted in
`dataset_prep.py`.

### 2.4 Splitting (`canonical/split.py`)
Implements protocol Rule 3 + Section 4's dataset roles.
`make_episode_disjoint_split(run_ids, ...) -> (train_ids, calib_ids, test_ids)`,
already drafted in `dataset_prep.py`, applied to TerminalBench only. τ²-Bench episodes
are never split — the entire dataset is the evaluation-only Mode B pool.

- 🔲 TBD — Gate 1: confirm TerminalBench has enough episodes for a real three-way
  split (protocol Section 7, Gate 1 checklist).

### 2.5 Prefix Generation (`canonical/prefixes.py`)
Implements protocol Rule 1. `generate_prefixes(run, events) -> List[PrefixRow]`,
already drafted in `dataset_prep.py`. Must apply the **same finalized checkpoint
policy to both datasets** (Section 4's Mode B note) — this module is shared, not
dataset-specific, unlike ingestion.

- 🔲 TBD — Gate 1 / Gate 2: exact checkpoint horizon K (candidate: first 30 steps by
  absolute index; confirm against real trajectory-length distributions before
  finalizing).

### 2.6 Feature Extraction (`canonical/features.py`)
Implements protocol Rules 2 and 9. `compute_features_up_to(events, t) -> Dict`,
already sketched in `dataset_prep.py`. The feature set consumed by M/S/L must be the
**common** feature set (Rule 9) — a separate, richer TerminalBench-only feature set
may exist for the TerminalBench-internal diagnostic model, but lives in a clearly
separate code path, never silently merged into the primary one.

- 🔲 TBD — Gate 1: which candidate features (retry_count, tool_error_count,
  unique_tools, latency, etc.) are actually computable identically on both datasets.

### 2.7 Method Families (`methods/heuristic.py`, `methods/classical_ml.py`,
`methods/sequence.py`, `methods/llm_monitor.py` [optional])
Each implements a common interface: `fit(train_prefixes)` (no-op for H — training-free,
per protocol method-families table), `predict_risk(prefix_features) -> float`. Training
uses episode-balanced sample weighting by default (Rule 11) for M/S/L.

**Interface refinement (deferred to post-Gate-1, noted now so it isn't lost):** H and M
naturally consume a flattened feature vector at checkpoint t. S is a sequence model and
needs the *ordered* feature sequence up to t, not a single flattened vector — collapsing
it to match H/M's signature would defeat the point of using a sequence model at all. L
(if built) consumes a semantic/text representation of the prefix. The common interface
should therefore be built around a `Prefix`/`FeatureSequence` abstraction that each
method's adapter reduces to what it actually needs (H/M: last/aggregated vector; S: full
ordered sequence; L: rendered text), rather than forcing every method into one flat-
vector call signature. This does not change the architecture diagram in Section 1 — it's
an implementation-level contract refinement, to be finalized once Gate 1's real feature
set is known.

- 🔲 Hardware decision (not data-dependent): whether L is implemented at all, gated on
  a local-model VRAM budget test against the RTX 2050's 4GB.

### 2.8 Threshold Calibration (`evaluation/threshold.py`)
Implements the frozen threshold-selection procedure (protocol Section 8): fit on
TRAIN, sweep thresholds on CALIBRATION, select the one maximizing calibration recall
subject to FAR ≤ target (tie-break: lower FAR, then higher threshold), freeze, apply
unchanged to TEST.

**Single-threshold contract across modes (explicit, not just implied):** calibration
happens exactly once per method, on TerminalBench CALIBRATION episodes only. The
resulting frozen threshold is applied unchanged to **both** TerminalBench TEST (Mode A)
and τ²-Bench (Mode B) — τ²-Bench never triggers a separate calibration pass. The
module's API should make a second, dataset-specific threshold structurally
impossible to produce (e.g. `calibrate(method) -> Threshold` takes no dataset
argument at all, only `apply(threshold, prefixes) -> alerts` does), rather than relying
on callers to remember not to recalibrate. A second threshold for τ²-Bench would
silently convert the transfer experiment into two separate in-distribution
experiments, defeating its purpose.

### 2.9 Common Evaluator (`evaluation/metrics.py`)
Computes the full metric set from Section 4's Mode A/B table: AUROC, AUPRC, Brier, ECE
(prefix-level, episode-balanced weighted per Rule 7), FAR, prospective Recall@FAR, raw
Recall, lead time, alert burden (episode-level). Every returned metric is tagged with
its Mode (A/B) and its dataset — no unlabeled metric value should be producible by this
module's API.

**Invalid combinations are mechanically rejected, not just mislabeled if requested
(strengthens the existing labeling requirement into an enforced one):** the API raises
an error rather than returning a value for e.g. `mode=B, metric=prospective_recall_at_far`
or `mode=B, metric=lead_time` (τ²-Bench has no onset boundary — these are structurally
undefined for it, not merely inadvisable), and for any Mode A request framed as an
"eventual-outcome diagnostic" interpretation. Enforcing this at the API boundary means
Mode A/B separation can't be silently bypassed by a caller who forgets the labeling
convention.

**FAR target — frozen now, not deferred:** the primary operating point is
`FAR_target = 0.05` (5%), fixed before the main experiment runs, consistent with the
threshold-selection procedure in Section 8 of the protocol document. Additional target
values (e.g. 1%, 10%) may be run as a secondary sensitivity analysis, but the paper's
headline Recall@FAR result uses this single frozen value — it does not get chosen
after seeing which value produces the best-looking result.

- 🔲 TBD — implementation-only, not conceptually open: exact ECE bin count/binning
  rule (fix a specific value, e.g. 10 equal-width bins, and document it — any
  reasonable fixed choice is acceptable as long as it's fixed and stated, per the
  earlier review's point that two implementations can disagree if this isn't pinned
  down).
- 🔲 TBD — implementation-only: threshold candidate set definition (unique calibration
  scores vs. a fixed probability grid — either is fine, pick one and document it).

### 2.9b Compute Cost (`evaluation/cost.py`)
Currently underspecified — the protocol and PRD require compute accounting as part of
the contribution, not an afterthought, so it gets its own module rather than living
implicitly inside `metrics.py`. Measures, per method, for locally run H/M/S/L: wall-
clock inference latency per prefix, peak memory, and
throughput (prefixes/second). **Memory is reported as two explicit fields, not one
coarse "peak memory" value** — `peak_cpu_ram` and `peak_gpu_vram` — since a method can
consume both simultaneously (e.g. S running on GPU still has CPU-side overhead); report
both for every method regardless of which is expected to dominate, plus a `device`
field stating what actually ran it. Literature-reported figures (PrefixGuard, AgentForesight,
Trajectory Guard) are recorded separately in the same module's output structure but
tagged `source: literature` vs. `source: local_measurement` — never merged into one
column, per Rule 7's prohibition on pooling locally measured and literature-reported
numbers as if comparable.

- 🔲 TBD — implementation-only: exact measurement methodology (e.g. warm-up runs
  excluded, number of repetitions averaged, measured on CPU vs. GPU per method as
  applicable) — pin a specific protocol and document it in `RESEARCH_LOG.md` before
  the main experiment runs, not after.

### 2.10 Statistical Layer (`evaluation/stats.py`)
Implements protocol Rule 7 (episode-cluster bootstrap) and Section 8's ranking-
stability definitions (raw pairwise-direction table, PDC + coverage per pair, overall
PDC over informative pairs, Kendall's τ/Spearman secondary). This is the module most
worth hand-verifying against toy examples before trusting on real data, given its
history of definitional bugs during design (see protocol document Section 8's
correction trail).

- 🔲 TBD — implementation-only: bootstrap iteration count and seed policy (pick fixed
  values, e.g. 1,000 iterations, fixed seed per experiment, and document them).

### 2.11 Results Storage + App (`results/store.py`, `results_app/`)
Local file/lightweight DB storage (no hosted service — PRD Section 6 explicit
out-of-scope). The app is a thin read layer over stored results: tables, comparison
charts, the ranking-stability visualization (raw pairwise table + PDC/coverage). It is
not a general-purpose dashboard and should not accumulate features beyond what the
paper's Results section needs.

## 3. Suggested tech stack

- **Language:** Python throughout, for consistency with the ML/stats stack.
- **Classical ML (M):** scikit-learn (logistic regression) and/or XGBoost.
- **Sequence model (S):** small GRU/1D-CNN, PyTorch (lightweight enough for 4GB VRAM
  at this feature-vector scale — not a foundation model).
- **L (optional):** local inference via `llama.cpp`/Ollama, contingent on the
  hardware decision (protocol Section 7, item 4 — explicitly not one of the two
  numbered data gates).
- **Stats:** `scipy`/`numpy` for bootstrap and calibration; avoid heavier dependencies
  unless a specific gap appears.
- **Storage:** flat files (Parquet/CSV) or SQLite — no need for a server-based DB at
  this scale.
- **Results app:** a lightweight local web app (e.g. Streamlit) is sufficient; this is
  explicitly not the software's primary contribution (PRD Section 4), so avoid
  over-investing here relative to the pipeline itself.

## 4. Suggested repository layout

```
aire-trace/
├── AIRE-Trace_Frozen_Protocol_and_Plan.md
├── PRD.md
├── AGENTS.md
├── TECHNICAL_DESIGN.md
├── RESEARCH_LOG.md
├── ingestion/
│   ├── tau2.py
│   └── terminalbench.py
├── canonical/
│   ├── schema.py        # Run, Event dataclasses
│   ├── outcome.py        # Rule 10
│   ├── sanitize.py       # Rule 6
│   ├── split.py          # Rule 3
│   ├── prefixes.py       # Rule 1
│   └── features.py       # Rules 2, 9
├── methods/
│   ├── heuristic.py
│   ├── classical_ml.py
│   ├── sequence.py
│   └── llm_monitor.py    # optional
├── evaluation/
│   ├── threshold.py
│   ├── metrics.py
│   ├── cost.py
│   └── stats.py
├── results/
│   └── store.py
├── results_app/
└── experiments/           # see Section 6a for the required per-run record contract
```

## 5. Explicit non-goals (repeated from PRD for implementation-time visibility)

Do not build: a new detector architecture as the headline contribution, foundation-
model training, exact reproductions of PrefixGuard/AgentForesight/Trajectory Guard,
more than 2 datasets or 3 mandatory method families, paid-API dependent components, a
multi-user hosted product.

## 5a. `experiments/` directory contract

Each run gets its own record (subfolder or structured file) containing, at minimum:
dataset + mode (τ²-Bench/Mode B, TerminalBench/Mode A), seed, feature set used, exact
checkpoint policy/horizon K, method (H/M/S/L), threshold target FAR, model
hyperparameters (where applicable), code commit hash, and the output location for that
run's results. This isn't a new requirement — `AGENTS.md`'s reproducibility rule
already requires exact config and code version per run — this section just makes the
`experiments/` directory's job explicit instead of leaving it as an unlabeled folder in
the repo tree.

## 5b. TBD resolution order — Gate 1 before implementation-only parameters

The 🔲 TBDs scattered through this document fall into two categories, and they must be
resolved in order: **Gate 1 scientific/data TBDs first** (actual schemas, outcome
fields, onset semantics, common feature set, split sufficiency, checkpoint horizon),
**then implementation-only TBDs** (ECE bin count, threshold candidate enumeration,
compute-measurement repetitions, bootstrap iterations/seed). This isn't just tidiness —
a Gate 1 finding can change what the sensible implementation-only choice even is (e.g.
the usable episode count directly affects what bootstrap configuration makes sense).
Pinning an implementation-only parameter before its relevant Gate 1 fact is known risks
having to revisit it anyway, or worse, not noticing it should be revisited.

## 6. What "done" means for this document

This document is implementation-ready once every 🔲 TBD above is resolved and moved
into either the protocol document (if it's a scientific decision) or directly into
code + `RESEARCH_LOG.md` (if it's a pinned-but-arbitrary implementation parameter like
bin count or seed). Do not delete the 🔲 markers as they're resolved — change them to
✅ with a one-line pointer to where the resolution lives, so this document keeps
functioning as an honest map of what's real vs. assumed.

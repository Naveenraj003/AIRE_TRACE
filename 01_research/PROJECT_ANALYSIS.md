# AIRE-Trace — Project Analysis

Status: Read-only audit; no code modified.

This document summarizes the repository structure, the role and contents of key files, implementation analysis, protocol compliance checks, tests and results, and recommendations. It aggregates what I inspected programmatically (core docs, preprocessing, evaluation, baselines, validators, and logs) and notes where files are reports/artifacts.

---

## Executive summary

- The repository implements AIRE-Trace: a frozen evaluation protocol and pipeline for prospective agent-failure warning across TerminalBench and τ²-Bench.
- The scientific contract and rules are authoritative in `AIRE-Trace_Frozen_Protocol_and_Plan.md` and enforced through `AGENTS.md` and `PRD.md`.
- Key pipeline components exist and are implemented in `src/`: ingestion/normalization (`preprocessing`), canonical schemas (`src/schemas`), leakage guards (`src/leakage`), prefix generation (`src/preprocessing/prefix_generator.py`), baselines (`src/baselines`), evaluation (`src/evaluation`), statistical/bootstrap and PDC computation (`src/evaluation/*`).
- The project includes a detailed `RESEARCH_LOG.md` documenting Gate checks, dataset inspections, and decisions. Tests under `tests/` exercise preprocessing invariants.
- I did not modify any repository files; this document is an added analysis only.

---

## High-level repo map (major files/folders)

- Root docs and control: `AIRE-Trace_Frozen_Protocol_and_Plan.md`, `PRD.md`, `TECHNICAL_DESIGN.md`, `AGENTS.md`, `RESEARCH_LOG.md`, `AGENTS.md`.
- Preprocessing & ingestion sketches: `dataset_prep.py` (top-level), `src/preprocessing/*` (detailed canonical normalizers, sanitization, terminalbench parser, prefix generator, splitter).
- Canonical schemas: `src/schemas/canonical.py`.
- Leakage checks & validators: `src/leakage/validators.py`.
- Baselines: `src/baselines/{heuristics,logistic,random_forest,sequence,registry}`.
- Evaluation: `src/evaluation/{metrics,thresholding,bootstrap,pdc,statistical_testing,alert_burden,false_alarms,late_detections}`.
- Experiment runners / analysis scripts: `src/run_gate*` and `src/` top-level runners.
- Tests: `tests/preprocessing/*` and other test folders exist.
- Reports and artifacts: `reports/`, `results/`, `archive/` — contain generated JSON/CSV/MD artifacts used as evidence in `RESEARCH_LOG.md`.

---

## Detailed file-level analysis (inspected files)

Note: I inspected the files listed below programmatically and read their contents. For files I did not open, I list their path and inferred role from name only.

### Root files

- `AIRE-Trace_Frozen_Protocol_and_Plan.md`
  - Purpose: authoritative frozen protocol, rules (1–11), dataset roles (Mode A/B), evaluation definitions, gating process.
  - Analysis: Thorough, explicit. Contains design corrections and rule-level invariants that the codebase and tests must enforce (e.g., episode-cluster bootstrap, episode-balanced prefix weighting, calibration procedure). Serves as the single source of truth.

- `PRD.md`
  - Purpose: product requirements built atop the protocol.
  - Analysis: Aligns with protocol; enumerates scope, acceptance criteria, and success criteria. Useful for checklists and test expectations.

- `TECHNICAL_DESIGN.md`
  - Purpose: module contracts and suggested layout.
  - Analysis: Good mapping from protocol to modules. Many items marked 🔲 TBD until Gate 1; implementation mirrors these contracts.

- `RESEARCH_LOG.md`
  - Purpose: append-only log of data-derived decisions and gate evidence.
  - Analysis: Contains dated entries and evidence references showing Gate 1–7 were executed; lists concrete numbers (episode counts, splits, bootstrap config). This file is critical provenance and appears consistent with the code paths.

- `AGENTS.md`
  - Purpose: short enforcement checklist and absolute prohibitions.
  - Analysis: Good guardrails; explicitly prevents silent protocol changes and mandates runtime guards.

- `dataset_prep.py`
  - Purpose: preliminary ingestion and prefix generation sketch; contains key functions `strip_terminal_leakage`, `normalize_tau2_file`, `normalize_terminalbench_row`, `compute_features_up_to`, `generate_prefixes`, and leakage guards.
  - Analysis: Serves as an early single-file sketch. Many caveats documented that field names must be inspected before trusting. Contains runtime assertions (`assert_no_feature_leakage`, `assert_no_split_leakage`) and follows protocol rules in code comments. The feature set and prefix sampling match the project's Category A features. Keep as reference; the production code appears to be in `src/`.

- `requirements.txt`
  - Observation: file read showed non-plain text bytes in the workspace read; it appears to contain package equality pins (e.g., `datasets==5.0.1`) but the file encoding appears to be UTF-16 or have a BOM. Recommendation: open and verify `requirements.txt` encoding and content before automated installs.

### `src/schemas/canonical.py`

- Purpose: `EpisodeRecord`, `EventRecord`, `PrefixRecord` dataclasses (canonical schema).
- Analysis: Clear design. `PrefixRecord.to_dict()` flattens features into `feat_*` keys for storage — consistent with downstream baselines and evaluators that look for `feat_` prefixes. Uses 1-indexed `step_index` and includes onset annotation flags.

### `src/preprocessing/` (inspected)

- `sanitization.py` (strip_terminal_leakage)
  - Purpose: sanitize events to strip outcome-bearing keys and neutralize terminal action types.
  - Analysis: Implements RULE 2 & 6; list of `OUTCOME_LEAK_KEYS` matches protocol. Ensure new outcome-bearing keys in incoming schemas get added to this set (watch evolving dataset schemas).

- `normalizer.py` (tau2 normalizer)
  - Purpose: normalize tau-bench runs into `EpisodeRecord` and `EventRecord` via `normalize_tau2_run`.
  - Analysis: Maps reward => eventual_outcome (0 success/1 failure) and constructs events. Comments note `strip_terminal_leakage` usage. Good defensive coding; many dataset assumptions are documented.

- `terminalbench.py` (Tracebench -> terminalbench normalizer)
  - Purpose: load HuggingFace artifact (zstd tar) and reconstruct chronological steps; map `incorrect_stages` -> annotation-derived onsets.
  - Analysis: Parsing is robust and defensive. It implements logic to map nested `action_ref` JSON to timestamps and canonical indices to produce `annotation_derived_onset_step`. This is nontrivial and seems well-instrumented. Be mindful of HF artifact access: `hf_hub_download(..., local_files_only=True)` requires a local copy or HF CLI cache.

- `prefix_generator.py`
  - Purpose: generate prefixes t = 1..min(T_i, K) and compute Category A features via `compute_category_a_features`.
  - Analysis: Features are consistently computed using only visible events (<= t). The function returns `PrefixRecord` instances including `eventual_outcome`, `onset_annotated`, and `annotation_derived_onset_step`. Matching protocol: no post-terminal padding; horizon default `max_k=30`.

- `splitter.py`
  - Purpose: deterministic task-group-aware split (53/18/18) with seed.
  - Analysis: Enforces task-disjointness with runtime assertions. This implements the `Task-Group Disjoint` split referenced in `RESEARCH_LOG.md`.

### `src/leakage/validators.py`

- Purpose: programmatic leakage checks used pre/post-preprocessing.
- Analysis: Validates forbidden feature keys, task and episode disjointness, horizon constraints, and preservation of unannotated failures. These assertions are aligned with protocol rules and should be executed automatically in preprocessing pipelines.

### `src/baselines/` (inspected)

- `heuristics.py`
  - Purpose: H-family heuristics (simple feature score, CombinedHeuristicMonitor H4 that z-score normalizes TRAIN and maps to sigmoid).
  - Analysis: Deterministic, training-free or minimal fit (z-score on TRAIN). Outputs are probability-like in [0,1]. Good practice: ensure training does not use post-onset prefixes.

- `logistic.py` (M1)
  - Purpose: Logistic regression with `StandardScaler`. Fits on TRAIN only.
  - Analysis: Fits scaler on TRAIN; correct. Uses `feat_` discovery if feature_cols None.

- `random_forest.py` (S1)
  - Purpose: RandomForestClassifier over Category A features.
  - Analysis: Practical, CPU-parallelized (`n_jobs=-1`). Note S-family in TECHNICAL_DESIGN suggested sequence models; the Random Forest is a tree-based tabular baseline labeled `S1` (used as sequence/strong baseline here).

### `src/evaluation/` (inspected)

- `metrics.py`
  - Purpose: compute sample-weighted AUROC/AUPRC/Brier/ECE and produce `compute_all_metrics` results with mode (`prospective` or `raw`).
  - Analysis: Weighting uses `w_{i,t} = 1/min(T_i, K)` per protocol. ECE is computed with weighted averages into uniform bins; default `n_bins=10` present. It calls `compute_episode_far_and_recall` to produce FAR/Recall. The function tags mode-specific outputs correctly.

- `thresholding.py`
  - Purpose: `select_calibration_threshold` that sweeps candidate thresholds and selects the one maximizing calibration-set recall subject to FAR ≤ target (0.05 default). Also `compute_episode_far_and_recall` which implements episode-level aggregation.
  - Analysis: Implementation matches the frozen procedure in Section 8. Candidate thresholds grid is `linspace(0.01,0.99,99)`. Recommendation: freeze and document candidate grid in `RESEARCH_LOG.md` (search_history is returned but primary threshold must be frozen before TEST).

- `bootstrap.py`
  - Purpose: episode-cluster bootstrap resampling to produce mean + 95% CI for metrics.
  - Analysis: Resamples episode integer IDs; recomputes prefix-level weighted AUROC/AUPRC/Brier/ECE on resampled prefix rows. It also resamples episode-level FAR/Recall from pre-aggregated arrays — this is efficient but ensure indexing and alignment is correct for variable episode counts. Default `n_iterations=100` in code, but `RESEARCH_LOG.md` mentions B=100 and later B=1000; the code exposes it as parameter.

- `pdc.py`
  - Purpose: compute pairwise metric comparisons and PDC/coverage across method pairs.
  - Analysis: Implementation follows the paper's rules: ties counted, informative_total computed, 2–2 tie yields 0.50, coverage reported. Note `lower_is_better` list includes `BRIER` (typo: Brier spelled `BRIER` in list) — in `evaluate_pairwise_metric` `lower_is_better = (metric_name.upper() in ["ECE", "BRIER", "FAR"])` — this is a small bug: should be `BRIER` vs `BRIER`? The metric is named `Brier` normally: code checks uppercase "BRIER" which will not match "Brier" and thus will incorrectly treat Brier as higher-is-better. Recommendation: fix metric name variant or accept both spellings. (No code changes requested; just flagging.)

- `bootstrap.py` and `metrics.py` consistency: ensure `compute_weighted_ece` binning matches the binning described in TECHNICAL_DESIGN; code uses `n_bins=10` default — document this choice in `RESEARCH_LOG.md`.

### Tests and verification

- `tests/preprocessing/*` — exist and `RESEARCH_LOG.md` claims `pytest` passing (16/16 earlier, later 38/38). There are tests for terminalbench repair, splitter, schemas, sanitization, leakage guards. The codebase includes guards that raise on protocol violations, and tests assert them.

### Reports & artifacts

- `reports/`, `results/`, `archive/` contain generated run outputs, gate reports, JSON results, and audit documents. `RESEARCH_LOG.md` references many of these artifacts as evidence (e.g. `results/baseline_runs/primary_k30_results.json`). These are generated artifacts, not source code.

---

## Noted issues, risks, and recommendations

- requirements.txt encoding: re-open and normalize to UTF-8 to avoid tooling issues. Running `pip install -r requirements.txt` may fail if file is UTF-16 or contains null bytes.

- `pdc.py` metric name typo: code compares uppercase metric name to `BRIER`. That will not match `Brier` and may lead to incorrect winner orientation. Confirm and normalize metric name keys (prefer uppercase canonicalization map).

- HF artifact access in `src/preprocessing/terminalbench.py` depends on local HF cache. `hf_hub_download(..., local_files_only=True)` will fail unless artifacts have been pre-downloaded. The code is defensive but note for reproducibility: document exact HF commit SHAs and provide instructions to download artifacts (or enable network access before running ingestion).

- `bootstrap.py` default `n_iterations=100` may be low for stable CIs; `RESEARCH_LOG.md` documents B=100 and also B=1000 used for tests. Standardize and freeze `B` (e.g., 1000) and record in `RESEARCH_LOG.md`.

- Ensure `compute_all_metrics(..., mode)` is invoked with correct `mode` per dataset (TerminalBench -> `prospective`, τ²-Bench -> `raw`). The code enforces mode values but callers must be audited.

- `requirements.txt` content should pin versions for core deps used in code (`numpy`, `pandas`, `scikit-learn`, `torch` if used, `huggingface_hub`, `zstandard`, `datasets`, `pyarrow`, `scipy`). Confirm the actual set matches production runs.

- Logging and reproducibility: many scripts rely on seeds; ensure seed is passed and saved in experiment run records (`experiments/` per TECHNICAL_DESIGN). `RESEARCH_LOG.md` indicates seeds used (42) and bootstrap seeds — keep these recorded.

---

## Coverage: what I inspected vs. what remains

- Inspected in detail: protocol docs, PRD, technical design, dataset_prep sketch, all `src/preprocessing/*`, `src/schemas/canonical.py`, `src/leakage/validators.py`, baselines in `src/baselines`, evaluation modules in `src/evaluation` (metrics, thresholding, bootstrap, pdc), and `RESEARCH_LOG.md` and `AGENTS.md`.
- Not exhaustively read: every single artifact under `reports/`, `archive/`, and some support runner scripts in `src/` (many `run_gate*` were not fully opened; they orchestrate experiments). Those are orchestration, not core logic; I can read each if you want per-file detailed notes.

---

## Suggested next steps (if you want me to continue)

- I can (without modifying code):
  - Expand this analysis into per-file verbatim excerpts for every `src/` and `tests/` file (complete top-to-bottom read). This will take more time but is doable.
  - Open and normalize `requirements.txt` to a UTF-8 plain-text listing (no code changes to project logic; just a file content touch — ask before proceeding because you said "don't modify anything").
  - Run the test suite locally and report outputs (requires executing code in the environment; I can only prepare commands unless you permit execution).

---

If you want the analysis to be more fine-grained (one subsection per file with line-level notes), tell me and I'll expand this `PROJECT_ANALYSIS.md` accordingly (I can iterate through every file programmatically and append summaries).

---

## Per-file detailed notes (line-level highlights)

Below are focused, line-level summaries for the repository's core source files I inspected. Each entry highlights the important functions, assumptions, invariants, and any small implementation notes you should watch for when editing or running the pipeline.

- `dataset_prep.py` (top-level sketch)
  - Key functions: `strip_terminal_leakage()` (neutralizes `action_type` and removes outcome keys), `normalize_tau2_file()`, `normalize_terminalbench_row()`, `compute_features_up_to()`, `generate_prefixes()`.
  - Notes: explicitly documents R1–R4 protocol rules in comments. Use `inspect_raw()` before trusting field maps. Leakage-guard functions `assert_no_feature_leakage()` and `assert_no_split_leakage()` raise on violations.

- `src/schemas/canonical.py`
  - Dataclasses: `EpisodeRecord`, `EventRecord`, `PrefixRecord`.
  - `PrefixRecord.to_dict()` flattens `features` into top-level `feat_*` keys for Parquet/CSV export — downstream code depends on this naming.

- `src/preprocessing/sanitization.py`
  - Function: `strip_terminal_leakage(raw_event)` removes keys listed in `OUTCOME_LEAK_KEYS` and converts terminal `action_type` values to neutral `message` content.
  - Implementation detail: update `OUTCOME_LEAK_KEYS` if new dataset fields are discovered during Gate 1 inspections.

- `src/preprocessing/normalizer.py`
  - Function: `normalize_tau2_run(run, idx, filename)` converts a tau-bench run into `EpisodeRecord` and `EventRecord`.
  - Assumption: `reward` field determines `eventual_outcome` (1→success mapped to 0, else 1 for failure). Defensive code calls `strip_terminal_leakage()` on each raw event.

- `src/preprocessing/terminalbench.py`
  - Function: `normalize_tracebench_as_terminalbench(row, commit_sha)` parses HF artifacts (zstd tarball) via `hf_hub_download` and reconstructs events and onset annotations.
  - Line-level note: it maps `incorrect_stages` → `annotation_derived_onset_step` by matching nested `action_ref` JSON to artifact timestamps (nontrivial). Be aware `hf_hub_download(..., local_files_only=True)` requires pre-downloaded artifacts or network access.

- `src/preprocessing/prefix_generator.py`
  - Functions: `compute_category_a_features(visible_events, t)` and `generate_episode_prefixes(episode, events, max_k=30)`.
  - Behavior: strictly uses events with `step_index <= t`. Generates prefixes for `t = 1..min(T_i, K)` with no post-terminal padding. Feature names align with `feat_*` convention.

- `src/preprocessing/splitter.py`
  - Function: `make_task_disjoint_split(tasks, n_train=53, n_calib=18, seed=42)`.
  - Invariant: asserts zero task overlap; used to avoid task leakage across splits.

- `src/leakage/validators.py`
  - Functions: `assert_no_task_leakage`, `assert_no_episode_leakage`, `assert_no_feature_leakage`, `assert_valid_checkpoint_horizon`, `assert_unannotated_failures_preserved`.
  - Note: these raise on protocol violations and should be executed as part of preprocessing; they check `feat_` keys or `features` map for forbidden outcome fields.

- `src/baselines/heuristics.py`
  - Classes: `HeuristicMonitor` (simple scaled single-feature score), `CombinedHeuristicMonitor` (`H4` — z-score normalization on TRAIN then sigmoid mapping).
  - Implementation note: `CombinedHeuristicMonitor.fit()` computes means/stds on TRAIN only — keep this entry point free of post-onset prefixes.

- `src/baselines/logistic.py`
  - Class: `LogisticBaseline` (scaler + sklearn LogisticRegression). `fit()` calls `scaler.fit_transform()` on TRAIN, `predict_proba()` uses the saved scaler.

- `src/baselines/random_forest.py`
  - Class: `RandomForestBaseline` with `n_jobs=-1`. `predict_proba()` returns clipped probabilities for class 1.

- `src/evaluation/metrics.py`
  - Functions: `compute_sample_weights()`, `compute_weighted_auroc()`, `compute_weighted_auprc()`, `compute_weighted_brier()`, `compute_weighted_ece()`, and `compute_all_metrics()`.
  - Note: sample weights use `1 / min(T_i, K)` episode-balanced weighting. `compute_all_metrics()` enforces `mode in {"prospective","raw"}` and only returns `Recall_at_FAR` under `prospective` mode.

- `src/evaluation/thresholding.py`
  - Functions: `compute_episode_far_and_recall()` and `select_calibration_threshold()`.
  - Behavior: candidate thresholds are `np.linspace(0.01, 0.99, 99)`; selection maximizes calibration recall subject to `FAR <= target_far` (default 0.05). Returned structure includes `search_history` for auditability.

- `src/evaluation/bootstrap.py`
  - Function: `compute_episode_bootstrap_ci(df_prefixes, y_prob, threshold, n_iterations=100, ...)`.
  - Behavior: resamples episode integer IDs, recomputes prefix-level weighted metrics, and resamples episode-level FAR/Recall from pre-aggregated arrays. Note default `n_iterations=100` is configurable and `RESEARCH_LOG.md` documents higher values used in experiments.

- `src/evaluation/pdc.py`
  - Functions: `evaluate_pairwise_metric()`, `compute_pdc_between_methods()`, `compute_overall_pdc()`.
  - Small bug to watch: code treats lower-is-better metric names by checking uppercase names against `"ECE", "BRIER", "FAR"`. The `Brier` metric (typical capitalization) will not match `BRIER` — normalize metric keys before comparison to avoid orientation errors.

- `src/preprocessing/run_pipeline.py` (driver)
  - Master pipeline `main()` loads `configs/data.yaml`, ingests TerminalBench and tau-bench, runs `make_task_disjoint_split()`, generates prefixes via `generate_episode_prefixes()`, runs all leakage validators, and writes Parquet manifests to `manifest_dir`. See file for per-stage export paths and manifest meta.

- `src/run_gate3_experiments.py` (baseline runner)
  - Master experiment `main()` loads Parquet manifests from `data/processed/manifests`, constructs `MasterEvaluator` with `target_far=0.05`, runs the primary experiment (`K=30`) and sensitivity runs, writes results JSON/CSV, and generates a Gate-3 report. It calls `evaluator.run_evaluation(...)` which orchestrates model training, calibration, and evaluation.

If you want explicit line-by-line commentary (e.g. "lines 1–40: imports; lines 41–120: function X; lines 121–200: error handling"), I can produce that for every file in the `src/` tree — tell me whether you prefer that exact format and I'll append it file-by-file.

---

## What this project is — short description with a real example

What it is:

- AIRE-Trace is a reproducible evaluation harness implementing a frozen, leakage-safe protocol for prospective early-warning monitoring of agent failures. It standardizes dataset ingestion, sanitization (no outcome leakage), episode/task splitting, prefix generation, train/calib/test separation, threshold calibration at a controlled FAR, and episode-cluster bootstrap statistical reporting.

Real example (conceptual):

- Input: TerminalBench HuggingFace dataset (task traces with `incorrect_stages`) and a local copy of `tau-bench` historical JSONs.
- Run: preprocess both sources to canonical Parquet manifests, train simple baselines (heuristic, logistic, random forest), calibrate thresholds on calibration episodes to achieve FAR ≤ 5%, evaluate on TerminalBench TEST (Mode A prospective metrics) and apply frozen thresholds to τ²-Bench (Mode B diagnostic metrics), then compute PDC ranking stability across AUROC/AUPRC/Recall@FAR/ECE.
- Output: Parquet manifests, JSON results (`primary_k30_results.json`), CSV comparison table, PDC summary, and Gate reports in `reports/`.

Example of the pipeline flow (commands you can run locally on the project machine):

1. Ensure prerequisites: Python environment with required packages (see `requirements.txt`). If `requirements.txt` encoding is non-UTF-8, open and inspect it first.

2. Preprocess datasets (Gate 2 preprocessing):

```powershell
python -m src.preprocessing.run_pipeline
```

Notes: this reads `configs/data.yaml` (path: `p:\AIRE-TRACE\configs\data.yaml`) and expects TerminalBench accessible via the HuggingFace cache and tau-bench files in `p:\AIRE-TRACE\data\tau-bench\historical_trajectories`.

3. Run Gate 3 baselines and evaluation (train, calibrate, evaluate):

```powershell
python -m src.run_gate3_experiments
```

Notes: this script reads manifests from `data/processed/manifests` (the locations written by the preprocessing run) and writes results to `results/baseline_runs` and `reports/`.

4. Review outputs (examples):

```powershell
type results\baseline_runs\primary_k30_results.json
type reports\gate3_baseline_protocol.md
```

Minimal end-to-end example (what you should see):

- `preprocessing` writes `terminalbench_prefixes.parquet` and `tau2_prefixes.parquet` to the configured `manifest_dir`.
- `run_gate3_experiments` reads those manifests, fits models, calibrates thresholds, and writes `primary_k30_results.json`, `calibrated_thresholds.json`, `pdc_summary.json`, and `baseline_comparison_table.csv` to `results/baseline_runs/`.

---

If you'd like, I will now (choose one):

- produce full line-by-line commentary for every file under `src/` and `tests/` (big append; will take measurable time), or
- iterate through the `src/` tree and create per-file short sections (1–4 key line-level notes each) for every file and append them to this document.

Tell me which of the two you prefer and I'll continue; I can finish the selected expansion and then mark the TODOs complete.

---

## End-to-End Current Project Status (As of September 2026)

### 1. Empirical Population Reconstruction & Lineage
- **Raw declared Tracebench rows:** 3,316.
- **Structural exclusions:** 2,655 structurally invalid (empty/aborted traces with no actionable steps) + 25 missing artifact paths.
- **Canonical study episodes:** Exactly 636 episodes deterministically reconstructed (`post_recovery_audit.txt`, `lineage_verification.txt`).
- **Task-disjoint splits:** TRAIN = 163 (53 tasks), CALIBRATION = 57 (18 tasks), TEST = 416 (18 tasks).
- **TEST episode breakdown:** 317 failures, 99 successes; 257 valid annotated failures, 60 unannotated failures.

### 2. Standardized Baseline Evaluation & Metric Ranking (Mode A, K=30)
- **Evaluated models:** Heuristic monitors ($H1-H4$), Logistic Regression ($M1$), Random Forest ($S1$), GRU ($S2$). Model $L$ marked pending.
- **Operating threshold policy:** Calibrated on CALIBRATION under $\text{FAR} \le 5\%$ budget and frozen before scoring TEST episodes.
- **Observed AUROC:** $H1=0.6205$, $H2=0.5752$, $H3=0.5074$, $H4=0.6135$, $M1=0.6215$, $S1=0.6371$, $S2=0.5496$.
- **Pairwise Direction Consistency (PDC):** $\text{PDC} = 0.8294$ with coverage $0.881$ across 21 informative pairs.
- **Key finding:** Prospective recall collapses under strict operational false-alarm constraints ($\text{Recall} \approx 0$ at $\text{FAR} \le 5\%$, rising to $0.0973$ at $\text{FAR} = 10\%$).

### 3. Operational Analysis (Gate 6) & Component Ablation (Gate 7)
- **Gate 6 operational audit:** Model $H3$ produced severe alerting burden (8,012 alerts, mean 19.26/ep, $\text{FAR} = 1.0000$), while $S1$ maintained controlled burden (25 alerts, mean 0.060/ep, $\text{FAR} = 0.0404$). Late alerts ($t > t_{\text{onset}}$) strictly quarantined.
- **Gate 7 feature ablation:** Condition $A4$ (removing `tool_error_count` and `retry_count`) produced the single largest observed degradation ($\Delta \text{AUROC} = -0.1069$), demonstrating strong association between error/retry signals and discrimination capability.

### 4. Canonical Paired Bootstrap Significance Testing (Milestones 1–5)
- **Tooling amendment:** `src/evaluation/statistical_testing.py::compute_paired_bootstrap_test` extended with native joint episode-cluster resampling for `Recall_at_FAR` under frozen thresholds.
- **Primary TEST population ($N=416$, $B=10,000$):**
  - Observed difference ($\text{dyn\_comp} - M1$): $+0.1089$
  - Bootstrap mean difference: $+0.1091$
  - 95% Confidence Interval: $[0.0706, 0.1496]$
  - Adjusted p-value: $p_{\text{adj}} = 9.999 \times 10^{-5}$ ($p < 0.0001$)
  - Result: **Statistically Significant** superiority over M1 on full TEST.
- **Secondary supported population ($N=217$):** $\Delta = 0.0000$, $p_{\text{adj}} = 1.0000$ (Non-significant).

### 5. Indian Patent Office Application Package (CRI Guidelines 2025)
- **Subject:** "System and Method for Prospective Failure Warning in Autonomous Agents Using Trajectory Risk Decomposition"
- **Statutory Forms & Complete Specification:**
  - Form 1 & Form 5 drafted in `docs/AIRE-Trace_Indian_Patent_Forms_1_and_5.md`.
  - Form 2 Complete Specification in `patent_docs/Form 2 (3).docx` and `docs/` containing 10 statutory claims (System Claim 1, Method Claim 6, Computer-Readable Medium Claim 10).
  - 4 Statutory Drawing Sheets in `patent_docs/IPR Drawings Template(n).docx` strictly adhering to Rule 15 margins (top/left 40mm, bottom/right 30mm) with Figures 1–4 from `figures/patent/`.
  - Prior-art claim-element chart completed in `AIRE-Trace — Prior-Art Claim-Element Chart.md`.
  - Passed comprehensive automated compliance audit (`audit_all.py`).

### 6. IEEE Conference Publication Package & Document Assets
- **Scientific manuscript:** `AIRE-Trace_Master_IEEE_Manuscript.md` (fully frozen).
- **Bibliographic references:** 13/13 independently verified against authoritative academic sources (`AIRE-Trace_Verified_References.md`).
- **Publication figures:** 6 canonical figures generated in `figures/ieee/` (Figures 1–6).
- **Universal Master files:** `AIRE-Trace_Universal_IEEE_Conference_Master.tex`, `.docx`, `.pdf` verified by `validate_universal_ieee_master.py`.
- **IEEE LaTeX package:** `AIRE-Trace_IEEE/main.tex` and compiled `AIRE-Trace_IEEE.pdf` adhering to two-column `IEEEtran.cls`.
- **IEEE Word Document (.docx):** Generation and formatting aligned with `Conference-LaTeX-template_10-17-19` with author block placeholders strictly preserved.


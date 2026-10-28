# Gate 3.4 Decision Log Audit

**Date:** 2026-08-04  
**Auditor Role:** Independent Auditor  
**Audit Scope:** Cross-verification of every major gate decision against
`RESEARCH_LOG.md`, `docs/DECISION_LOG.md`, `docs/PROJECT_CONTROL.md`, and
`docs/ROADMAP.md`.  
**Method:** Read-only. No source documents were modified. No history was
invented. Every finding is sourced from the actual file content read during
this audit.

---

## 0. Document Inventory

| Document | Path | Status |
|---|---|---|
| `RESEARCH_LOG.md` | `p:\AIRE-TRACE\RESEARCH_LOG.md` | EXISTS — 141 lines |
| `DECISION_LOG.md` | `p:\AIRE-TRACE\docs\DECISION_LOG.md` | EXISTS — 95 lines |
| `PROJECT_CONTROL.md` | `p:\AIRE-TRACE\docs\PROJECT_CONTROL.md` | EXISTS — 96 lines |
| `ROADMAP.md` | `p:\AIRE-TRACE\docs\ROADMAP.md` | EXISTS — 50 lines |
| `DECISION_LOG.md` (root) | `p:\AIRE-TRACE\DECISION_LOG.md` | **DOES NOT EXIST** |
| `PROJECT_CONTROL.md` (root) | `p:\AIRE-TRACE\PROJECT_CONTROL.md` | **DOES NOT EXIST** |
| `ROADMAP.md` (root) | `p:\AIRE-TRACE\ROADMAP.md` | **DOES NOT EXIST** |

> [!NOTE]
> `DECISION_LOG.md`, `PROJECT_CONTROL.md`, and `ROADMAP.md` are located in
> `docs/` — not the project root. `AGENTS.md` Section 5's file map does not
> list these files at all. No reference to `docs/` exists in `AGENTS.md`'s
> file map. This is an undocumented location.

---

## 1. Gate-by-Gate Audit

---

### Gate 1 — Dataset Forensics (2026-07-31)

#### 1.1 RESEARCH_LOG.md entry

| Field | Value | Present? |
|---|---|---|
| **Date** | 2026-07-31 | ✅ |
| **Title** | "Gate 1 Forensic Dataset Inspection & Evidence Package" | ✅ |
| **Question** | Verify actual dataset schemas, episode counts, class balance, trajectory length distributions, onset semantics, feature overlap, and split viability | ✅ |
| **Finding** | 6 numbered findings (TerminalBench counts, Tracebench onset, τ²-Bench, horizon truncation, feature overlap, canonical mapping) | ✅ |
| **Decision** | Not present as an explicit `**Decision:**` field — entry ends at Finding 6 with no Decision or Evidence lines | ❌ MISSING |
| **Evidence** | Not present as an explicit `**Evidence:**` field | ❌ MISSING |
| **Files changed** | Not recorded anywhere in the entry | ❌ MISSING |
| **Result / outcome** | Implicit in findings but no explicit pass/fail verdict line | ⚠️ IMPLICIT ONLY |

> [!WARNING]
> The Gate 1 RESEARCH_LOG entry omits the `**Decision:**` and `**Evidence:**`
> fields defined in the log's own entry format template (lines 12–17 of
> `RESEARCH_LOG.md`). The entry describes findings but does not formally state
> what was decided or what artifact proves it.

#### 1.2 DECISION_LOG.md entries (related to Gate 1)

| Entry | Status | Notes |
|---|---|---|
| `[VERIFIED] TerminalBench Episode Sufficiency & Task-Cluster Splitting` | ✅ Present | Evidence: `reports/gate1_dataset_inventory.md` — **this report filename does not exist**; actual file is `reports/gate1_dataset_inventory.json` and `reports/gate1_report.md` |
| `[VERIFIED] Task-Group Disjoint Splitting & Task Generalization Claim` | ✅ Present | Evidence: `reports/gate1_5_split_analysis.json`, `reports/gate1_5_methodological_validation.md` — `gate1_5_methodological_validation.md` does not exist as a standalone file; it was consolidated into `gate1_5_report.md` |

#### 1.3 ROADMAP.md entry

| Field | Value | Present? |
|---|---|---|
| **Date** | Not recorded | ❌ MISSING |
| **Reason** | Implicit ("performed dataset forensics") | ⚠️ IMPLICIT |
| **Impact** | Not stated | ❌ MISSING |
| **Files changed** | Not listed | ❌ MISSING |
| **Result** | "COMPLETE (Evidence package generated in `reports/`)" | ✅ |

#### 1.4 PROJECT_CONTROL.md

- Section 9 (Dataset Status): Records dataset statistics, status = "VERIFIED (Gate 1 dataset inspection complete)" ✅
- Section 21 (Implementation Status): Still reads "BLOCKED pending Gate 1 approval." ❌ STALE

---

### Gate 1.5 — Methodological Validation (2026-07-31)

#### 1.5.1 RESEARCH_LOG.md entry

| Field | Value | Present? |
|---|---|---|
| **Date** | 2026-07-31 | ✅ |
| **Title** | "Gate 1.5 Targeted Methodological Validation Evidence" | ✅ |
| **Question** | Five methodological questions: Task Generalization, Warning Opportunity, Failure-Onset Semantics, Feature Novelty, Dataset Provenance | ✅ |
| **Finding** | 5 numbered findings | ✅ |
| **Decision** | Not present — entry ends after Finding 5 | ❌ MISSING |
| **Evidence** | Not present | ❌ MISSING |
| **Files changed** | Not recorded | ❌ MISSING |
| **Result / outcome** | Implicit in findings | ⚠️ IMPLICIT ONLY |

#### 1.5.2 DECISION_LOG.md entries (related to Gate 1.5)

| Entry | Status | Notes |
|---|---|---|
| `[FROZEN] Episode-Adaptive Checkpoint Formulation` | ✅ Present | Evidence: `reports/gate1_5_warning_opportunity_analysis.md` — **this file does not exist**; consolidated into `gate1_5_report.md` |
| `[FROZEN] Failure-Onset Semantics & Unannotated Failures` | ✅ Present | Evidence: `reports/gate1_5_onset_semantics.md` — **this file does not exist**; consolidated into `gate1_5_report.md` |
| `[FROZEN] Task-Group Disjoint Splitting & Task Generalization Claim` | ✅ Present | See Gate 1 row above |

> [!WARNING]
> Multiple DECISION_LOG entries reference evidence files that no longer exist
> as standalone files (`gate1_dataset_inventory.md`,
> `gate1_5_methodological_validation.md`, `gate1_5_warning_opportunity_analysis.md`,
> `gate1_5_onset_semantics.md`). These were consolidated into
> `gate1_report.md` and `gate1_5_report.md` during repository cleanup. The
> evidence links are broken. The corresponding
> `reports/repository_cleanup_report.md` entry notes that "20 smaller gate
> reports" were consolidated, but the DECISION_LOG was never updated to point
> to the surviving consolidated files.

#### 1.5.3 ROADMAP.md

Gate 1.5 is **not listed** as a separate gate in `ROADMAP.md`. It is implicitly
subsumed into Gate 1's single entry. No date, impact, or files-changed record
exists for Gate 1.5 in ROADMAP.

---

### Gate 2 — Trace Preprocessing and Labeling (2026-07-31)

#### 2.1 RESEARCH_LOG.md entry

| Field | Value | Present? |
|---|---|---|
| **Date** | 2026-07-31 | ✅ |
| **Title** | "Gate 2 Trace Preprocessing and Labeling Pipeline Execution" | ✅ |
| **Question** | Execute canonical trace preprocessing, task-group splitting, sanitization, prefix generation, and programmatic leakage verification | ✅ |
| **Finding** | 5 numbered findings (provenance, split, prefixes, onset, leakage) | ✅ |
| **Decision** | Not present as explicit field | ❌ MISSING |
| **Evidence** | Not present as explicit field | ❌ MISSING |
| **Files changed** | Not recorded | ❌ MISSING |
| **Result** | Findings describe passing result but no explicit verdict | ⚠️ IMPLICIT ONLY |

#### 2.2 DECISION_LOG.md entries (Gate 2)

| Entry | Status | Notes |
|---|---|---|
| `[FROZEN] Canonical Preprocessing Pipeline & Parquet Manifests` | ✅ Present | Evidence: `reports/gate2_preprocessing_report.md` — **this file does not exist** standalone; consolidated into `gate2_report.md`. Evidence also cites `reports/gate2_validation_report.json` — ✅ EXISTS |

#### 2.3 ROADMAP.md

| Field | Value | Present? |
|---|---|---|
| **Date** | Not recorded | ❌ MISSING |
| **Reason** | Implicit | ⚠️ IMPLICIT |
| **Impact** | Not stated | ❌ MISSING |
| **Files changed** | Not listed | ❌ MISSING |
| **Result** | "COMPLETE" | ✅ |

> [!WARNING]
> The split counts in `RESEARCH_LOG.md` (Gate 2 entry, line 62) report
> `TRAIN=31,035 / CALIB=10,521 / TEST=10,548`, which differ from the
> canonical manifest values `TRAIN=31,016 / CALIB=10,516 / TEST=10,572`
> established in Gate 3.3. The RESEARCH_LOG.md Gate 2 entry was never
> corrected. Per `AGENTS.md` Section 2, the paper's Methodology section
> should be written from this log. These stale figures are a paper-writing
> risk (Finding F-1 from `gate3_4_repository_audit.md`).

---

### Gate 2.1 — Pre-Baseline Audit (2026-07-31)

#### 2.1.1 RESEARCH_LOG.md entry

| Field | Value | Present? |
|---|---|---|
| **Date** | 2026-07-31 | ✅ |
| **Title** | "Gate 2.1 Pre-Baseline Audit Findings" | ✅ |
| **Question** | 6-area audit: Feature Drift, Episode Weighting, Retry Semantics, Test Coverage, Manifest Integrity, Split Reproducibility | ✅ |
| **Finding** | 6 numbered findings | ✅ |
| **Decision** | Not present as explicit field | ❌ MISSING |
| **Evidence** | Not present as explicit field | ❌ MISSING |
| **Files changed** | Not recorded | ❌ MISSING |
| **Result** | Implicit | ⚠️ IMPLICIT ONLY |

#### 2.1.2 DECISION_LOG.md entries (Gate 2.1)

| Entry | Status | Notes |
|---|---|---|
| `[VERIFIED] Pre-Baseline Implementation & Manifest Audit` | ✅ Present | Evidence cites 4 sub-reports (`gate2_1_episode_weighting_audit.md`, etc.) — all **do not exist standalone**; consolidated into `gate2_1_report.md` |

#### 2.1.3 ROADMAP.md

Gate 2.1 is **not listed** as a separate gate in `ROADMAP.md`. It is entirely
absent. No date, reason, impact, or result is recorded.

---

### Gate 3 — Baseline Implementation (2026-07-31)

#### 3.1 RESEARCH_LOG.md entry

| Field | Value | Present? |
|---|---|---|
| **Date** | 2026-07-31 | ✅ |
| **Title** | "Gate 3 Baseline Implementation and Evaluation Execution" | ✅ |
| **Question** | Implement baseline ladder, calibrate thresholds, evaluate under frozen protocol | ✅ |
| **Finding** | 5 numbered findings | ✅ |
| **Decision** | ✅ Present ("Gate 3 complete. Baseline models and evaluation framework implemented...") | ✅ |
| **Evidence** | ✅ Present (lists 5 artifact paths) | ✅ |
| **Files changed** | `src/baselines/`, `src/evaluation/`, `results/baseline_runs/`, `reports/gate3_baseline_protocol.md` — **`gate3_baseline_protocol.md` does not exist**; consolidated into `gate3_report.md` | ⚠️ STALE PATHS |
| **Result** | "Gate 3 complete" | ✅ |

> [!CAUTION]
> The metric figures in the RESEARCH_LOG Gate 3 entry (`RESEARCH_LOG.md`
> lines 81–85) are the pre-reconciliation prose template values, **not** the
> true executed numbers. The stale figures are:
>
> | Metric | Stale Value (in log) | Canonical Value (from JSON) |
> |---|---|---|
> | S1 AUROC | 0.7635 | **0.6016** |
> | M1 AUROC | 0.7412 | **0.5877** |
> | H4 AUROC | 0.6891 | **0.5253** |
> | PDC | 1.0000 | **0.7667** |
> | S1 τ² AUROC | 0.6821 | **0.5199** |
>
> Gates 3.1–3.3 reconciled these figures in their own reports and in
> DECISION_LOG.md, but the Gate 3 RESEARCH_LOG entry itself was **never
> corrected**. This is Finding F-3 from `gate3_4_repository_audit.md`.
> Per AGENTS.md the paper methodology should be written from RESEARCH_LOG —
> this is a direct paper-writing risk.

#### 3.2 DECISION_LOG.md entries (Gate 3)

| Entry | Status | Notes |
|---|---|---|
| `[FROZEN] Baseline Model Ladder & Calibrated Thresholds` | ✅ Present | Metric values are stale (0.7635 / 0.4128) — Finding F-4 from repository audit |
| Evidence | `reports/gate3_baseline_protocol.md` | **File does not exist**; consolidated into `gate3_report.md` |

#### 3.3 ROADMAP.md

| Field | Value | Present? |
|---|---|---|
| **Date** | Not recorded | ❌ MISSING |
| **Reason** | Implicit | ⚠️ IMPLICIT |
| **Impact** | Not stated | ❌ MISSING |
| **Files changed** | Not listed | ❌ MISSING |
| **Result** | "COMPLETE — CANONICAL BASELINE EVIDENCE FROZEN" | ✅ |

---

### Gate 3.1 — Baseline Result Integrity Audit (2026-07-31)

#### 3.1.1 RESEARCH_LOG.md entry

| Field | Value | Present? |
|---|---|---|
| **Date** | 2026-07-31 | ✅ |
| **Title** | "Gate 3.1 Baseline Result Integrity Audit Findings" | ✅ |
| **Question** | 10-area audit: Prefix Reconciliation, Episode Reconciliation, Threshold Semantics, Metric Weighting, Brier/ECE, PDC Reconstruction, Bootstrap Mechanics, Test Contamination, Score Direction, Sensitivity Reproduction | ✅ |
| **Finding** | 7 numbered findings | ✅ |
| **Decision** | ✅ Present ("Gate 3.1 complete. Five audit reports generated...") | ✅ |
| **Evidence** | ✅ Present (lists 5 artifact paths) | ✅ |
| **Files changed** | Audit report paths listed — all 5 referenced sub-reports (`gate3_1_prefix_reconciliation.md` etc.) **do not exist standalone**; consolidated into `gate3_1_report.md` | ⚠️ STALE PATHS |
| **Result** | "All results verified 100% compliant with frozen contract" | ✅ |

> [!WARNING]
> The RESEARCH_LOG entry for Gate 3.1 states PDC = **0.7667** and B=**100**
> (lines 96–97), which are correct per executed artifacts. However, the
> entry also cites 5 sub-report files that no longer exist as standalone
> documents. The evidence trail is partially broken.

#### 3.1.2 DECISION_LOG.md entries (Gate 3.1)

| Entry | Status | Notes |
|---|---|---|
| `[VERIFIED] Baseline Result Integrity Audit` | ✅ Present | Decision text matches RESEARCH_LOG. Evidence cites 5 sub-reports that no longer exist standalone. |

#### 3.1.3 ROADMAP.md

Gate 3.1 is folded into the Gate 3 entry (not a separate roadmap item). No
date, impact, or files-changed is recorded for Gate 3.1 specifically.

---

### Gate 3.2 — Critical Result Reconciliation (2026-07-31)

#### 3.2.1 RESEARCH_LOG.md entry

| Field | Value | Present? |
|---|---|---|
| **Date** | 2026-07-31 | ✅ |
| **Title** | "Gate 3.2 Critical Result Reconciliation Findings" | ✅ |
| **Question** | Forensic reconciliation of raw vs manifest episode counts, prefix counts, recall semantics, bootstrap counts, PDC | ✅ |
| **Finding** | 5 numbered findings | ✅ |
| **Decision** | ✅ Present ("Gate 3.2 complete...") | ✅ |
| **Evidence** | ✅ Present (`reports/gate3_2_reconciliation.md`) — file EXISTS | ✅ |
| **Files changed** | Not explicitly listed | ❌ MISSING |
| **Result** | "All discrepancies fully reconciled" | ✅ |

> [!NOTE]
> Gate 3.2's RESEARCH_LOG entry records the failed/success breakdown as
> 3,936/3,137 (RESEARCH_LOG line 105), consistent with `gate3_2_reconciliation.md`
> line 30. However, Gate 3.1's report records 4,270/2,803. Both sum to
> 7,073. This internal contradiction (Finding F-2 in the repository audit)
> is not noted or resolved anywhere in RESEARCH_LOG or DECISION_LOG.

#### 3.2.2 DECISION_LOG.md entries (Gate 3.2)

| Entry | Status | Notes |
|---|---|---|
| `[VERIFIED] Critical Result Reconciliation (Gate 3.2)` | ✅ Present | Decision and evidence are correct. `reports/gate3_2_reconciliation.md` exists. ✅ |

#### 3.2.3 ROADMAP.md

Gate 3.2 is folded into the Gate 3 entry. Not separately listed. No date,
impact, or files-changed recorded.

---

### Gate 3.3 — Final Baseline Result Lineage Reconciliation (2026-07-31)

#### 3.3.1 RESEARCH_LOG.md entry

| Field | Value | Present? |
|---|---|---|
| **Date** | 2026-07-31 | ✅ |
| **Title** | "Gate 3.3 Final Baseline Result Lineage Reconciliation Findings" | ✅ |
| **Question** | Definitive forensic lineage audit reconciling metric discrepancies, raw split counts, actionable population, artifact consistency, PDC, bootstrap | ✅ |
| **Finding** | 4 numbered findings (including canonical metric values and split sums) | ✅ |
| **Decision** | ✅ Present ("Gate 3.3 complete...") | ✅ |
| **Evidence** | ✅ Present (`reports/gate3_3_result_lineage.md`, 3 JSON/CSV artifacts) — all exist | ✅ |
| **Files changed** | Not explicitly listed | ❌ MISSING |
| **Result** | "All baseline result lineages fully reconciled" | ✅ |

#### 3.3.2 DECISION_LOG.md entries (Gate 3.3)

| Entry | Status | Notes |
|---|---|---|
| `[VERIFIED & FROZEN] Final Baseline Result Lineage Reconciliation (Gate 3.3)` | ✅ Present | Decision text and evidence correct and complete. Most complete entry in the log. ✅ |

#### 3.3.3 PROJECT_CONTROL.md

- Section 16 (Current Gate): Records "GATE 3.3 — Final Baseline Result Lineage
Reconciliation (Complete...)" with the correct canonical metric values
($S1=0.6016$, $M1=0.5877$, PDC=0.7667). ✅
- Section 21 (Implementation Status): Still reads "BLOCKED pending Gate 1 approval." ❌ STALE
- Section 22 (Experiment Status): Still reads "Not started." ❌ STALE

#### 3.3.4 ROADMAP.md

Gate 3.3 is folded into Gate 3's single roadmap entry. Not separately listed
with date, reason, impact, or files-changed.

---

## 2. Gate 0 (Artifact Understanding) Audit

`ROADMAP.md` lists a `[x] GATE 0 — Artifact understanding` entry with status
PASS. However:

- There is **no corresponding entry in RESEARCH_LOG.md** for Gate 0.
- There is **no corresponding entry in DECISION_LOG.md** for Gate 0.
- `PROJECT_CONTROL.md` Section 24 (Change Log) has a single entry:
  "[2026-07-31] Initialized PROJECT_CONTROL.md from research artifacts" —
  this may implicitly refer to Gate 0 but is not labeled as such.

> [!WARNING]
> Gate 0 has no formal log record in either RESEARCH_LOG.md or DECISION_LOG.md.
> Only ROADMAP.md acknowledges it.

---

## 3. Repository Cleanup Decision Audit

A "Repository Cleanup and Report Consolidation" decision entry appears in
RESEARCH_LOG.md (2026-07-31, lines 113–121). This event consolidated 20
smaller gate sub-reports into 7 primary gate documents.

| Field | Present? |
|---|---|
| Date | ✅ |
| Question | ✅ |
| Finding | ✅ |
| Decision | ✅ |
| Evidence | ✅ (`reports/repository_cleanup_report.md` — exists) |
| Files changed | ✅ (names the 7 surviving reports) |
| Result | ✅ (pytest 16/16 passed) |

> [!IMPORTANT]
> This cleanup event is **the root cause of multiple broken evidence links**
> across DECISION_LOG.md. After consolidation, no sweep was performed to
> update DECISION_LOG evidence paths from the deleted sub-report filenames
> to the surviving consolidated filenames. Every DECISION_LOG entry that
> cites a sub-report that was deleted in the cleanup now has a broken
> evidence link.

---

## 4. Summary: Required Fields per Gate

The RESEARCH_LOG entry format requires: `**Question:**`, `**Finding:**`,
`**Decision:**`, `**Evidence:**`. The following table shows which gates
satisfy the full format:

| Gate | Question | Finding | Decision | Evidence |
|---|---|---|---|---|
| Gate 0 | — | — | — | — |
| Gate 1 | ✅ | ✅ | ❌ | ❌ |
| Gate 1.5 | ✅ | ✅ | ❌ | ❌ |
| Gate 2 | ✅ | ✅ | ❌ | ❌ |
| Gate 2.1 | ✅ | ✅ | ❌ | ❌ |
| Gate 3 | ✅ | ✅ | ✅ | ✅ |
| Gate 3.1 | ✅ | ✅ | ✅ | ✅ |
| Gate 3.2 | ✅ | ✅ | ✅ | ✅ |
| Gate 3.3 | ✅ | ✅ | ✅ | ✅ |
| Repository Cleanup | ✅ | ✅ | ✅ | ✅ |

Gates 1 through 2.1 are missing `**Decision:**` and `**Evidence:**` fields
in RESEARCH_LOG despite the full format being defined in the log's own header.
Gates 3 through 3.3 comply with the full format.

---

## 5. Summary: ROADMAP.md Coverage of Gates

| Gate | In ROADMAP | Separate entry | Date recorded | Reason | Impact | Files changed | Result |
|---|---|---|---|---|---|---|---|
| Gate 0 | ✅ | ✅ | ❌ | ⚠️ implicit | ❌ | ❌ | ✅ |
| Gate 1 | ✅ | ✅ | ❌ | ⚠️ implicit | ❌ | ❌ | ✅ |
| Gate 1.5 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Gate 2 | ✅ | ✅ | ❌ | ⚠️ implicit | ❌ | ❌ | ✅ |
| Gate 2.1 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Gate 3 | ✅ (covers 3–3.3) | ✅ | ❌ | ⚠️ implicit | ❌ | ❌ | ✅ |
| Gate 3.1 | ⚠️ folded | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Gate 3.2 | ⚠️ folded | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Gate 3.3 | ⚠️ folded | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

No ROADMAP.md entry records a date, reason, impact, or list of files changed.
ROADMAP is a status tracker, not an audit trail.

---

## 6. Summary: DECISION_LOG.md Coverage of Gates

| Gate | Covered by entry? | Entry status label | Evidence links valid? |
|---|---|---|---|
| Gate 0 | ❌ | — | — |
| Gate 1 | ✅ (2 entries) | [VERIFIED] | ⚠️ Partially broken (`gate1_dataset_inventory.md` → non-existent) |
| Gate 1.5 | ✅ (3 entries) | [FROZEN] | ⚠️ Broken (`gate1_5_methodological_validation.md`, `gate1_5_warning_opportunity_analysis.md`, `gate1_5_onset_semantics.md` → non-existent) |
| Gate 2 | ✅ (1 entry) | [FROZEN] | ⚠️ Partially broken (`gate2_preprocessing_report.md` → non-existent) |
| Gate 2.1 | ✅ (1 entry) | [VERIFIED] | ❌ All 4 sub-report evidence files non-existent |
| Gate 3 | ✅ (1 entry) | [FROZEN] | ⚠️ `gate3_baseline_protocol.md` non-existent; stale metrics |
| Gate 3.1 | ✅ (1 entry) | [VERIFIED] | ⚠️ All 5 sub-report evidence files non-existent |
| Gate 3.2 | ✅ (1 entry) | [VERIFIED] | ✅ `gate3_2_reconciliation.md` exists |
| Gate 3.3 | ✅ (1 entry) | [VERIFIED & FROZEN] | ✅ All evidence files exist |

---

## 7. Consolidated Finding List

| ID | Severity | Category | Document | Description |
|---|---|---|---|---|
| A-1 | Medium | Missing fields | `RESEARCH_LOG.md` — Gates 1, 1.5, 2, 2.1 | `**Decision:**` and `**Evidence:**` fields absent in 4 gate entries despite the log's own template requiring them |
| A-2 | High | Stale metrics | `RESEARCH_LOG.md` — Gate 3 entry (lines 81–85) | Pre-reconciliation metric values never corrected: S1 AUROC=0.7635 (should be 0.6016), M1=0.7412 (→0.5877), PDC=1.0000 (→0.7667), S1 τ²=0.6821 (→0.5199) |
| A-3 | Medium | Stale split counts | `RESEARCH_LOG.md` — Gate 2 entry (line 62) | Split counts TRAIN=31,035/CALIB=10,521/TEST=10,548 do not match manifest canonical values (31,016/10,516/10,572) |
| A-4 | High | Stale metrics | `docs/DECISION_LOG.md` — `[FROZEN] Baseline Model Ladder` entry (line 70) | S1 AUROC=0.7635 and Recall@FAR=0.4128 are pre-reconciliation values; entry is marked [FROZEN] making correction require a deliberate amendment |
| A-5 | High | Broken evidence links | `docs/DECISION_LOG.md` — multiple entries | 9 evidence file paths reference sub-reports deleted during repository cleanup; files no longer exist as standalone documents |
| A-6 | Medium | Stale status | `docs/PROJECT_CONTROL.md` — Sections 21 & 22 | Section 21 says "BLOCKED pending Gate 1 approval"; Section 22 says "Not started" — both are stale by at least 3 gates |
| A-7 | Low | No ROADMAP date | `docs/ROADMAP.md` — all gate entries | No gate entry records an actual date; ROADMAP is a status tracker only, not an audit trail |
| A-8 | Low | Missing sub-gate entries | `docs/ROADMAP.md` | Gates 1.5, 2.1, 3.1, 3.2, 3.3 have no separate ROADMAP entries; they are absent or folded into a parent gate entry |
| A-9 | Low | Gate 0 undocumented | `RESEARCH_LOG.md`, `docs/DECISION_LOG.md` | Gate 0 (Artifact Understanding) appears only in ROADMAP; no log entry exists in either RESEARCH_LOG or DECISION_LOG |
| A-10 | High | Undocumented file locations | `AGENTS.md` Section 5 | The file map in AGENTS.md does not list `docs/DECISION_LOG.md`, `docs/PROJECT_CONTROL.md`, or `docs/ROADMAP.md` — their existence in `docs/` is undescribed in the enforcement checklist |
| A-11 | High | Unresolved contradiction | `gate3_1_report.md` vs `gate3_2_reconciliation.md` | TEST failed/successful episode breakdown: 4,270/2,803 (Gate 3.1) vs 3,936/3,137 (Gate 3.2) — contradiction not acknowledged or resolved in RESEARCH_LOG or DECISION_LOG |
| A-12 | Medium | Protocol deviation unrecorded | `docs/DECISION_LOG.md` | S1 is implemented as a Random Forest (classical ML) rather than a sequence model as specified by the frozen protocol. This deviation (Finding F-6 in repository audit) has no DECISION_LOG or RESEARCH_LOG entry recording the substitution decision |
| A-13 | High | Protocol violation unrecorded | `docs/DECISION_LOG.md` | Training without episode-balanced sample weights (Rule 11 violation, Finding F-7 in repository audit) is undocumented in DECISION_LOG or RESEARCH_LOG. No amendment entry exists |

---

## 8. Items Not Found (No History Invented)

The following items were searched for and **not found** in any project
document. They are reported as absent, not fabricated:

- No `DECISION_LOG.md` at the project root.
- No `PROJECT_CONTROL.md` at the project root.
- No `ROADMAP.md` at the project root.
- No RESEARCH_LOG entry for Gate 0.
- No ROADMAP entry for Gate 1.5, 2.1, 3.1, 3.2, or 3.3 as separate items.
- No DECISION_LOG entry for the S1 sequence-model substitution decision.
- No DECISION_LOG entry acknowledging the training sample weight omission.
- No correction of Gate 3 stale metrics in RESEARCH_LOG.
- No DECISION_LOG entry for the B=100 bootstrap substitution (default was B=500).

---

## 9. Audit Status

**Audit: COMPLETE — 13 findings catalogued.**  
**Documents read:** `RESEARCH_LOG.md`, `docs/DECISION_LOG.md`,
`docs/PROJECT_CONTROL.md`, `docs/ROADMAP.md`, `gate1_report.md`,
`gate1_5_report.md`, `gate2_report.md`, `gate2_1_report.md`,
`gate3_report.md`, `gate3_1_report.md`, `gate3_2_reconciliation.md`,
`gate3_3_result_lineage.md`, `gate3_4_repository_audit.md`.  
**No document was modified. No history was invented.**

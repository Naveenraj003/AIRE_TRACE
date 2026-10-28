# AIRE-Trace: Agent Insight and Reliability Evaluation Trace

## 1. What AIRE-Trace Is
AIRE-Trace is a standardized prospective, prefix-only evaluation protocol and harness for comparing AI-agent failure-warning methods on recorded execution trajectories. It fixes information visibility, failure-target definitions, alert semantics, calibration procedures, false-alarm constraints, lead-time measurement, and compute accounting across benchmarks.

---

## 2. Project Organization & Directory Structure

The repository is organized into six functional directories:

```
AIRE-TRACE/
├── 01_research/                       # 1. Research & Scientific Documentation
│   ├── RESEARCH_LOG.md                # Chronological master record of all findings
│   ├── AIRE-Trace_Frozen_Protocol_and_Plan.md # Authoritative scientific protocol
│   ├── PRD.md                         # Product Requirements Document
│   ├── TECHNICAL_DESIGN.md            # Technical Architecture & Invariant Specifications
│   ├── PROJECT_ANALYSIS.md            # Critical gap analysis and project overview
│   ├── AIRE-Trace — Prior-Art Claim-Element Chart.md # Prior art element benchmarking
│   ├── AIRE-Trace_Claim_Traceability_Audit.md        # Audit linking claims to empirical data
│   ├── AIRE-Trace_Figure_Traceability_Audit.md       # Audit verifying figures
│   └── docs/                          # In-depth research notes, logs, and literature surveys
│
├── 02_experiments/                    # 2. AIRE-Trace Project Experiments & Engine
│   ├── src/                           # Preprocessing, baselines, evaluation, and API modules
│   ├── tests/                         # Full automated test suite (54/54 tests passing)
│   ├── results/                       # Empirical outputs, prediction traces, and bootstrap runs
│   ├── data/                          # Dataset corpora (TerminalBench, tau-bench)
│   ├── configs/                       # Dataset and model configurations
│   ├── reports/                       # Generated analysis reports
│   ├── dataset_prep.py                # Dataset preparation pipeline
│   ├── repaired_636_canonical.json    # Canonical 636 study population
│   ├── exclusion_audit_results.csv    # 2,680 exclusion audit records
│   ├── recovery_manifest.json         # Lineage recovery manifest
│   ├── lineage_verification.txt       # Lineage verification certificate
│   ├── post_recovery_audit.txt        # Post-recovery audit record
│   ├── run_all.ps1                    # Master experiment execution script
│   └── validate_invariants.py         # Protocol invariant validator
│
├── 03_patent/                         # 3. Patent Filing Package (Indian Patent Office CRI 2025)
│   ├── Form 2 (3).docx                # Complete Specification in official Word format
│   ├── IPR Drawings Template(n).docx  # Statutory Drawing Sheets 1/4 to 4/4
│   ├── AIRE-Trace_Indian_Patent_Complete_Specification_Form2.md # Form 2 Complete Specification
│   ├── AIRE-Trace_Indian_Patent_Forms_1_and_5.md                # Form 1 (Grant) & Form 5 (Inventorship)
│   └── figures/                       # High-resolution patent drawings (Figs 1 to 4)
│
├── 04_ieee_publication/               # 4. IEEE Conference Publication Package
│   ├── AIRE-Trace_Universal_IEEE_Conference_Master.docx # 5-page IEEE Word document master
│   ├── AIRE-Trace_Universal_IEEE_Conference_Master.pdf  # 5-page high-resolution rendered PDF
│   ├── AIRE-Trace_IEEE_Conference_Paper.pdf             # Submission PDF
│   ├── AIRE-Trace_Master_IEEE_Manuscript.md             # Synchronized Markdown manuscript
│   ├── AIRE-Trace_Verified_References.md                # 20 verified IEEE bibliographic entries
│   ├── AIRE-Trace_IEEE_Submission_Readiness.md          # Submission audit checklist
│   ├── AIRE-Trace_Universal_IEEE_Master_README.md       # Package navigation guide
│   ├── build_ieee_full_under6_paper.py                  # Automated 5-page Word document builder
│   ├── generate_clean_ieee_figures.py                   # High-res 300-DPI figure generator
│   ├── verify_docx.py                                   # Automated Word document auditor
│   ├── verify_pdf.py                                    # Automated PDF auditor
│   ├── ieee_docx_helpers.py                             # Reusable docx formatting utilities
│   ├── figures/ieee/                                    # Publication figures (Figs 1 to 6)
│   └── AIRE-Trace_IEEE/                                 # LaTeX package (IEEEtran.cls & main.tex)
│
├── 05_archive/                        # 5. Archived & Superseded Assets
│   ├── archive/                       # Previous project archives (audits, historical drafts)
│   ├── scratch/                       # Temporary scratch scripts and intermediate tests
│   ├── build_ieee_6page_paper.py      # Intermediate builder
│   ├── generate_ieee_docx.py          # Legacy Word generator
│   └── consolidated_reference_data.py # Consolidated reference archive data
│
├── 06_templates_and_uploads/          # 6. Reference Templates & Uploads
│   ├── Conference-LaTeX-template_10-17-19/              # IEEE Conference LaTeX template
│   ├── Patent Template ZIP/                             # Official Indian Patent Word templates
│   └── GUIDELINES FOR EXAMINATION OF COMPUTER RELATED INVENTIONS (CRIs) - 2025.pdf
│
├── README.md                          # Repository Navigation & Directory Map
├── AGENTS.md                          # Mandatory Operational & Scientific Rules
├── pytest.ini                         # Test runner configuration
└── requirements.txt                   # Complete frozen environment dependencies
```

---

## 3. Quick Start & Execution

### Run Automated Tests
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
*Executes all 54 unit, protocol invariant, and regression tests across preprocessing, baselines, evaluation, and APIs.*

### Compile IEEE Conference Word Document & PDF
```powershell
# Compile the 5-page IEEE Word document
.\.venv\Scripts\python.exe 04_ieee_publication/build_ieee_full_under6_paper.py

# Audit the generated document against all 20 scientific invariants
.\.venv\Scripts\python.exe 04_ieee_publication/verify_docx.py
```

### Re-generate High-Resolution Figures (300 DPI)
```powershell
.\.venv\Scripts\python.exe 04_ieee_publication/generate_clean_ieee_figures.py
```

---

## 4. Key Authoritative Empirical Results
1. **Study Population Reconstruction:**
   - 3,316 declared Tracebench rows $\to$ 636 canonical study episodes (TRAIN = 163, CALIBRATION = 57, TEST = 416).
2. **Operational Recall Collapse:**
   - Conventional baselines ($H1-H4, M1, S1, S2$) exhibit weak-to-moderate ranking (AUROC 0.5074 to 0.6371), but suffer a prospective recall collapse (Recall@FAR near zero under an operational $5\%$ false-alarm budget).
3. **Trajectory Risk Decomposition (`dyn_comp`):**
   $$s_{\text{dyn\_comp}}(t) = P(M1 \mid e_{1:t}) - P(M_{\text{static}} \mid \text{task})$$
   - Calibrated threshold on CALIBRATION: $\tau^* = 0.5522$.
   - TEST performance: Prospective Recall@FAR $= 0.1167$ at $\text{FAR} = 0.0404$.
   - High-resolution joint bootstrap ($B=10,000$): $\Delta_{\text{obs}} = +0.1089$, $95\%\text{ CI } [0.0706, 0.1496]$, $p_{\text{adj}} = 9.999 \times 10^{-5}$ ($p < 0.0001$).
4. **Domain Sensitivity on Secondary Population (217 Gate-X Supported Episodes):**
   - Neither $M1$ nor `dyn_comp` crossed frozen calibration thresholds, confirming that thresholds must not be retuned post-hoc on test data.
5. **Feature Ablation (Group A4):**
   - Removing tool error and retry counts collapses $S1$ discrimination by $\Delta\text{AUROC} = -0.1069$ (from 0.6371 to 0.5302).

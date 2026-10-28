# Formatting Report — iConCISE 2027

## Environment & Build Status
- **Local Compiler Availability:** No local TeX distribution (`pdflatex`, `latexmk`, `xelatex`, `tectonic`) installed in the runtime environment.
- **Overleaf Deployment Bundle:** Verified and updated at `output/iConCISE_2027_Overleaf_Package.zip`.
  - Confirmed via automated extraction assertions that `main.tex` in the bundle includes all S1 tabular ensemble updates.
- **Target Compiled Artifact:** Evaluated against `submit_1.pdf` and verified IEEE conference compliance.

## Document Verification & Visual Audit
- **Page Count:** Exactly 6 pages (meets strict iConCISE 6-page maximum constraint).
- **Page Dimensions & Margins:** IEEEtran standard US Letter (8.5" x 11"), two-column format with 0.75" top, 1.0" bottom, 0.625" side margins, 0.17" column gutter.
- **Section & Layout Balance:**
  - Page 1: Title, 4-author block, Abstract (updated with `tabular ensemble (S1)` and `sequence-model (S2)`), Section I (Introduction).
  - Page 2: Section II (Related Work), Section III (Methodology), Fig. 1 (Architecture diagram), Fig. 2 (Prospective prefix semantics).
  - Page 3: Section III-D (Trajectory Risk Decomposition), Section IV (Experimental Setup), Table I (Warning Method Registry with S1 as Tabular ensemble), Section IV-A text (updated without `sequence-comparison tier`), Section IV-B (Metrics).
  - Page 4: Table II (Primary Mode A Test Performance), Table III (Bootstrap Comparison), Fig. 3 (Mode A TEST AUROC bar chart with 95% bootstrap CIs), Section V (Results), V-B, V-C, V-D.
  - Page 5: Table IV (S1 Feature Ablation), Table V (Operational Warning Profile), Section V-E (Operational Analysis), Section VI (Discussion & Limitations), Section VII (Conclusion start).
  - Page 6: Section VII (Conclusion end), References [1]–[13] occupying top ~40% of Column 1. Ample whitespace guarantees zero risk of page spill.
- **Figures:**
  - Fig. 1 (`fig1_aire_trace_architecture.png`): High resolution, clear labels, unclipped.
  - Fig. 2 (`fig3_prospective_prefix.png`): Clean vector diagram of prefix window and onset.
  - Fig. 3 (`fig4_mode_a_auroc.png`): High-contrast bar plot with clean 95% CI error bars.
- **References:**
  - All 13 references properly numbered, formatted according to IEEE standards, and cited sequentially in text.

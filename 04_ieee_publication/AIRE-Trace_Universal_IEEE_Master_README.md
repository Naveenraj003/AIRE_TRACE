# AIRE-Trace Universal IEEE Conference Master

## Purpose
This document package contains the venue-neutral IEEE conference master versions of the AIRE-Trace manuscript. It is designed to be easily adaptable to any appropriate IEEE conference by applying the venue-specific templates and constraints later.

* **`AIRE-Trace_Universal_IEEE_Conference_Master.tex`**: A generic Pandoc LaTeX conversion from the baseline Markdown. It is a venue-neutral baseline and NOT a pre-configured `IEEEtran` conference document.
* **`AIRE-Trace_Universal_IEEE_Conference_Master.pdf`**: A venue-neutral Markdown-rendered preview PDF. It is NOT the final two-column IEEE Xplore submission PDF.
* **`AIRE-Trace_Universal_IEEE_Conference_Master.docx`**: A generic DOCX conversion from the baseline Markdown.

## Source of Truth
The scientific content is based strictly on the frozen canonical project artifacts:
* `AIRE-Trace_Master_IEEE_Manuscript.md` (Primary scientific manuscript)
* `AIRE-Trace_Claim_Traceability_Audit.md` (Evidence audit)
* `AIRE-Trace_Verified_References.md` (13/13 verified references)
* `AIRE-Trace_Figure_Traceability_Audit.md` (Figure audit)
* `repaired_636_canonical.json` and all artifacts in `results/baseline_runs/` (Canonical empirical artifacts)

## Current Status
* **SCIENTIFIC STATE:** FROZEN
* **MANUSCRIPT:** COMPLETE
* **REFERENCES:** VERIFIED 13/13
* **FIGURES:** COMPLETE 6/6
* **VENUE:** UNDECIDED
* **PAGE LIMIT:** UNDECIDED
* **AUTHOR INFORMATION:** PLACEHOLDER

## Future Venue Adaptation
When a venue is selected, the following must be updated directly in the master documents:
* Apply the official venue-specific IEEE template (DOCX or LaTeX).
* Conform to the venue's specific page limit.
* Adjust paper size if the venue requires something other than US Letter.
* Apply blind-review mode (e.g., stripping author names) if required by the venue.
* Replace the `[AUTHOR BLOCK]` placeholders with real names, departments, institutions, and emails.
* Update submission metadata, copyright footer, and venue-specific declarations.
* Add supplementary material if required/allowed by the venue.
* Perform a final PDF validation according to IEEE Xplore requirements (e.g., using IEEE PDF eXpress).

## Scientific Invariants
The following critical frozen invariants must **never** be changed during venue adaptation to save space or adjust formatting:
* **Dataset Size:** 3,316 declared rows, 636 canonical study episodes.
* **Splits:** TRAIN = 163, CALIBRATION = 57, TEST = 416.
* **Failure Statistics:** 317 TEST failures, 99 successful episodes, 257 valid annotated failures, 60 unannotated failures.
* **Models Evaluated:** H1–H4, M1, S1, S2 (Model L remains unevaluated).
* **Threshold Rules:** Frozen thresholds, FAR ≤ 5%.
* **Statistical Methods:** Episode-cluster bootstrap (B=1000), Holm-Bonferroni correction.
* **Protocol Details:** Primary Mode A protocol, checkpoint horizon K=30.
* **Results:** All verified AUROC/AUPRC values, stated confidence intervals, A4 ablation degradation, PDC definition and coverage values.
* **Conclusions:** All stated scientific limitations.

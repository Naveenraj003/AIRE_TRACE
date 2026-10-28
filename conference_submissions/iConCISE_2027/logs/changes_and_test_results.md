# Change Log & Test Results

## Changes Made
- **Issue A Resolution (Table I Method Registry & Text Consistency):**
  - **Table I Registry:** Updated method family for **S1** in `Table I` (`working/main.tex`, line 331) from `Sequence$^\dagger$` to `Tabular ensemble`. Retained **S2** (GRU) as `Sequence`.
  - **Table I Footnote:** Streamlined to remove the registry discrepancy explanation (`$^\dagger$S1 classified Sequence by registry...`), retaining the hardware note: `\multicolumn{3}{@{}l}{\footnotesize L skipped: RTX~2050, 4\,GB.}`.
  - **Abstract Alignment:** Updated abstract model-family list (lines 72–74) so S1 is explicitly identified as `tabular ensemble (S1)` while S2 remains `sequence-model (S2)`.
  - **Methodology Text Alignment:** Replaced `sequence-comparison tier` in Section IV-A (lines 349–352) with wording identifying S1 as a tabular ensemble baseline: `S1 is evaluated as a tabular ensemble baseline that maps cumulative prefix trajectory statistics into a non-recurrent decision forest, directly contrasting with S2's hidden-state GRU recurrence.`
  - **Invariance Guarantee:** Preserved all model configurations, hyperparameters, thresholds, evaluation results, statistical procedures (bootstrap CI, Holm-Bonferroni correction), and protocol definitions without alteration.
- **Overleaf Package Update:**
  - Re-archived `output/iConCISE_2027_Overleaf_Package.zip` after programmatically verifying that `main.tex` in the zip bundle contains all corrected wording and definitions.

## Verification & Test Results
- **Package & Source Integrity:**
  - Automated Python assertion tests verified the presence of `tabular ensemble (S1)`, `sequence-model (S2)`, removal of `sequence-comparison tier`, and exact retention of all empirical values (AUROC, AUPRC, Recall@FAR, FAR, PDC).
- **Plagiarism & Similarity Audit (Crossref / iThenticate / Turnitin):**
  - Evaluated files: `Naveen (1).pdf` and `Naveen.pdf.pdf` (Submission ID: `trn:oid:::14348:637711911`).
  - **Filtered Similarity (Bibliography & Quotes excluded):** **1%** overall similarity (institutional affiliation match only).
  - **Unfiltered Similarity (Bibliography included):** **7%** overall similarity (solely arXiv reference titles in Section VIII).
  - **Single-Source Similarity:** Maximum 1%.
  - **Submitted Works:** **0%**.
  - **Integrity Flags:** **0 Flags**.
  - **Result:** **PASSED** with high margin.
- **Document Layout & Page Budget Audit:**
  - Target document length: Strictly 6 pages.
  - Page 6 headroom: References conclude at line 35 of Column 1, leaving ~60% of Column 1 and 100% of Column 2 free. Text adjustments in abstract (+16 chars) and methodology ($-2$ words) comfortably preserve the 6-page ceiling.

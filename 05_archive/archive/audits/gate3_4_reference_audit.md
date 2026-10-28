# Reference Audit Report

## 1. Broken References

The following internal references point to non-existent objects, files, or gates:

- **reports/gate1_5_report.md**:
  - `gate1_5_methodological_validation.md` (Broken file reference)
  - `gate1_5_warning_opportunity_analysis.md` (Broken file reference)
  - `gate1_5_onset_semantics.md` (Broken file reference)
  - `gate1_5_feature_novelty_analysis.md` (Broken file reference)

- **reports/gate1_report.md**:
  - `gate1_feature_comparison.md` (Broken file reference)
  - `gate1_leakage_audit.md` (Broken file reference)
  - `gate1_checkpoint_analysis.md` (Broken file reference)

- **reports/gate2_1_report.md**:
  - `gate2_1_episode_weighting_audit.md` (Broken file reference)
  - `gate2_1_retry_semantics.md` (Broken file reference)
  - `gate2_1_test_coverage.md` (Broken file reference)
  - `gate2_1_split_reproducibility.md` (Broken file reference)

- **reports/gate2_report.md**:
  - `gate2_preprocessing_report.md` (Broken file reference)
  - `gate2_feature_provenance.md` (Broken file reference)

- **reports/gate3_1_report.md**:
  - `gate3_1_prefix_reconciliation.md` (Broken file reference)
  - `gate3_1_threshold_semantics.md` (Broken file reference)
  - `gate3_1_metric_weighting.md` (Broken file reference)
  - `gate3_1_pdc_audit.md` (Broken file reference)
  - `gate3_1_bootstrap_audit.md` (Broken file reference)

- **reports/gate3_4_repository_audit.md**:
  - `gate3_1_report.md/gate3_2_reconciliation.md` (Broken file reference due to malformed path)

- **reports/repository_cleanup_report.md**:
  - `gate3_baseline_protocol.md` (Broken file reference)
  - `Gate R` (Broken gate reference)

## 2. Outdated References

The following references point to objects that have been renamed or whose types have changed:

- **reports/gate1_report.md**:
  - `gate1_dataset_inventory.md` is an outdated reference. The actual artifact generated is `gate1_dataset_inventory.json`.

## 3. Duplicated References

The following files contain redundant or duplicated definitions of references within the same document context:

- None identified in strict markdown link or cross-reference formatting, but standard cleanup is advised for documents that self-reference themselves via absolute paths (e.g. `reports/gate3_3_result_lineage.md` linking to itself).

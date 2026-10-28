import os
from pathlib import Path

# Repository root is 3 levels up from this file (src/api/config.py)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Paths to artifacts
MANIFESTS_DIR = REPO_ROOT / "data" / "processed" / "manifests"
RESULTS_DIR = REPO_ROOT / "results" / "baseline_runs"
REPORTS_DIR = REPO_ROOT / "reports"

TB_PREFIXES_PATH = MANIFESTS_DIR / "terminalbench_prefixes.parquet"
REPAIRED_CANONICAL_PATH = REPO_ROOT / "repaired_636_canonical.json"

PREDICTION_TRACES_PATH = RESULTS_DIR / "prediction_traces_k30.parquet"
PRIMARY_RESULTS_PATH = RESULTS_DIR / "primary_k30_results.json"
THRESHOLDS_PATH = RESULTS_DIR / "calibrated_thresholds.json"
PDC_SUMMARY_PATH = RESULTS_DIR / "pdc_summary.json"
LATE_DETECTIONS_PATH = REPORTS_DIR / "gate6_late_detections.json"
DYN_COMP_PREDICTIONS_PATH = RESULTS_DIR / "dyn_comp_predictions_k30.parquet"
DYN_COMP_THRESHOLDS_PATH = RESULTS_DIR / "dyn_comp_threshold_k30.json"
SIGNIFICANCE_PATH = RESULTS_DIR / "dyn_comp_vs_m1_bootstrap_k30_v2_B10000.json"

# Models
EXPECTED_MODELS = ["H1", "H2", "H3", "H4", "M1", "S1", "dyn_comp"]
HORIZON_K = 30

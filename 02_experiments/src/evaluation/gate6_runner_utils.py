"""
Shared runner utility for Gate 6 Diagnostics.
Provides common setup, data loading, and export functionality to prevent
duplication across diagnostic runner scripts.
"""

import os
import json
import math
import pandas as pd
from typing import Callable, Dict, Any
from src.evaluation.evaluator import MasterEvaluator

def replace_nan_with_none(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: replace_nan_with_none(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_nan_with_none(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    return obj

def run_gate6_diagnostic(
    diagnostic_name: str,
    analysis_func: Callable[[MasterEvaluator, pd.DataFrame, Dict[str, Any], int], Dict[str, Any]],
    output_filename: str,
    max_k: int = 30
):
    """
    Common orchestration shared by all Gate 6 diagnostic runners.
    - Setup directories
    - Load datasets and frozen thresholds
    - Instantiate evaluator
    - Run the provided diagnostic analysis
    - Clean and export results
    """
    print("==================================================")
    print(f"RUNNING AIRE-TRACE GATE 6 DIAGNOSTIC: {diagnostic_name.upper()}")
    print("==================================================")

    manifest_dir = r"p:\AIRE-TRACE\data\processed\manifests"
    results_dir = r"p:\AIRE-TRACE\results\baseline_runs"
    reports_dir = r"p:\AIRE-TRACE\reports"

    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    tb_path = os.path.join(manifest_dir, "terminalbench_prefixes.parquet")
    print(f"Loading manifest: {tb_path}...")
    df_tb = pd.read_parquet(tb_path)

    thresh_artifact_path = os.path.join(results_dir, "calibrated_thresholds.json")
    print(f"Loading frozen thresholds: {thresh_artifact_path}...")
    with open(thresh_artifact_path, "r", encoding="utf-8") as f:
        frozen_thresholds = json.load(f)

    evaluator = MasterEvaluator(target_far=0.05, random_seed=42)

    print(f"Running {diagnostic_name} for K = {max_k}...")
    results = analysis_func(evaluator, df_tb, frozen_thresholds, max_k)

    # Export to reports/ and results/
    report_artifact_path = os.path.join(reports_dir, output_filename)
    results_artifact_path = os.path.join(results_dir, output_filename)

    cleaned_results = replace_nan_with_none(results)

    with open(report_artifact_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_results, f, indent=2)

    with open(results_artifact_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_results, f, indent=2)

    print(f"Exported Gate 6 Artifacts:")
    print(f"  - {report_artifact_path}")
    print(f"  - {results_artifact_path}")
    print("==================================================")

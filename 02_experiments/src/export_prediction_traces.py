import os
import json
import math
import pandas as pd
import numpy as np
import tempfile
import shutil
import sys

# Ensure project root is in path if run from elsewhere
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.evaluation.evaluator import MasterEvaluator

def assert_parity(name, expected, actual):
    def is_undefined(val):
        if val is None:
            return True
        try:
            return math.isnan(float(val))
        except (ValueError, TypeError):
            return False

    if is_undefined(expected) and is_undefined(actual):
        exp_str = 'null' if expected is None else 'NaN'
        act_str = 'null' if actual is None else 'NaN'
        print(f"{name}")
        print(f"  Published:   {exp_str:<4} (undefined)")
        print(f"  Recomputed:  {act_str:<4} (undefined)")
        print(f"  Status:      PASS — equivalent undefined representation")
        return

    if is_undefined(expected) or is_undefined(actual):
        print(f"Parity Failure: {name}")
        print(f"  Published:  {expected}")
        print(f"  Recomputed: {actual}")
        raise AssertionError(f"Parity check failed for {name} (undefined/finite mismatch)")
        
    diff = abs(expected - actual)
    if not math.isclose(expected, actual, rel_tol=1e-12, abs_tol=1e-12):
        print(f"Parity Failure: {name}")
        print(f"  Published:  {expected:.12f}")
        print(f"  Recomputed: {actual:.12f}")
        print(f"  Difference: {diff:.12e}")
        raise AssertionError(f"Parity check failed for {name}")

def main():
    print("==================================================")
    print("AIRE-Trace Prediction Trace Exporter")
    print("==================================================")

    manifest_dir = r"P:\AIRE-TRACE\data\processed\manifests"
    results_dir = r"P:\AIRE-TRACE\results\baseline_runs"
    
    tb_path = os.path.join(manifest_dir, "terminalbench_prefixes.parquet")
    tau2_path = os.path.join(manifest_dir, "tau2_prefixes.parquet")
    primary_json_path = os.path.join(results_dir, "primary_k30_results.json")
    thresholds_json_path = os.path.join(results_dir, "calibrated_thresholds.json")
    final_artifact_path = os.path.join(results_dir, "prediction_traces_k30.parquet")

    # 1. Dataset Validation
    print("Loading manifests and validating dataset population...")
    df_tb = pd.read_parquet(tb_path)
    df_tau2 = pd.read_parquet(tau2_path)
    
    episodes = df_tb[["episode_id", "split", "eventual_outcome"]].drop_duplicates()
    total_eps = len(episodes)
    train_eps = len(episodes[episodes["split"] == "train"])
    calib_eps = len(episodes[episodes["split"] == "calibration"])
    test_eps = len(episodes[episodes["split"] == "test"])
    test_fails = len(episodes[(episodes["split"] == "test") & (episodes["eventual_outcome"] == 1)])
    
    assert total_eps == 636, f"Expected 636 total episodes, got {total_eps}"
    assert train_eps == 163, f"Expected 163 train episodes, got {train_eps}"
    assert calib_eps == 57, f"Expected 57 calibration episodes, got {calib_eps}"
    assert test_eps == 416, f"Expected 416 test episodes, got {test_eps}"
    assert test_fails == 317, f"Expected 317 TEST failures, got {test_fails}"
    print("Dataset population signature validated successfully.")

    # 2. Re-fit models and evaluate
    print("\nInstantiating MasterEvaluator and running deterministic evaluation...")
    evaluator = MasterEvaluator(target_far=0.05, bootstrap_iterations=1, random_seed=42)
    # compute_bootstrap=False will skip bootstrapping and save time
    results = evaluator.run_evaluation(df_tb, df_tau2, max_k=30, compute_bootstrap=False)
    
    # 3. Validation setup
    print("\nLoading frozen artifacts for parity verification...")
    with open(primary_json_path, "r", encoding="utf-8") as f:
        frozen_primary = json.load(f)
    with open(thresholds_json_path, "r", encoding="utf-8") as f:
        frozen_thresholds = json.load(f)
        
    expected_models = ["H1", "H2", "H3", "H4", "M1", "S1"]
    mode_a_results = results["mode_a_terminalbench_test"]
    frozen_mode_a = frozen_primary["mode_a_terminalbench_test"]
    
    # Verify overall configuration
    assert results["horizon_k"] == 30 == frozen_primary["horizon_k"]
    assert results["target_far"] == 0.05 == frozen_primary["target_far"]
    
    print("\nStarting strict parity checks (abs_tol=1e-12, rel_tol=1e-12)...")
    
    for m_id in expected_models:
        print(f"  Validating {m_id}...")
        
        # Verify valid annotated TEST failures from JSON (must equal 257)
        frozen_valid_fails = frozen_mode_a[m_id]["Exclusion_Stats"]["Valid_Episodes"]
        assert frozen_valid_fails == 257, f"Expected 257 valid annotated TEST failures for {m_id}, got {frozen_valid_fails}"
        
        # 3a. Threshold Verification
        new_thresh = results["calibrated_thresholds"][m_id]["frozen_threshold"]
        old_thresh = frozen_thresholds[m_id]["frozen_threshold"]
        assert_parity(f"{m_id} Calibrated Threshold", old_thresh, new_thresh)
        
        # 3b. Metric Parity
        new_metrics = mode_a_results[m_id]
        old_metrics = frozen_mode_a[m_id]
        
        for metric in ["AUROC", "AUPRC", "FAR", "Recall_at_FAR"]:
            assert_parity(f"{m_id} {metric}", old_metrics[metric], new_metrics[metric])

    print("All thresholds and target metrics perfectly matched the frozen canonical study.")

    # 4. Prediction Traces Extraction & Validation
    print("\nExtracting and validating prediction traces...")
    df_test_k = df_tb[(df_tb["split"] == "test") & (df_tb["prefix_len"] <= 30)]
    n_test_prefixes = len(df_test_k)
    mode_a_predictions = results["mode_a_predictions"]
    
    dfs_to_concat = []
    
    for m_id in expected_models:
        preds = mode_a_predictions[m_id]
        
        # Shape check
        assert len(preds) == n_test_prefixes, f"Shape mismatch for {m_id}: {len(preds)} != {n_test_prefixes}"
        
        # Probability validity check
        if not np.all((preds >= 0.0) & (preds <= 1.0)):
            raise AssertionError(f"Probabilities out of bounds [0, 1] for {m_id}")
        if np.any(np.isnan(preds)) or np.any(np.isinf(preds)):
            raise AssertionError(f"NaN or Inf found in probabilities for {m_id}")
            
        # Alignment check
        df_model = df_test_k[["episode_id", "prefix_len"]].copy()
        df_model["model_id"] = m_id
        df_model["predicted_probability"] = preds
        
        dfs_to_concat.append(df_model)
        
    df_final = pd.concat(dfs_to_concat, ignore_index=True)
    
    # Final row count check
    expected_rows = n_test_prefixes * len(expected_models)
    assert len(df_final) == expected_rows, f"Total rows mismatch: {len(df_final)} != {expected_rows}"
    
    # Uniqueness check
    unique_count = df_final.groupby(["model_id", "episode_id", "prefix_len"]).size().max()
    assert unique_count == 1, f"Found duplicate prediction keys! Max count = {unique_count}"
    
    print("Prediction trace dimensions, alignment, and bounds strictly validated.")

    # 5. Atomic File Creation
    print(f"\nWriting artifact atomically to {final_artifact_path}...")
    fd, temp_path = tempfile.mkstemp(suffix=".parquet", dir=results_dir)
    os.close(fd)
    
    try:
        df_final.to_parquet(temp_path, index=False)
        # Validate temporary artifact is readable
        pd.read_parquet(temp_path)
        # Atomically replace
        os.replace(temp_path, final_artifact_path)
        print("SUCCESS! Canonical prediction trace artifact exported.")
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise RuntimeError(f"Failed to export artifact atomically: {e}")

if __name__ == "__main__":
    main()

import os
import json
import numpy as np
import pandas as pd
from src.evaluation.statistical_testing import compute_paired_bootstrap_test

def run_population(df_pop, pop_name, pop_desc, out_filename, supp_source=None):
    n_test_episodes = int(df_pop["episode_id"].nunique())
    n_prefixes = len(df_pop)
    
    # Thresholds
    cal = json.load(open("results/baseline_runs/calibrated_thresholds.json"))
    thr = json.load(open("results/baseline_runs/dyn_comp_threshold_k30.json"))
    m1_thresh = float(cal["M1"]["frozen_threshold"])
    dyn_thresh = float(thr["dyn_comp_frozen_threshold"])
    
    thresholds = {
        "dyn_comp": dyn_thresh,
        "M1": m1_thresh
    }
    
    predictions = {
        "dyn_comp": df_pop["dyn_comp"].values,
        "M1": df_pop["prob_m1"].values
    }
    
    # Run canonical paired bootstrap test
    results = compute_paired_bootstrap_test(
        df_prefixes=df_pop,
        predictions=predictions,
        base_model="dyn_comp",
        comparators=["M1"],
        n_iterations=1000,
        random_seed=42,
        max_k=30,
        metrics=["Recall_at_FAR"],
        thresholds=thresholds,
        mode="prospective"
    )
    
    res = results[0]
    diag = res["diagnostics"]
    
    # Episode count breakdown
    df_tmp = df_pop.copy()
    df_tmp["onset_step"] = pd.to_numeric(df_tmp["annotation_derived_onset_step"], errors="coerce")
    succ = df_tmp[df_tmp["eventual_outcome"] == 0]
    n_succ = int(succ["episode_id"].nunique())
    
    fail = df_tmp[df_tmp["eventual_outcome"] == 1]
    fail_valid_mask = (
        (fail["onset_annotated"].astype(bool)) &
        (fail["onset_step"].notna()) &
        (fail["prefix_len"] <= fail["onset_step"])
    )
    n_valid_fail = int(fail[fail_valid_mask]["episode_id"].nunique())
    
    out_record = {
        "comparison": res["comparison"],
        "metric": res["metric"],
        "mode": "prospective",
        "population": pop_desc,
        "n_test_episodes": n_test_episodes,
        "n_success_episodes": n_succ,
        "n_valid_failure_episodes": n_valid_fail,
        "n_prefixes": n_prefixes,
        "horizon_k": 30,
        "B": 1000,
        "random_seed": 42,
        "m1_frozen_threshold": m1_thresh,
        "m1_threshold_source": "results/baseline_runs/calibrated_thresholds.json",
        "dyn_comp_frozen_threshold": dyn_thresh,
        "dyn_comp_threshold_source": "results/baseline_runs/dyn_comp_threshold_k30.json",
        "obs_m1_recall": diag["comp_obs_recall"],
        "obs_m1_far": diag["comp_obs_far"],
        "obs_dyn_recall": diag["base_obs_recall"],
        "obs_dyn_far": diag["base_obs_far"],
        "obs_diff_dyn_minus_m1": res["delta_obs"],
        "bootstrap_mean_diff": res["bootstrap_mean_delta"],
        "ci_lower_95": res["ci_lower_95"],
        "ci_upper_95": res["ci_upper_95"],
        "p_raw": res["p_raw"],
        "p_adj": res["p_adj"],
        "alpha": res["alpha"],
        "reject_H0": res["reject_H0"],
        "diagnostics": {
            "m1_bootstrap_far_mean": diag["comp_bootstrap_far_mean"],
            "m1_bootstrap_far_ci_95": diag["comp_bootstrap_far_ci_95"],
            "dyn_comp_bootstrap_far_mean": diag["base_bootstrap_far_mean"],
            "dyn_comp_bootstrap_far_ci_95": diag["base_bootstrap_far_ci_95"],
            "m1_bootstrap_fars_first10": diag["comp_bootstrap_fars"][:10],
            "dyn_comp_bootstrap_fars_first10": diag["base_bootstrap_fars"][:10]
        },
        "methodology": "Canonical compute_paired_bootstrap_test with joint episode-cluster resampling and null-centered p-value formula.",
        "status": "AUTHORITATIVE"
    }
    
    if supp_source:
        out_record["population_source"] = supp_source
        
    out_path = os.path.join("results/baseline_runs", out_filename)
    with open(out_path, "w") as f:
        json.dump(out_record, f, indent=2)
    print(f"Saved {pop_name} to {out_path}")
    return out_record

def main():
    parquet_path = "results/baseline_runs/dyn_comp_predictions_k30.parquet"
    df_all = pd.read_parquet(parquet_path)
    
    # 1. 416-episode primary population
    rec_416 = run_population(
        df_all,
        pop_name="416 Primary Population",
        pop_desc="416 TEST episodes (full, unfiltered)",
        out_filename="dyn_comp_vs_m1_bootstrap_k30_v2.json"
    )
    
    # 2. 217-episode Gate-X secondary population
    supp_path = "results/baseline_runs/gate_x_supported_episode_ids.json"
    supp_data = json.load(open(supp_path))
    supp_ids = set(supp_data["supported_episode_ids"])
    df_217 = df_all[df_all["episode_id"].isin(supp_ids)].copy()
    
    rec_217 = run_population(
        df_217,
        pop_name="217 Gate-X Secondary Population",
        pop_desc="217 Gate-X supported TEST episodes",
        out_filename="dyn_comp_vs_m1_bootstrap_k30_supported217_v2.json",
        supp_source=supp_path
    )
    
    print("\n--- SUMMARY OF RUNS ---")
    print("416 Population:")
    print(f"  Observed Diff: {rec_416['obs_diff_dyn_minus_m1']:.4f}")
    print(f"  Bootstrap Mean Diff: {rec_416['bootstrap_mean_diff']:.4f}")
    print(f"  95% CI: [{rec_416['ci_lower_95']:.4f}, {rec_416['ci_upper_95']:.4f}]")
    print(f"  p_raw: {rec_416['p_raw']:.6f}, p_adj: {rec_416['p_adj']:.6f}")
    print(f"  Reject H0 (alpha=0.05): {rec_416['reject_H0']}")
    
    print("\n217 Population:")
    print(f"  Observed Diff: {rec_217['obs_diff_dyn_minus_m1']:.4f}")
    print(f"  Bootstrap Mean Diff: {rec_217['bootstrap_mean_diff']:.4f}")
    print(f"  95% CI: [{rec_217['ci_lower_95']:.4f}, {rec_217['ci_upper_95']:.4f}]")
    print(f"  p_raw: {rec_217['p_raw']:.6f}, p_adj: {rec_217['p_adj']:.6f}")
    print(f"  Reject H0 (alpha=0.05): {rec_217['reject_H0']}")

if __name__ == "__main__":
    main()

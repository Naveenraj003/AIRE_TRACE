import os
import json
import numpy as np
import pandas as pd
from src.evaluation.statistical_testing import compute_paired_bootstrap_test

def main():
    parquet_path = "results/baseline_runs/dyn_comp_predictions_k30.parquet"
    df_all = pd.read_parquet(parquet_path)
    
    n_test_episodes = int(df_all["episode_id"].nunique())
    n_prefixes = len(df_all)
    
    # Load frozen thresholds
    cal = json.load(open("results/baseline_runs/calibrated_thresholds.json"))
    thr = json.load(open("results/baseline_runs/dyn_comp_threshold_k30.json"))
    m1_thresh = float(cal["M1"]["frozen_threshold"])
    dyn_thresh = float(thr["dyn_comp_frozen_threshold"])
    
    thresholds = {
        "dyn_comp": dyn_thresh,
        "M1": m1_thresh
    }
    
    predictions = {
        "dyn_comp": df_all["dyn_comp"].values,
        "M1": df_all["prob_m1"].values
    }
    
    B = 10000
    random_seed = 42
    
    print(f"Executing compute_paired_bootstrap_test with B={B}, random_seed={random_seed}...")
    results = compute_paired_bootstrap_test(
        df_prefixes=df_all,
        predictions=predictions,
        base_model="dyn_comp",
        comparators=["M1"],
        n_iterations=B,
        random_seed=random_seed,
        max_k=30,
        metrics=["Recall_at_FAR"],
        thresholds=thresholds,
        mode="prospective"
    )
    
    res = results[0]
    diag = res["diagnostics"]
    
    # Count extreme replicates exactly:
    # p_raw = (1 + count_extreme) / (B + 1)
    # count_extreme = int(round(p_raw * (B + 1) - 1))
    count_extreme = int(round(res["p_raw"] * (B + 1) - 1))
    
    # Episode count breakdown
    df_tmp = df_all.copy()
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
    n_excluded_fail = int(fail["episode_id"].nunique()) - n_valid_fail
    
    out_record = {
        "comparison": res["comparison"],
        "metric": res["metric"],
        "mode": "prospective",
        "population": "416 TEST episodes (full, unfiltered)",
        "n_test_episodes": n_test_episodes,
        "n_success_episodes": n_succ,
        "n_valid_failure_episodes": n_valid_fail,
        "n_excluded_failure_episodes": n_excluded_fail,
        "n_prefixes": n_prefixes,
        "horizon_k": 30,
        "B": B,
        "random_seed": random_seed,
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
        "count_extreme_replicates": count_extreme,
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
        "status": "AUTHORITATIVE_HIGH_RESOLUTION_B10000"
    }
    
    out_path = "results/baseline_runs/dyn_comp_vs_m1_bootstrap_k30_v2_B10000.json"
    with open(out_path, "w") as f:
        json.dump(out_record, f, indent=2)
    print(f"Saved B=10,000 result to {out_path}")
    
    print("\n--- RESULTS (B=10,000) ---")
    print(f"Population: {n_test_episodes} episodes ({n_succ} succ, {n_valid_fail} valid fail, {n_excluded_fail} excluded fail)")
    print(f"Observed M1 Recall: {diag['comp_obs_recall']:.4f}, FAR: {diag['comp_obs_far']:.4f}")
    print(f"Observed dyn_comp Recall: {diag['base_obs_recall']:.4f}, FAR: {diag['base_obs_far']:.4f}")
    print(f"Observed Difference (dyn - M1): {res['delta_obs']:.4f}")
    print(f"Bootstrap Mean Difference: {res['bootstrap_mean_delta']:.4f}")
    print(f"95% CI: [{res['ci_lower_95']:.4f}, {res['ci_upper_95']:.4f}]")
    print(f"Extreme Replicates (|Delta_0| >= |Delta_obs|): {count_extreme} / {B}")
    print(f"p_raw: {res['p_raw']:.8f}")
    print(f"p_adj: {res['p_adj']:.8f}")
    print(f"Reject H0 (alpha=0.05): {res['reject_H0']}")

if __name__ == "__main__":
    main()

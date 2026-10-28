"""
AIRE-Trace Episode-Cluster Bootstrap Module
Resamples unique episode_id units (NOT prefix rows) to compute non-parametric 95% Confidence Intervals.
Fully vectorized for sub-second execution speed.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List
from src.evaluation.metrics import (
    compute_sample_weights,
    compute_weighted_auroc,
    compute_weighted_auprc,
    compute_weighted_brier,
    compute_weighted_ece
)

def compute_episode_bootstrap_ci(
    df_prefixes: pd.DataFrame,
    y_prob: np.ndarray,
    threshold: float,
    n_iterations: int = 100,
    random_seed: int = 42,
    max_k: int = 30,
    mode: str = "prospective"
) -> Dict[str, Dict[str, float]]:
    """
    Performs episode-level cluster bootstrap resampling.
    Requires mode="prospective" to ensure valid failure onsets.
    """
    if mode != "prospective":
        raise ValueError("Bootstrap is only supported for prospective mode.")
    
    rng = np.random.RandomState(random_seed)
    
    unique_episodes, ep_inverse = np.unique(df_prefixes["episode_id"].values, return_inverse=True)
    n_episodes = len(unique_episodes)
    
    # Pre-group row indices per episode integer ID
    ep_row_indices = [np.where(ep_inverse == i)[0] for i in range(n_episodes)]
    
    y_true_all = df_prefixes["eventual_outcome"].values.astype(int)
    weights_all = compute_sample_weights(df_prefixes, max_k=max_k)
    
    # Pre-aggregate episode-level max probabilities and outcomes
    df_tmp = df_prefixes[["episode_id", "eventual_outcome", "onset_annotated", "annotation_derived_onset_step", "prefix_len"]].copy()
    df_tmp["prob"] = y_prob

    ep_all = df_tmp.groupby("episode_id").agg(
        outcome=("eventual_outcome", "first"),
        max_prob=("prob", "max")
    )
    succ_probs = ep_all[ep_all["outcome"] == 0]["max_prob"].values
    n_succ = len(succ_probs)

    fail_df = df_tmp[df_tmp["eventual_outcome"] == 1]

    if mode == "prospective":
        onset_col = pd.to_numeric(fail_df["annotation_derived_onset_step"], errors="coerce")
        valid_episodes = fail_df[(fail_df["onset_annotated"].astype(bool)) & (onset_col.notna())]["episode_id"].unique()
        n_fail = len(valid_episodes)
        
        valid_mask = (
            (fail_df["onset_annotated"].astype(bool)) & 
            (onset_col.notna()) & 
            (fail_df["prefix_len"] <= onset_col)
        )
        fail_valid_df = fail_df[valid_mask]
        fail_probs = fail_valid_df.groupby("episode_id")["prob"].max().values
    elif mode == "raw":
        n_fail = fail_df["episode_id"].nunique()
        fail_probs = fail_df.groupby("episode_id")["prob"].max().values
    else:
        raise ValueError(f"Unknown mode: {mode}")

    metric_bootstraps = {
        "AUROC": [],
        "AUPRC": [],
        "FAR": [],
        "Brier": [],
        "ECE": []
    }
    
    recall_key = "Recall_at_FAR" if mode == "prospective" else "Raw_Recall"
    metric_bootstraps[recall_key] = []
    
    for b in range(n_iterations):
        # Resample episode integer IDs with replacement
        sampled_ep_ids = rng.choice(n_episodes, size=n_episodes, replace=True)
        sampled_row_indices = np.concatenate([ep_row_indices[i] for i in sampled_ep_ids])
        
        y_true_sub = y_true_all[sampled_row_indices]
        y_prob_sub = y_prob[sampled_row_indices]
        weights_sub = weights_all[sampled_row_indices]
        
        auroc = compute_weighted_auroc(y_true_sub, y_prob_sub, weights_sub)
        auprc = compute_weighted_auprc(y_true_sub, y_prob_sub, weights_sub)
        brier = compute_weighted_brier(y_true_sub, y_prob_sub, weights_sub)
        ece = compute_weighted_ece(y_true_sub, y_prob_sub, weights_sub)
        
        # Resample episode-level FAR and Recall directly from pre-aggregated arrays
        sampled_succ_indices = rng.choice(n_succ, size=n_succ, replace=True) if n_succ > 0 else []
        sampled_fail_indices = rng.choice(len(fail_probs), size=n_fail, replace=True) if n_fail > 0 and len(fail_probs) > 0 else []
        
        far = float(np.sum(succ_probs[sampled_succ_indices] >= threshold) / n_succ) if n_succ > 0 else 0.0
        recall = float(np.sum(fail_probs[sampled_fail_indices] >= threshold) / n_fail) if n_fail > 0 else 0.0
        
        metric_bootstraps["AUROC"].append(auroc)
        metric_bootstraps["AUPRC"].append(auprc)
        metric_bootstraps["Brier"].append(brier)
        metric_bootstraps["ECE"].append(ece)
        metric_bootstraps["FAR"].append(far)
        metric_bootstraps[recall_key].append(recall)
        
    ci_results = {}
    for k, vals in metric_bootstraps.items():
        arr = np.array(vals)
        ci_lower = float(np.percentile(arr, 2.5))
        ci_upper = float(np.percentile(arr, 97.5))
        mean_val = float(np.mean(arr))
        ci_results[k] = {
            "mean": round(mean_val, 4),
            "ci_lower": round(ci_lower, 4),
            "ci_upper": round(ci_upper, 4)
        }
        
    return ci_results

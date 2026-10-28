"""
AIRE-Trace Calibration Threshold Selection Module
Selects warning threshold tau on CALIBRATION set by maximizing Recall subject to FAR <= target_far (5%).
Selected threshold is frozen and exported for untouched evaluation on TEST and tau2-Bench.
Vectorized for maximum computational speed.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

def compute_episode_far_and_recall(
    df_prefixes: pd.DataFrame,
    y_prob: np.ndarray,
    threshold: float,
    mode: str = "prospective"
) -> Tuple[float, float, Dict[str, int]]:
    """
    Computes episode-level False Alarm Rate (FAR) and Recall at threshold tau.
    Fast vectorized implementation.
    """
    df_tmp = df_prefixes[["episode_id", "eventual_outcome", "onset_annotated", "annotation_derived_onset_step", "prefix_len"]].copy()
    df_tmp["prob"] = y_prob
    
    exclusion_stats = {}

    # 1. Episode maximum probability for all prefixes
    ep_all = df_tmp.groupby("episode_id").agg(
        outcome=("eventual_outcome", "first"),
        max_prob=("prob", "max")
    )
    succ_probs = ep_all[ep_all["outcome"] == 0]["max_prob"].values
    n_succ = len(succ_probs)
    far = float(np.sum(succ_probs >= threshold) / n_succ) if n_succ > 0 else 0.0

    # 2. Episode maximum probability for prospective prefixes (t <= onset)
    fail_df = df_tmp[df_tmp["eventual_outcome"] == 1]
    
    if mode == "prospective":
        row_has_annot = fail_df["onset_annotated"].astype(bool)
        onset_col = pd.to_numeric(fail_df["annotation_derived_onset_step"], errors="coerce")
        row_has_onset = onset_col.notna()
        row_is_valid = row_has_annot & row_has_onset
        
        ep_valid = fail_df[row_is_valid]["episode_id"].unique()
        ep_annot = fail_df[row_has_annot]["episode_id"].unique()
        total_fail = fail_df["episode_id"].nunique()
        
        n_fail = len(ep_valid)
        unannotated = total_fail - len(ep_annot)
        malformed = len(ep_annot) - len(ep_valid)
        excluded = total_fail - n_fail
        
        exclusion_stats = {
            "Total_Failures": total_fail,
            "Valid_Episodes": n_fail,
            "Unannotated_Episodes": unannotated,
            "Malformed_Episodes": malformed,
            "Excluded_Episodes": excluded
        }
        
        if n_fail == 0:
            return far, 0.0, exclusion_stats

        valid_mask = (
            (fail_df["onset_annotated"].astype(bool)) & 
            (onset_col.notna()) & 
            (fail_df["prefix_len"] <= onset_col)
        )
        fail_valid_df = fail_df[valid_mask]
        fail_probs = fail_valid_df.groupby("episode_id")["prob"].max().values
    elif mode == "raw":
        n_fail = fail_df["episode_id"].nunique()
        if n_fail == 0:
            return far, 0.0, {}
        fail_probs = fail_df.groupby("episode_id")["prob"].max().values
    else:
        raise ValueError(f"Unknown mode: {mode}")

    recall = float(np.sum(fail_probs >= threshold) / n_fail)
    return far, recall, exclusion_stats


def select_calibration_threshold(
    df_calib: pd.DataFrame,
    y_prob_calib: np.ndarray,
    target_far: float = 0.05
) -> Dict[str, Any]:
    """
    Sweeps thresholds tau in [0.0, 1.0] on CALIBRATION dataset.
    Selects threshold tau* maximizing Recall subject to FAR <= target_far.
    Fast vectorized threshold sweep.
    """
    df_tmp = df_calib[["episode_id", "eventual_outcome", "onset_annotated", "annotation_derived_onset_step", "prefix_len"]].copy()
    df_tmp["prob"] = y_prob_calib

    # Pre-aggregate episode max probabilities ONCE
    ep_all = df_tmp.groupby("episode_id").agg(
        outcome=("eventual_outcome", "first"),
        max_prob=("prob", "max")
    )
    succ_probs = ep_all[ep_all["outcome"] == 0]["max_prob"].values
    n_succ = len(succ_probs)

    fail_df = df_tmp[df_tmp["eventual_outcome"] == 1]
    
    # Calibration evaluates strictly on prospective recall
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

    candidate_thresholds = np.linspace(0.01, 0.99, 99)
    best_tau = 0.5
    best_recall = -1.0
    best_far = 1.0
    threshold_records = []

    for tau in candidate_thresholds:
        far = float(np.sum(succ_probs >= tau) / n_succ) if n_succ > 0 else 0.0
        recall = float(np.sum(fail_probs >= tau) / n_fail) if n_fail > 0 else 0.0
        threshold_records.append({"threshold": float(tau), "far": far, "recall": recall})
        
        if far <= target_far:
            if recall > best_recall or (recall == best_recall and far < best_far):
                best_tau = float(tau)
                best_recall = recall
                best_far = far

    if best_recall < 0:
        df_rec = pd.DataFrame(threshold_records)
        min_far_row = df_rec.loc[df_rec["far"].idxmin()]
        best_tau = float(min_far_row["threshold"])
        best_far = float(min_far_row["far"])
        best_recall = float(min_far_row["recall"])

    return {
        "frozen_threshold": round(best_tau, 4),
        "calibration_far": round(best_far, 4),
        "calibration_recall": round(best_recall, 4),
        "target_far": target_far,
        "search_history": threshold_records
    }

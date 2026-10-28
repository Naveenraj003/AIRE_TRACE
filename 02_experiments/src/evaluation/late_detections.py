"""
AIRE-Trace Gate 6 Late Detections Analysis Module
Identifies warning alerts occurring after failure onset (alert_step > failure_onset_step).
Reports late alert statistics per model without modifying primary evaluation outputs.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any

def compute_late_detections_for_model(
    df_test: pd.DataFrame,
    y_prob: np.ndarray,
    threshold: float
) -> Dict[str, Any]:
    """
    Computes late detection statistics for a single model at specified threshold.
    
    Late alert condition:
    eventual_outcome == 1 AND onset_annotated == True AND prefix_len > annotation_derived_onset_step AND y_prob >= threshold.
    """
    df_tmp = df_test[["episode_id", "prefix_len", "eventual_outcome", "onset_annotated", "annotation_derived_onset_step"]].copy()
    df_tmp["prob"] = y_prob

    # Filter to failure episodes
    fail_df = df_tmp[df_tmp["eventual_outcome"] == 1].copy()

    # Identify valid failure episodes (annotated with non-null onset)
    row_has_annot = fail_df["onset_annotated"].astype(bool)
    onset_col = pd.to_numeric(fail_df["annotation_derived_onset_step"], errors="coerce")
    row_has_onset = onset_col.notna()
    valid_mask = row_has_annot & row_has_onset

    valid_fail_df = fail_df[valid_mask].copy()
    valid_fail_df["onset_step"] = pd.to_numeric(valid_fail_df["annotation_derived_onset_step"])

    valid_episodes = valid_fail_df["episode_id"].unique()
    total_valid_fail_episodes = len(valid_episodes)

    if total_valid_fail_episodes == 0:
        return {
            "total_late_alerts": 0,
            "unique_late_alert_episodes": 0,
            "total_valid_fail_episodes": 0,
            "only_late_alert_episodes": 0,
            "pct_failed_episodes_with_only_late_alerts": 0.0,
            "lateness_min": None,
            "lateness_max": None,
            "lateness_mean": None,
            "lateness_median": None
        }

    # Evaluate alerts
    valid_fail_df["is_alert"] = valid_fail_df["prob"] >= threshold
    valid_fail_df["is_early"] = valid_fail_df["is_alert"] & (valid_fail_df["prefix_len"] <= valid_fail_df["onset_step"])
    valid_fail_df["is_late"] = valid_fail_df["is_alert"] & (valid_fail_df["prefix_len"] > valid_fail_df["onset_step"])
    valid_fail_df["lateness"] = np.where(valid_fail_df["is_late"], valid_fail_df["prefix_len"] - valid_fail_df["onset_step"], np.nan)

    late_alerts = valid_fail_df[valid_fail_df["is_late"]]
    total_late_alerts = int(len(late_alerts))
    unique_late_alert_episodes = int(late_alerts["episode_id"].nunique())

    # Episode-level classification
    ep_summary = valid_fail_df.groupby("episode_id").agg(
        has_early=("is_early", "any"),
        has_late=("is_late", "any")
    )
    
    # Fill in any valid failure episodes that had 0 prefixes in valid_fail_df
    ep_summary = ep_summary.reindex(valid_episodes, fill_value=False)

    ep_summary["only_late"] = ep_summary["has_late"] & (~ep_summary["has_early"])
    only_late_episodes_count = int(ep_summary["only_late"].sum())
    pct_only_late = float((only_late_episodes_count / total_valid_fail_episodes) * 100.0)

    if total_late_alerts > 0:
        lateness_vals = late_alerts["lateness"].values
        lateness_min = float(np.min(lateness_vals))
        lateness_max = float(np.max(lateness_vals))
        lateness_mean = float(np.mean(lateness_vals))
        lateness_median = float(np.median(lateness_vals))
    else:
        lateness_min = None
        lateness_max = None
        lateness_mean = None
        lateness_median = None

    return {
        "total_late_alerts": total_late_alerts,
        "unique_late_alert_episodes": unique_late_alert_episodes,
        "total_valid_fail_episodes": total_valid_fail_episodes,
        "only_late_alert_episodes": only_late_episodes_count,
        "pct_failed_episodes_with_only_late_alerts": round(pct_only_late, 4),
        "lateness_min": round(lateness_min, 4) if lateness_min is not None else None,
        "lateness_max": round(lateness_max, 4) if lateness_max is not None else None,
        "lateness_mean": round(lateness_mean, 4) if lateness_mean is not None else None,
        "lateness_median": round(lateness_median, 4) if lateness_median is not None else None
    }


def run_late_detections_analysis(
    evaluator,
    df_tb: pd.DataFrame,
    frozen_thresholds: Dict[str, Any],
    max_k: int = 30
) -> Dict[str, Any]:
    """
    Executes full Gate 6 late detections analysis across baseline models.
    Reuses MasterEvaluator._prepare_fitted_models() and loaded frozen thresholds.
    Does NOT compute calibration thresholds or invoke select_calibration_threshold().
    """
    df_tb_k = df_tb[df_tb["prefix_len"] <= max_k].copy()
    df_train = df_tb_k[df_tb_k["split"] == "train"].copy()
    df_test = df_tb_k[df_tb_k["split"] == "test"].copy()

    # Reuse shared fitted models helper
    fitted_models = evaluator._prepare_fitted_models(df_train)

    results = {}
    for m_id, model in fitted_models.items():
        if m_id == "L" or model == "L_PENDING":
            continue

        # Extract frozen threshold from exported Gate 5 artifact dict or numeric value
        t_info = frozen_thresholds.get(m_id)
        if isinstance(t_info, dict):
            frozen_thresh = float(t_info["frozen_threshold"])
        elif isinstance(t_info, (int, float)):
            frozen_thresh = float(t_info)
        else:
            raise KeyError(f"Missing frozen threshold for model '{m_id}' in frozen_thresholds input.")

        prob_test = model.predict_proba(df_test)
        late_stats = compute_late_detections_for_model(df_test, prob_test, frozen_thresh)
        late_stats["frozen_threshold"] = round(float(frozen_thresh), 4)

        results[m_id] = late_stats

    return {
        "horizon_k": max_k,
        "target_far": evaluator.target_far,
        "late_detections": results
    }

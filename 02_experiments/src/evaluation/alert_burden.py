"""
AIRE-Trace Gate 6.3 Alert Burden Analysis Module
Computes overall alert burden statistics for models using frozen thresholds.
Reports statistics independently of primary evaluation metrics.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any

def compute_alert_burden_for_model(
    df_test: pd.DataFrame,
    y_prob: np.ndarray,
    threshold: float
) -> Dict[str, Any]:
    """
    Computes diagnostic alert burden statistics for a single model at specified threshold.
    Alert condition: y_prob >= threshold.
    Calculates total alerts and per-episode distributions.
    """
    df_tmp = df_test[["episode_id", "prefix_len"]].copy()
    df_tmp["prob"] = y_prob
    df_tmp["is_alert"] = df_tmp["prob"] >= threshold

    total_alerts = int(df_tmp["is_alert"].sum())
    total_episodes = df_tmp["episode_id"].nunique()

    if total_episodes == 0:
        return {
            "total_alerts": 0,
            "mean_alerts_per_episode": None,
            "median_alerts_per_episode": None,
            "min_alerts_per_episode": None,
            "max_alerts_per_episode": None,
            "alerts_distribution": {}
        }

    alert_counts = df_tmp.groupby("episode_id")["is_alert"].sum()
    counts = alert_counts.values

    ab_min = int(np.min(counts))
    ab_max = int(np.max(counts))
    ab_mean = float(np.mean(counts))
    ab_median = float(np.median(counts))

    # Histogram-ready counts: mapping from "number of alerts" -> "count of episodes"
    # To keep JSON serialization clean, convert keys to strings
    val_counts = alert_counts.value_counts().to_dict()
    alerts_distribution = {str(k): int(v) for k, v in sorted(val_counts.items())}

    return {
        "total_alerts": total_alerts,
        "mean_alerts_per_episode": round(ab_mean, 4),
        "median_alerts_per_episode": round(ab_median, 4),
        "min_alerts_per_episode": ab_min,
        "max_alerts_per_episode": ab_max,
        "alerts_distribution": alerts_distribution
    }

def run_alert_burden_analysis(
    evaluator,
    df_tb: pd.DataFrame,
    frozen_thresholds: Dict[str, Any],
    max_k: int = 30
) -> Dict[str, Any]:
    """
    Executes full Gate 6.3 alert burden analysis across baseline models.
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
        ab_stats = compute_alert_burden_for_model(df_test, prob_test, frozen_thresh)
        ab_stats["frozen_threshold"] = round(float(frozen_thresh), 4)

        results[m_id] = ab_stats

    return {
        "horizon_k": max_k,
        "target_far": evaluator.target_far,
        "alert_burden": results
    }

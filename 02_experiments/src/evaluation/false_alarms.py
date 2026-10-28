"""
AIRE-Trace Gate 6.2 False Alarms Analysis Module
Identifies alerts occurring on successful episodes (eventual_outcome == 0).
Reports false alarm statistics per model without modifying primary evaluation outputs.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any

def compute_false_alarms_for_model(
    df_test: pd.DataFrame,
    y_prob: np.ndarray,
    threshold: float
) -> Dict[str, Any]:
    """
    Computes false alarm statistics for a single model at specified threshold.
    
    False alarm condition:
    eventual_outcome == 0 AND y_prob >= threshold.
    """
    df_tmp = df_test[["episode_id", "prefix_len", "eventual_outcome"]].copy()
    df_tmp["prob"] = y_prob

    # Filter to successful episodes
    success_df = df_tmp[df_tmp["eventual_outcome"] == 0].copy()
    
    success_episodes = success_df["episode_id"].unique()
    total_success_episodes = len(success_episodes)
    
    if total_success_episodes == 0:
        return {
            "total_false_alarm_episodes": 0,
            "false_alarm_rate": 0.0,
            "false_alarms_per_episode_min": None,
            "false_alarms_per_episode_max": None,
            "false_alarms_per_episode_mean": None,
            "false_alarms_per_episode_median": None,
            "representative_false_alarm_episodes": []
        }
        
    success_df["is_alert"] = success_df["prob"] >= threshold
    
    # Count alerts per episode
    alert_counts = success_df.groupby("episode_id")["is_alert"].sum()
    
    # False alarm episodes have count >= 1
    false_alarm_eps = alert_counts[alert_counts >= 1]
    total_false_alarm_episodes = int(len(false_alarm_eps))
    
    far = total_false_alarm_episodes / total_success_episodes if total_success_episodes > 0 else 0.0
    
    counts = alert_counts.values
    fa_min = int(np.min(counts))
    fa_max = int(np.max(counts))
    fa_mean = float(np.mean(counts))
    fa_median = float(np.median(counts))
    
    # Representative episode IDs (top 5 with most alerts)
    top_eps = false_alarm_eps.sort_values(ascending=False).head(5).index.tolist()
    top_eps = [str(x) for x in top_eps]

    return {
        "total_false_alarm_episodes": total_false_alarm_episodes,
        "false_alarm_rate": round(far, 4),
        "false_alarms_per_episode_min": fa_min,
        "false_alarms_per_episode_max": fa_max,
        "false_alarms_per_episode_mean": round(fa_mean, 4),
        "false_alarms_per_episode_median": round(fa_median, 4),
        "representative_false_alarm_episodes": top_eps
    }

def run_false_alarms_analysis(
    evaluator,
    df_tb: pd.DataFrame,
    frozen_thresholds: Dict[str, Any],
    max_k: int = 30
) -> Dict[str, Any]:
    """
    Executes full Gate 6.2 false alarms analysis across baseline models.
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
        fa_stats = compute_false_alarms_for_model(df_test, prob_test, frozen_thresh)
        fa_stats["frozen_threshold"] = round(float(frozen_thresh), 4)

        results[m_id] = fa_stats

    return {
        "horizon_k": max_k,
        "target_far": evaluator.target_far,
        "false_alarms": results
    }

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import pandas as pd
from src.api.loaders import (
    get_episodes_df, 
    get_predictions_df, 
    get_late_detections,
    get_thresholds,
    get_alerts
)
from src.api.config import EXPECTED_MODELS

router = APIRouter(prefix="/investigation", tags=["investigation"])

@router.get("/alerts/{model_id}")
def get_alert_investigation(model_id: str):
    if model_id not in EXPECTED_MODELS:
        raise HTTPException(status_code=404, detail="Unknown model ID")
        
    df_ep = get_episodes_df()
    df_pred = get_predictions_df()
    thresholds = get_thresholds()
    
    if df_ep is None or df_pred is None or thresholds is None:
        raise HTTPException(status_code=503, detail="Artifacts not loaded")
        
    m_thresh = thresholds.get(model_id, {}).get("frozen_threshold")
    if m_thresh is None:
        raise HTTPException(status_code=500, detail="Threshold missing for model")
        
    # Get TEST set episodes only
    test_eps = df_ep[df_ep["split"] == "test"].copy()
    test_ep_ids = set(test_eps["episode_id"])
    
    m_preds = df_pred[(df_pred["model_id"] == model_id) & (df_pred["episode_id"].isin(test_ep_ids))].copy()
    m_preds["is_alert"] = m_preds["predicted_probability"] >= m_thresh
    
    alerted_preds = m_preds[m_preds["is_alert"]]
    
    # Calculate first alerts
    if not alerted_preds.empty:
        first_alerts = alerted_preds.loc[alerted_preds.groupby("episode_id")["prefix_len"].idxmin()]
    else:
        first_alerts = pd.DataFrame(columns=["episode_id", "prefix_len"])
        
    total_alerted_episodes = len(first_alerts)
    total_test_episodes = len(test_eps)
    
    distribution = first_alerts["prefix_len"].value_counts().to_dict()
    distribution = {int(k): int(v) for k, v in distribution.items()}
    
    # Derive early/late using identical Gate 6 semantics
    # Only applies to valid annotated failures
    valid_fails = test_eps[
        (test_eps["eventual_outcome"] == 1) & 
        (test_eps["onset_annotated"] == True) & 
        (test_eps["annotation_derived_onset_step"].notna())
    ].copy()
    
    valid_fails["onset_step"] = pd.to_numeric(valid_fails["annotation_derived_onset_step"])
    valid_fail_map = valid_fails.set_index("episode_id")["onset_step"].to_dict()
    
    episodes_list = []
    
    early_count = 0
    late_count = 0
    
    # Align with the alert list cache to match prediction df exact bounds
    for ep_id in test_ep_ids:
        alert_info = get_alerts(ep_id).get(model_id, {})
        first_prefix = alert_info.get("first_alert_prefix")
        alerted = alert_info.get("alerted", False)
        
        timing = "none"
        if alerted and first_prefix is not None:
            if ep_id in valid_fail_map:
                onset = valid_fail_map[ep_id]
                if first_prefix <= onset:
                    timing = "early"
                    early_count += 1
                else:
                    timing = "late"
                    late_count += 1
            else:
                timing = "unannotated_or_success"
                
        episodes_list.append({
            "episode_id": ep_id,
            "first_alert_prefix": first_prefix,
            "alerted": alerted,
            "timing": timing
        })
        
    return {
        "model_id": model_id,
        "total_test_episodes": total_test_episodes,
        "total_alerted_episodes": total_alerted_episodes,
        "episodes_with_no_alert": total_test_episodes - total_alerted_episodes,
        "first_alert_distribution": distribution,
        "early_alerts": early_count,
        "late_alerts": late_count,
        "episodes": sorted(episodes_list, key=lambda x: x["episode_id"])
    }

@router.get("/late-detections")
def get_late_investigation():
    # Return aggregate from gate6 + derived episode list using Gate 6 semantics
    gate6_data = get_late_detections()
    df_ep = get_episodes_df()
    df_pred = get_predictions_df()
    thresholds = get_thresholds()
    
    if not gate6_data or df_ep is None or df_pred is None or thresholds is None:
        raise HTTPException(status_code=503, detail="Artifacts not loaded")
        
    test_eps = df_ep[df_ep["split"] == "test"].copy()
    valid_fails = test_eps[
        (test_eps["eventual_outcome"] == 1) & 
        (test_eps["onset_annotated"] == True) & 
        (test_eps["annotation_derived_onset_step"].notna())
    ].copy()
    valid_fails["onset_step"] = pd.to_numeric(valid_fails["annotation_derived_onset_step"])
    valid_episodes = valid_fails["episode_id"].unique()
    
    enriched_results = {}
    gate6_stats = gate6_data.get("late_detections", {})
    
    for m_id in EXPECTED_MODELS:
        m_stats = gate6_stats.get(m_id, {})
        m_thresh = thresholds.get(m_id, {}).get("frozen_threshold")
        
        # Derive only_late_episodes using exact Gate 6 logic
        if m_thresh is not None:
            df_tmp = valid_fails.copy()
            m_preds = df_pred[(df_pred["model_id"] == m_id) & (df_pred["episode_id"].isin(valid_episodes))].copy()
            # Merge predictions
            merged = pd.merge(df_tmp, m_preds, on="episode_id")
            
            merged["is_alert"] = merged["predicted_probability"] >= m_thresh
            merged["is_early"] = merged["is_alert"] & (merged["prefix_len"] <= merged["onset_step"])
            merged["is_late"] = merged["is_alert"] & (merged["prefix_len"] > merged["onset_step"])
            
            ep_summary = merged.groupby("episode_id").agg(
                has_early=("is_early", "any"),
                has_late=("is_late", "any")
            ).reindex(valid_episodes, fill_value=False)
            
            ep_summary["only_late"] = ep_summary["has_late"] & (~ep_summary["has_early"])
            only_late_eps = ep_summary[ep_summary["only_late"]].index.tolist()
        else:
            only_late_eps = []
            
        enriched_results[m_id] = {
            "stats": m_stats,
            "only_late_episodes": sorted(only_late_eps)
        }
        
    return {
        "horizon_k": gate6_data.get("horizon_k"),
        "target_far": gate6_data.get("target_far"),
        "models": enriched_results
    }

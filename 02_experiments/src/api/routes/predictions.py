from fastapi import APIRouter, HTTPException
from typing import List, Dict
from src.api.loaders import get_predictions_df, get_thresholds, get_episodes_df, get_alerts
from src.api.config import EXPECTED_MODELS, HORIZON_K
from src.api.schemas import EpisodePredictionsResponse, ModelPredictions, PredictionRow, AlertResponse

router = APIRouter()

def _check_episode_validity(episode_id: str):
    df_ep = get_episodes_df()
    if df_ep is None:
        raise HTTPException(status_code=503, detail="Artifacts not loaded")
        
    ep = df_ep[(df_ep["episode_id"] == episode_id) & (df_ep["split"] == "test")]
    if ep.empty:
        raise HTTPException(status_code=404, detail="Episode not found or not in canonical TEST set")

@router.get("/episodes/{episode_id}/predictions", response_model=EpisodePredictionsResponse)
def get_episode_predictions(episode_id: str):
    _check_episode_validity(episode_id)
        
    df_preds = get_predictions_df()
    if df_preds is None:
        raise HTTPException(status_code=503, detail="Artifacts not loaded")
        
    ep_preds = df_preds[df_preds["episode_id"] == episode_id]
    if ep_preds.empty:
        raise HTTPException(status_code=404, detail="No predictions found for this episode")
        
    thresholds = get_thresholds()
    
    models_dict = {}
    for m_id in EXPECTED_MODELS:
        m_df = ep_preds[ep_preds["model_id"] == m_id].sort_values("prefix_len")
        preds_list = [
            PredictionRow(prefix_len=row["prefix_len"], probability=row["predicted_probability"]) 
            for _, row in m_df.iterrows()
        ]
        models_dict[m_id] = ModelPredictions(
            threshold=thresholds[m_id]["frozen_threshold"],
            predictions=preds_list
        )
        
    return EpisodePredictionsResponse(
        episode_id=episode_id,
        horizon_k=HORIZON_K,
        models=models_dict
    )

@router.get("/episodes/{episode_id}/alerts", response_model=List[AlertResponse])
def get_episode_alerts(episode_id: str):
    _check_episode_validity(episode_id)
    alerts = get_alerts(episode_id)
    if not alerts:
        raise HTTPException(status_code=404, detail="No predictions/alerts found for this episode")
        
    results = []
    for m_id in EXPECTED_MODELS:
        data = alerts[m_id]
        results.append(AlertResponse(
            model=m_id,
            first_alert_prefix=data["first_alert_prefix"],
            alerted=data["alerted"],
            threshold=data["threshold"]
        ))
    return results

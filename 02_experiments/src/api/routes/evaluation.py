from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from src.api.loaders import get_primary_results, get_pdc_summary, get_late_detections, get_thresholds, get_significance
from src.api.config import EXPECTED_MODELS

router = APIRouter()

@router.get("/models")
def list_models():
    primary = get_primary_results()
    thresholds = get_thresholds()
    if not primary or not thresholds:
        raise HTTPException(status_code=503, detail="Artifacts not loaded")
        
    models_info = []
    mode_a = primary.get("mode_a_terminalbench_test", {})
    sig = get_significance()
    for m_id in EXPECTED_MODELS:
        m_stats = mode_a.get(m_id, {})
        m_thresh = thresholds.get(m_id, {}).get("frozen_threshold")
        if m_id == "dyn_comp" and sig:
            models_info.append({
                "model_id": m_id,
                "frozen_threshold": m_thresh,
                "auroc": None,
                "auprc": None,
                "far": sig.get("obs_dyn_far"),
                "recall_at_far": sig.get("obs_dyn_recall")
            })
        else:
            models_info.append({
                "model_id": m_id,
                "frozen_threshold": m_thresh,
                "auroc": m_stats.get("AUROC"),
                "auprc": m_stats.get("AUPRC"),
                "far": m_stats.get("FAR"),
                "recall_at_far": m_stats.get("Recall_at_FAR")
            })
    return models_info

@router.get("/evaluation/summary")
def get_eval_summary():
    primary = get_primary_results()
    if not primary:
        raise HTTPException(status_code=503, detail="Artifacts not loaded")
    return primary.get("mode_a_terminalbench_test", {})

@router.get("/evaluation/pdc")
def get_pdc():
    pdc = get_pdc_summary()
    if not pdc:
        raise HTTPException(status_code=503, detail="Artifacts not loaded")
    return pdc

@router.get("/evaluation/late-detections")
def get_late_detect():
    late = get_late_detections()
    if not late:
        raise HTTPException(status_code=503, detail="Artifacts not loaded")
    return late

@router.get("/evaluation/significance")
def get_signif():
    sig = get_significance()
    if not sig:
        raise HTTPException(status_code=503, detail="Artifacts not loaded")
    return sig

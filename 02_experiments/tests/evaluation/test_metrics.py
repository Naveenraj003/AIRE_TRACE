import pytest
import pandas as pd
import numpy as np
from src.evaluation.metrics import (
    compute_sample_weights,
    compute_weighted_auroc,
    compute_weighted_auprc,
    compute_weighted_brier,
    compute_weighted_ece,
    compute_all_metrics
)

def test_metrics():
    df = pd.DataFrame({
        "episode_id": ["ep1", "ep1", "ep2", "ep2"],
        "total_steps": [10, 10, 20, 20],
        "prefix_len": [1, 2, 1, 2],
        "eventual_outcome": [0, 0, 1, 1],
        "onset_annotated": [False, False, True, True],
        "annotation_derived_onset_step": [None, None, 2, 2]
    })
    y_prob = np.array([0.1, 0.2, 0.7, 0.9])
    
    weights = compute_sample_weights(df, max_k=30)
    assert np.allclose(weights, [1/10, 1/10, 1/20, 1/20])
    
    auroc = compute_weighted_auroc(df["eventual_outcome"].values, y_prob, weights)
    assert auroc == 1.0
    
    m_dict = compute_all_metrics(df, y_prob, threshold=0.5, mode="prospective")
    assert "AUROC" in m_dict
    assert "AUPRC" in m_dict
    assert "Recall_at_FAR" in m_dict
    assert "FAR" in m_dict
    assert "Brier" in m_dict
    assert "ECE" in m_dict

    m_dict_raw = compute_all_metrics(df, y_prob, threshold=0.5, mode="raw")
    assert "Raw_Recall" in m_dict_raw
    assert "Recall_at_FAR" not in m_dict_raw

def test_recall_at_far_calibration_failure():
    df = pd.DataFrame({
        "episode_id": ["ep1", "ep2"],
        "total_steps": [10, 20],
        "prefix_len": [1, 2],
        "eventual_outcome": [0, 1],
        "onset_annotated": [False, True],
        "annotation_derived_onset_step": [None, 2]
    })
    y_prob = np.array([0.1, 0.9])
    
    m_dict_fail = compute_all_metrics(
        df, y_prob, threshold=0.5, mode="prospective", 
        calibration_far=0.10, target_far=0.05
    )
    assert np.isnan(m_dict_fail["Recall_at_FAR"])


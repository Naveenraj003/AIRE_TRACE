"""
Tests for Gate 6.3 Alert Burden Analysis Module.
Ensures frozen thresholds are used, no calibration occurs, and outputs are correct.
"""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import MagicMock, patch
from src.evaluation.alert_burden import (
    compute_alert_burden_for_model,
    run_alert_burden_analysis
)
from src.evaluation.evaluator import MasterEvaluator

def test_compute_alert_burden_for_model():
    """Test alert burden calculation across episodes."""
    df_test = pd.DataFrame({
        "episode_id": ["E1", "E1", "E2", "E2", "E3", "E4"],
        "prefix_len": [1, 2, 1, 2, 1, 1],
    })
    
    # E1: 2 alerts
    # E2: 1 alert
    # E3: 1 alert
    # E4: 0 alerts
    y_prob = np.array([0.8, 0.9, 0.2, 0.6, 0.9, 0.1])
    threshold = 0.5
    
    stats = compute_alert_burden_for_model(df_test, y_prob, threshold)
    
    assert stats["total_alerts"] == 4
    
    assert stats["min_alerts_per_episode"] == 0
    assert stats["max_alerts_per_episode"] == 2
    assert stats["mean_alerts_per_episode"] == 1.0  # (2 + 1 + 1 + 0) / 4
    assert stats["median_alerts_per_episode"] == 1.0  # middle of 0, 1, 1, 2
    
    # Distribution check
    assert stats["alerts_distribution"] == {
        "0": 1,
        "1": 2,
        "2": 1
    }

def test_run_alert_burden_analysis_frozen_thresholds():
    """Ensure run_alert_burden_analysis uses frozen thresholds and doesn't calibrate."""
    df_tb = pd.DataFrame({
        "episode_id": ["E1", "E2"],
        "prefix_len": [1, 2],
        "split": ["train", "test"],
        "eventual_outcome": [1, 1], # dummy variable needed for _prepare_fitted_models
        "feat_1": [0.1, 0.2]
    })
    
    frozen_thresholds = {
        "H1": {"frozen_threshold": 0.55},
        "M1": 0.65
    }
    
    evaluator = MasterEvaluator(target_far=0.05)
    
    # Mock _prepare_fitted_models to return dummy models
    mock_model_h1 = MagicMock()
    mock_model_h1.predict_proba.return_value = np.array([0.6]) # 1 test instance
    
    mock_model_m1 = MagicMock()
    mock_model_m1.predict_proba.return_value = np.array([0.7])
    
    evaluator._prepare_fitted_models = MagicMock(return_value={
        "H1": mock_model_h1,
        "M1": mock_model_m1
    })
    
    # We explicitly patch select_calibration_threshold to ensure it is NOT called
    with patch("src.evaluation.evaluator.select_calibration_threshold") as mock_calibrate:
        results = run_alert_burden_analysis(evaluator, df_tb, frozen_thresholds, max_k=30)
        
        # Ensure select_calibration_threshold is never called
        mock_calibrate.assert_not_called()
    
    assert "alert_burden" in results
    assert "H1" in results["alert_burden"]
    assert "M1" in results["alert_burden"]
    
    # Verify H1 threshold
    assert results["alert_burden"]["H1"]["frozen_threshold"] == 0.55
    # Verify M1 threshold
    assert results["alert_burden"]["M1"]["frozen_threshold"] == 0.65

"""
Tests for Gate 6.2 False Alarms Analysis Module.
Ensures frozen thresholds are used, no calibration occurs, and outputs are correct.
"""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import MagicMock, patch
from src.evaluation.false_alarms import (
    compute_false_alarms_for_model,
    run_false_alarms_analysis
)
from src.evaluation.evaluator import MasterEvaluator

def test_compute_false_alarms_for_model_success():
    """Test false alarm counting for successful episodes."""
    df_test = pd.DataFrame({
        "episode_id": ["E1", "E1", "E2", "E2", "E3", "E4"],
        "prefix_len": [1, 2, 1, 2, 1, 1],
        "eventual_outcome": [0, 0, 0, 0, 1, 0] # E3 is a failure, should be ignored
    })
    
    # E1 has alerts at prefix 1 and 2
    # E2 has alert at prefix 2
    # E3 is failure
    # E4 has no alerts
    y_prob = np.array([0.8, 0.9, 0.2, 0.6, 0.9, 0.1])
    threshold = 0.5
    
    stats = compute_false_alarms_for_model(df_test, y_prob, threshold)
    
    # Total successful episodes = E1, E2, E4 (3 episodes)
    # Total false alarm episodes = E1, E2 (2 episodes)
    assert stats["total_false_alarm_episodes"] == 2
    assert stats["false_alarm_rate"] == round(2 / 3, 4)
    
    # Alerts counts: E1: 2, E2: 1, E4: 0
    assert stats["false_alarms_per_episode_min"] == 0
    assert stats["false_alarms_per_episode_max"] == 2
    assert stats["false_alarms_per_episode_mean"] == 1.0 # (2+1+0)/3
    assert stats["false_alarms_per_episode_median"] == 1.0 # middle of 0, 1, 2
    
    # Representative episodes should include E1, E2 in order of counts
    assert stats["representative_false_alarm_episodes"] == ["E1", "E2"]

def test_run_false_alarms_analysis_frozen_thresholds():
    """Ensure run_false_alarms_analysis uses frozen thresholds and doesn't calibrate."""
    df_tb = pd.DataFrame({
        "episode_id": ["E1", "E2"],
        "prefix_len": [1, 2],
        "eventual_outcome": [0, 0],
        "split": ["train", "test"],
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
        results = run_false_alarms_analysis(evaluator, df_tb, frozen_thresholds, max_k=30)
        
        # Ensure select_calibration_threshold is never called
        mock_calibrate.assert_not_called()
    
    assert "false_alarms" in results
    assert "H1" in results["false_alarms"]
    assert "M1" in results["false_alarms"]
    
    # Verify H1 threshold
    assert results["false_alarms"]["H1"]["frozen_threshold"] == 0.55
    # Verify M1 threshold
    assert results["false_alarms"]["M1"]["frozen_threshold"] == 0.65

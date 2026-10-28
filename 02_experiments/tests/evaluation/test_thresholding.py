import pytest
import pandas as pd
import numpy as np
from src.evaluation.thresholding import select_calibration_threshold, compute_episode_far_and_recall

def test_threshold_selection():
    df = pd.DataFrame({
        "episode_id": ["ep1", "ep1", "ep2", "ep2", "ep3", "ep3"],
        "total_steps": [5, 5, 5, 5, 5, 5],
        "prefix_len": [1, 2, 1, 2, 1, 2],
        "eventual_outcome": [0, 0, 1, 1, 1, 1], # 1 succ, 2 fail
        "onset_annotated": [False, False, True, True, True, True],
        "annotation_derived_onset_step": [None, None, 2, 2, 2, 2]
    })
    y_prob = np.array([0.02, 0.04, 0.6, 0.8, 0.7, 0.9])
    
    thresh_info = select_calibration_threshold(df, y_prob, target_far=0.05)
    assert "frozen_threshold" in thresh_info
    assert thresh_info["calibration_far"] <= 0.05
    assert thresh_info["calibration_recall"] == 1.0

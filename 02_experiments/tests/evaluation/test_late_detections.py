import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
from src.evaluation.late_detections import compute_late_detections_for_model, run_late_detections_analysis
from src.evaluation.evaluator import MasterEvaluator

def test_compute_late_detections_basic():
    # Setup test dataframe with 2 valid failure episodes (ep_fail1, ep_fail2) and 1 success episode (ep_succ)
    # ep_fail1: onset at step 2. Prefixes at step 1, 2, 3.
    # ep_fail2: onset at step 1. Prefixes at step 1, 2.
    df_test = pd.DataFrame({
        "episode_id": ["ep_succ", "ep_succ", "ep_fail1", "ep_fail1", "ep_fail1", "ep_fail2", "ep_fail2"],
        "prefix_len": [1, 2, 1, 2, 3, 1, 2],
        "eventual_outcome": [0, 0, 1, 1, 1, 1, 1],
        "onset_annotated": [False, False, True, True, True, True, True],
        "annotation_derived_onset_step": [None, None, 2, 2, 2, 1, 1]
    })

    # Probabilities:
    # ep_succ: 0.1, 0.2 (no alert at threshold 0.5)
    # ep_fail1: step 1 (0.6 - early alert), step 2 (0.7 - onset alert), step 3 (0.8 - late alert, lateness = 3 - 2 = 1)
    # ep_fail2: step 1 (0.3 - no alert), step 2 (0.9 - late alert, lateness = 2 - 1 = 1) -> ONLY LATE alert
    y_prob = np.array([0.1, 0.2, 0.6, 0.7, 0.8, 0.3, 0.9])
    threshold = 0.5

    res = compute_late_detections_for_model(df_test, y_prob, threshold)

    assert res["total_late_alerts"] == 2
    assert res["unique_late_alert_episodes"] == 2
    assert res["total_valid_fail_episodes"] == 2
    assert res["only_late_alert_episodes"] == 1  # ep_fail2 had only late alert
    assert res["pct_failed_episodes_with_only_late_alerts"] == 50.0
    assert res["lateness_min"] == 1.0
    assert res["lateness_max"] == 1.0
    assert res["lateness_mean"] == 1.0
    assert res["lateness_median"] == 1.0

def test_compute_late_detections_no_late_alerts():
    df_test = pd.DataFrame({
        "episode_id": ["ep_fail1", "ep_fail1"],
        "prefix_len": [1, 2],
        "eventual_outcome": [1, 1],
        "onset_annotated": [True, True],
        "annotation_derived_onset_step": [2, 2]
    })
    y_prob = np.array([0.6, 0.1])
    threshold = 0.5

    res = compute_late_detections_for_model(df_test, y_prob, threshold)

    assert res["total_late_alerts"] == 0
    assert res["unique_late_alert_episodes"] == 0
    assert res["total_valid_fail_episodes"] == 1
    assert res["only_late_alert_episodes"] == 0
    assert res["pct_failed_episodes_with_only_late_alerts"] == 0.0
    assert res["lateness_min"] is None
    assert res["lateness_mean"] is None

def test_gate6_reads_frozen_thresholds_and_never_invokes_calibration():
    """Regression test verifying Gate 6 loads frozen thresholds and NEVER calls select_calibration_threshold()."""
    df_tb = pd.DataFrame({
        "dataset_id": ["tb", "tb", "tb", "tb"],
        "episode_id": ["ep0", "ep1", "ep1", "ep1"],
        "split": ["train", "train", "test", "test"],
        "prefix_len": [1, 1, 1, 2],
        "total_steps": [2, 2, 2, 2],
        "eventual_outcome": [0, 1, 1, 1],
        "onset_annotated": [False, True, True, True],
        "annotation_derived_onset_step": [None, 1, 1, 1],
        "feat_tool_error_count": [0, 1, 0, 1],
        "feat_retry_count": [0, 0, 0, 1],
        "feat_repeated_action_last2": [0, 0, 0, 0]
    })

    frozen_thresholds = {
        "H1": {"frozen_threshold": 0.74},
        "H2": {"frozen_threshold": 0.53},
        "H3": {"frozen_threshold": 0.01},
        "H4": {"frozen_threshold": 0.99},
        "M1": {"frozen_threshold": 0.98},
        "S1": {"frozen_threshold": 0.92},
        "S2": {"frozen_threshold": 0.95}
    }

    evaluator = MasterEvaluator(target_far=0.05)

    with patch("src.evaluation.thresholding.select_calibration_threshold") as mock_calib:
        results = run_late_detections_analysis(evaluator, df_tb, frozen_thresholds, max_k=30)
        mock_calib.assert_not_called()

    assert "late_detections" in results
    assert results["late_detections"]["H1"]["frozen_threshold"] == 0.74

import pytest
import pandas as pd
import numpy as np
from src.evaluation.bootstrap import compute_episode_bootstrap_ci

def test_episode_bootstrap():
    df = pd.DataFrame({
        "episode_id": ["ep1", "ep1", "ep2", "ep2", "ep3", "ep3"],
        "total_steps": [5, 5, 5, 5, 5, 5],
        "prefix_len": [1, 2, 1, 2, 1, 2],
        "eventual_outcome": [0, 0, 1, 1, 1, 1],
        "onset_annotated": [False, False, True, True, True, True],
        "annotation_derived_onset_step": [None, None, 2, 2, 2, 2]
    })
    y_prob = np.array([0.02, 0.04, 0.6, 0.8, 0.7, 0.9])
    
    ci_res = compute_episode_bootstrap_ci(df, y_prob, threshold=0.5, n_iterations=50, random_seed=42)
    assert "AUROC" in ci_res
    assert "mean" in ci_res["AUROC"]
    assert "ci_lower" in ci_res["AUROC"]
    assert "ci_upper" in ci_res["AUROC"]

import numpy as np
import pandas as pd
import pytest
from src.evaluation.statistical_testing import compute_paired_bootstrap_test

def test_compute_paired_bootstrap_test_identity():
    # Mock data
    np.random.seed(42)
    episodes = [1, 1, 2, 2, 3, 3]
    outcomes = [1, 1, 0, 0, 1, 1]
    
    df_prefixes = pd.DataFrame({
        "episode_id": episodes,
        "eventual_outcome": outcomes,
        "total_steps": [2, 2, 2, 2, 2, 2]
    })
    
    # Identical predictions
    preds = np.array([0.9, 0.8, 0.1, 0.2, 0.6, 0.7])
    
    predictions = {
        "S1": preds,
        "M1": preds,
        "S2": preds,
        "H1": preds,
        "H2": preds,
        "H3": preds,
        "H4": preds
    }
    
    results = compute_paired_bootstrap_test(
        df_prefixes, predictions, 
        base_model="S1", 
        comparators=["M1", "S2", "H1", "H2", "H3", "H4"],
        n_iterations=5, # Small N for speed
        random_seed=42,
        max_k=30
    )
    
    # Check all 6 exist for AUROC and AUPRC (12 total)
    assert len(results) == 12
    
    auroc_res = [r for r in results if r["metric"] == "AUROC"]
    assert len(auroc_res) == 6
    
    for r in results:
        # Delta obs must be 0
        assert np.isclose(r["delta_obs"], 0.0)
        # Bootstrap mean delta must be 0
        assert np.isclose(r["bootstrap_mean_delta"], 0.0)
        # Raw p-value for exactly equal vectors will evaluate to 1.0 because |Delta_b_0| = 0, |Delta_obs| = 0.
        # Actually it's (1 + B) / (B + 1) = 1.0
        assert r["p_raw"] == 1.0
        assert r["p_adj"] == 1.0
        assert not r["reject_H0"]

def test_holm_bonferroni_properties():
    # We can mock the raw p-values by supplying different predictions
    np.random.seed(42)
    episodes = np.repeat(np.arange(10), 5)
    outcomes = np.repeat(np.random.randint(0, 2, 10), 5)
    
    df_prefixes = pd.DataFrame({
        "episode_id": episodes,
        "eventual_outcome": outcomes,
        "total_steps": np.repeat(5, 50)
    })
    
    predictions = {"S1": np.random.rand(50)}
    comparators = ["C1", "C2", "C3", "C4", "C5", "C6"]
    for c in comparators:
        predictions[c] = np.random.rand(50)
        
    results = compute_paired_bootstrap_test(
        df_prefixes, predictions, 
        base_model="S1", 
        comparators=comparators,
        n_iterations=50,
        random_seed=42
    )
    
    for metric in ["AUROC", "AUPRC"]:
        metric_results = [r for r in results if r["metric"] == metric]
        
        # Sort manually by p_raw
        metric_results.sort(key=lambda x: x["p_raw"])
        
        prev_adj = -1.0
        for i, r in enumerate(metric_results):
            p_raw = r["p_raw"]
            p_adj = r["p_adj"]
            
            # Adjusted >= Raw
            assert p_adj >= p_raw
            
            # Monotonicity
            assert p_adj >= prev_adj
            prev_adj = p_adj
            
            # Cap at 1.0
            assert p_adj <= 1.0

def test_compute_paired_bootstrap_test_recall_at_far():
    np.random.seed(42)
    # 4 episodes: 2 success (0), 2 valid failure (1)
    episodes = [1, 1, 2, 2, 3, 3, 4, 4]
    outcomes = [0, 0, 0, 0, 1, 1, 1, 1]
    prefix_lens = [1, 2, 1, 2, 1, 2, 1, 2]
    onset_annot = [False, False, False, False, True, True, True, True]
    onset_steps = [np.nan, np.nan, np.nan, np.nan, 2, 2, 2, 2]
    
    df_prefixes = pd.DataFrame({
        "episode_id": episodes,
        "eventual_outcome": outcomes,
        "prefix_len": prefix_lens,
        "onset_annotated": onset_annot,
        "annotation_derived_onset_step": onset_steps,
    })
    
    preds_s1 = np.array([0.1, 0.2, 0.3, 0.4, 0.7, 0.8, 0.2, 0.3])
    preds_m1 = np.array([0.1, 0.2, 0.3, 0.4, 0.7, 0.8, 0.2, 0.3])
    
    predictions = {
        "S1": preds_s1,
        "M1": preds_m1
    }
    thresholds = {
        "S1": 0.5,
        "M1": 0.5
    }
    
    # Missing threshold check
    with pytest.raises(ValueError, match="thresholds dict"):
        compute_paired_bootstrap_test(
            df_prefixes, predictions,
            base_model="S1",
            comparators=["M1"],
            metrics=["Recall_at_FAR"],
            thresholds=None
        )
        
    results = compute_paired_bootstrap_test(
        df_prefixes, predictions,
        base_model="S1",
        comparators=["M1"],
        metrics=["Recall_at_FAR"],
        thresholds=thresholds,
        n_iterations=20,
        random_seed=42
    )
    
    assert len(results) == 1
    res = results[0]
    assert res["metric"] == "Recall_at_FAR"
    assert np.isclose(res["delta_obs"], 0.0)
    assert np.isclose(res["bootstrap_mean_delta"], 0.0)
    assert res["p_raw"] == 1.0
    assert not res["reject_H0"]
    assert "ci_lower_95" in res
    assert "ci_upper_95" in res
    assert "diagnostics" in res
    assert len(res["diagnostics"]["base_bootstrap_fars"]) == 20
    assert len(res["diagnostics"]["comp_bootstrap_fars"]) == 20

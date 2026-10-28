import pytest
import pandas as pd
import json
from pathlib import Path
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = REPO_ROOT / "results" / "baseline_runs"

DYN_COMP_PREDS = RESULTS_DIR / "dyn_comp_predictions_k30.parquet"
DYN_COMP_THRESH = RESULTS_DIR / "dyn_comp_threshold_k30.json"
SIGNIFICANCE_JSON = RESULTS_DIR / "dyn_comp_vs_m1_bootstrap_k30_v2_B10000.json"
PDC_JSON = RESULTS_DIR / "pdc_summary.json"
EPISODES_JSON = REPO_ROOT / "repaired_636_canonical.json"

@pytest.fixture(scope="module")
def dyn_comp_artifacts():
    return {
        "preds": pd.read_parquet(DYN_COMP_PREDS),
        "thresh": json.loads(DYN_COMP_THRESH.read_text(encoding="utf-8")),
        "sig": json.loads(SIGNIFICANCE_JSON.read_text(encoding="utf-8")),
        "pdc": json.loads(PDC_JSON.read_text(encoding="utf-8")),
        "episodes": json.loads(EPISODES_JSON.read_text(encoding="utf-8"))["episodes"]
    }

def test_dyn_comp_score_preservation(dyn_comp_artifacts):
    df = dyn_comp_artifacts["preds"]
    test_ep = df["episode_id"].iloc[0]
    raw_val = df[(df["episode_id"] == test_ep) & (df["prefix_len"] == 1)].iloc[0]["dyn_comp"]
    
    with client:
        res = client.get(f"/api/episodes/{test_ep}/predictions")
        assert res.status_code == 200
        models = res.json()["models"]
        assert "dyn_comp" in models
        api_preds = models["dyn_comp"]["predictions"]
        api_val = next(p["probability"] for p in api_preds if p["prefix_len"] == 1)
        
        assert raw_val == api_val, "API did not perfectly preserve the raw unnormalized dyn_comp score."

def test_dyn_comp_alert_parity(dyn_comp_artifacts):
    df = dyn_comp_artifacts["preds"]
    thresh = dyn_comp_artifacts["thresh"]["dyn_comp_frozen_threshold"]
    
    # Find an episode that crosses the threshold
    alerted_df = df[df["dyn_comp"] >= thresh]
    assert not alerted_df.empty, "No alerts found in artifact!"
    
    test_ep = alerted_df["episode_id"].iloc[0]
    
    # Raw artifact calculation
    ep_df = df[df["episode_id"] == test_ep].sort_values("prefix_len")
    first_alert_prefix = ep_df[ep_df["dyn_comp"] >= thresh]["prefix_len"].min()
    
    # API calculation
    with client:
        res = client.get(f"/api/episodes/{test_ep}/alerts")
        assert res.status_code == 200
        alerts = res.json()
        dyn_alert = next(a for a in alerts if a["model"] == "dyn_comp")
        
        assert dyn_alert["alerted"] is True
        assert dyn_alert["first_alert_prefix"] == first_alert_prefix
        assert dyn_alert["threshold"] == thresh

def test_dyn_comp_significance_endpoint(dyn_comp_artifacts):
    sig = dyn_comp_artifacts["sig"]
    
    with client:
        res = client.get("/api/evaluation/significance")
        assert res.status_code == 200
        api_sig = res.json()
        
        assert api_sig["obs_diff_dyn_minus_m1"] == sig["obs_diff_dyn_minus_m1"]
        assert api_sig["obs_diff_dyn_minus_m1"] == 0.1089
        
        assert api_sig["ci_lower_95"] == sig["ci_lower_95"]
        assert api_sig["ci_lower_95"] == 0.0706
        
        assert api_sig["ci_upper_95"] == sig["ci_upper_95"]
        assert api_sig["ci_upper_95"] == 0.1496
        
        assert api_sig["p_adj"] == sig["p_adj"]
        assert api_sig["p_adj"] == pytest.approx(9.999e-05)
        
        assert api_sig["B"] == sig["B"]
        assert api_sig["B"] == 10000

def test_pdc_endpoint(dyn_comp_artifacts):
    pdc = dyn_comp_artifacts["pdc"]
    
    with client:
        res = client.get("/api/evaluation/pdc")
        assert res.status_code == 200
        api_pdc = res.json()
        
        assert "overall_pdc" in api_pdc
        assert "overall_pdc_coverage" in api_pdc
        
        assert api_pdc["overall_pdc"] == pdc["overall_pdc"]
        assert api_pdc["overall_pdc_coverage"] == pdc["overall_pdc_coverage"]

def test_dyn_comp_test_only_isolation(dyn_comp_artifacts):
    df = dyn_comp_artifacts["preds"]
    
    with client:
        res = client.get("/api/episodes")
        api_eps = res.json()
        api_ep_ids = {e["episode_id"] for e in api_eps}
        
        # Verify all dyn_comp parquet episode IDs are present in the API's episode list (which is strictly TEST split)
        dyn_ep_ids = set(df["episode_id"].unique())
        
        assert dyn_ep_ids.issubset(api_ep_ids), "dyn_comp predictions contain episode IDs not in the canonical API TEST set"

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.api.app import app
from src.api.loaders import get_primary_results, get_late_detections, get_alerts, get_episodes_df

# Needs lifespan to run
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_no_evaluation_imports():
    """Test 1 - No evaluation imports in API (Static Check)"""
    # Use static checking like test_architectural_imports to avoid pytest collection artifacts
    route_file = os.path.join(os.path.dirname(__file__), '../../src/api/routes/investigation.py')
    with open(route_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "src.evaluation" not in content, "investigation.py must not import src.evaluation"
    assert "src.baselines" not in content, "investigation.py must not import src.baselines"

def test_investigation_unknown_model(client):
    """Test 3 - Model validation"""
    res = client.get("/api/investigation/alerts/UNKNOWN")
    assert res.status_code == 404

def test_investigation_test_split_only(client):
    """Test 4 - Episode consistency (TEST split only)"""
    res = client.get("/api/investigation/alerts/S1")
    assert res.status_code == 200
    data = res.json()
    
    # All episodes must be from TEST split
    df_ep = get_episodes_df()
    test_eps = set(df_ep[df_ep["split"] == "test"]["episode_id"])
    
    returned_eps = [ep["episode_id"] for ep in data["episodes"]]
    for ep_id in returned_eps:
        assert ep_id in test_eps, f"Episode {ep_id} is not in canonical TEST split"

def test_first_alert_correctness(client):
    """Test 5 - First-alert correctness"""
    res = client.get("/api/investigation/alerts/S1")
    data = res.json()
    
    # Find one that alerted
    alerted_eps = [ep for ep in data["episodes"] if ep["alerted"]]
    if alerted_eps:
        ep = alerted_eps[0]
        ep_id = ep["episode_id"]
        reported_prefix = ep["first_alert_prefix"]
        
        # Verify against loaders cache
        alert_info = get_alerts(ep_id).get("S1")
        assert alert_info is not None
        assert alert_info["first_alert_prefix"] == reported_prefix

def test_gate6_consistency(client):
    """Test 7 - Gate 6 consistency"""
    res = client.get("/api/investigation/late-detections")
    assert res.status_code == 200
    data = res.json()
    
    # Verify aggregate values match exactly what's in gate6 JSON
    frozen_gate6 = get_late_detections()
    
    assert data["horizon_k"] == frozen_gate6["horizon_k"]
    
    frozen_stats = frozen_gate6.get("late_detections", {})
    
    for m_id, m_data in data["models"].items():
        if m_id in frozen_stats:
            assert m_data["stats"]["total_late_alerts"] == frozen_stats[m_id]["total_late_alerts"]
            assert m_data["stats"]["pct_failed_episodes_with_only_late_alerts"] == frozen_stats[m_id]["pct_failed_episodes_with_only_late_alerts"]

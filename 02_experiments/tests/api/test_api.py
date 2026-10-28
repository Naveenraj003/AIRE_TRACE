import pytest
import hashlib
import os
from pathlib import Path
from fastapi.testclient import TestClient
from src.api.app import app

# Create test client
# We use TestClient as a context manager to trigger lifespan events
# See: https://fastapi.tiangolo.com/advanced/testing-events/
client = TestClient(app)

# The artifacts we must protect
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFESTS_DIR = REPO_ROOT / "data" / "processed" / "manifests"
RESULTS_DIR = REPO_ROOT / "results" / "baseline_runs"
REPORTS_DIR = REPO_ROOT / "reports"

ARTIFACTS_TO_HASH = [
    RESULTS_DIR / "primary_k30_results.json",
    RESULTS_DIR / "calibrated_thresholds.json",
    RESULTS_DIR / "pdc_summary.json",
    REPORTS_DIR / "gate6_late_detections.json",
    RESULTS_DIR / "prediction_traces_k30.parquet",
    REPO_ROOT / "repaired_636_canonical.json"
]

def hash_file(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

@pytest.fixture(scope="session", autouse=True)
def immutability_check():
    """
    Ensures that the API tests do not mutate the canonical artifacts.
    Runs before and after all tests.
    """
    pre_hashes = {path.name: hash_file(path) for path in ARTIFACTS_TO_HASH}
    
    yield  # Run tests
    
    post_hashes = {path.name: hash_file(path) for path in ARTIFACTS_TO_HASH}
    for name in pre_hashes:
        assert pre_hashes[name] == post_hashes[name], f"Artifact {name} was MUTATED during API execution!"

def test_architectural_imports():
    """
    Search/import inspection confirms src/api/ has no imports from src.evaluation or src.baselines.
    """
    api_dir = REPO_ROOT / "src" / "api"
    for root, _, files in os.walk(api_dir):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    assert "src.evaluation" not in content, f"Illegal import of src.evaluation found in {file}"
                    assert "src.baselines" not in content, f"Illegal import of src.baselines found in {file}"
                    assert "evaluator" not in content.lower(), f"Suspicious evaluator reference in {file}"

def test_health():
    with client:
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert data["canonical_episodes"] == 636
        assert data["test_episodes"] == 416
        assert data["prediction_rows"] == 62146
        assert data["prediction_prefixes"] == 8878
        assert data["models"] == 7

def test_episodes():
    with client:
        response = client.get("/api/episodes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 416
        
        # Grab a valid episode
        valid_ep = data[0]["episode_id"]
        
        # test GET /api/episodes/{valid}
        res2 = client.get(f"/api/episodes/{valid_ep}")
        assert res2.status_code == 200
        assert res2.json()["episode_id"] == valid_ep

        # test GET /api/episodes/{invalid}
        res3 = client.get("/api/episodes/invalid_episode_id")
        assert res3.status_code == 404

        # test GET /api/episodes/{id}/predictions
        res4 = client.get(f"/api/episodes/{valid_ep}/predictions")
        assert res4.status_code == 200
        pred_data = res4.json()
        assert pred_data["episode_id"] == valid_ep
        assert pred_data["horizon_k"] == 30
        assert len(pred_data["models"]) == 7
        for m_id in ["H1", "H2", "H3", "H4", "M1", "S1", "dyn_comp"]:
            assert m_id in pred_data["models"]
            m_preds = pred_data["models"][m_id]
            assert "threshold" in m_preds
            assert isinstance(m_preds["predictions"], list)

        # test GET /api/episodes/{id}/alerts
        res5 = client.get(f"/api/episodes/{valid_ep}/alerts")
        assert res5.status_code == 200
        alerts = res5.json()
        assert len(alerts) == 7

def test_models():
    with client:
        response = client.get("/api/models")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 7
        model_ids = {m["model_id"] for m in data}
        assert model_ids == {"H1", "H2", "H3", "H4", "M1", "S1", "dyn_comp"}
        assert "frozen_threshold" in data[0]

def test_evaluation_summary():
    with client:
        response = client.get("/api/evaluation/summary")
        assert response.status_code == 200
        data = response.json()
        assert "M1" in data

def test_pdc_summary():
    with client:
        response = client.get("/api/evaluation/pdc")
        assert response.status_code == 200
        data = response.json()
        assert "overall_pdc" in data

def test_late_detections():
    with client:
        response = client.get("/api/evaluation/late-detections")
        assert response.status_code == 200
        data = response.json()
        assert "late_detections" in data

def test_audit_summary():
    with client:
        response = client.get("/api/audit/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["audit_status"] == "recorded"
        assert data["episodes_count"] == 636

def test_frontend_static_serving():
    with client:
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "AIRE-Trace Demo System" in response.text

def test_episode_events():
    with client:
        response = client.get("/api/episodes")
        valid_ep = response.json()[0]["episode_id"]
        
        res2 = client.get(f"/api/episodes/{valid_ep}/events")
        assert res2.status_code == 200
        events = res2.json()
        assert isinstance(events, list)
        if len(events) > 0:
            assert "step_index" in events[0]
            assert "action_type" in events[0]

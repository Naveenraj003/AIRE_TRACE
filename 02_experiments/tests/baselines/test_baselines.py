import pytest
import pandas as pd
import numpy as np
from src.baselines.heuristics import HeuristicMonitor, CombinedHeuristicMonitor
from src.baselines.logistic import LogisticBaseline
from src.baselines.random_forest import RandomForestBaseline
from src.baselines.registry import BaselineRegistry

@pytest.fixture
def dummy_data():
    df = pd.DataFrame({
        "feat_steps_so_far": [1, 2, 3, 1, 2, 3],
        "feat_actor_role_agent": [1, 1, 2, 1, 1, 2],
        "feat_actor_role_tool": [0, 1, 1, 0, 1, 1],
        "feat_actor_role_user": [0, 0, 0, 0, 0, 0],
        "feat_actor_role_system": [0, 0, 0, 0, 0, 0],
        "feat_action_type_message": [1, 0, 1, 1, 0, 1],
        "feat_action_type_tool_call": [0, 1, 1, 0, 1, 1],
        "feat_action_type_tool_res": [0, 1, 1, 0, 1, 1],
        "feat_tool_error_count": [0, 1, 2, 0, 0, 1],
        "feat_retry_count": [0, 1, 2, 0, 0, 0],
        "feat_unique_tools_used": [1, 1, 2, 1, 1, 1],
        "feat_tool_call_ratio": [0.5, 0.5, 0.6, 0.5, 0.5, 0.5],
        "feat_repeated_action_last2": [0, 1, 1, 0, 0, 1]
    })
    y = np.array([0, 1, 1, 0, 0, 1])
    return df, y

def test_heuristic_monitors(dummy_data):
    df, y = dummy_data
    h1 = HeuristicMonitor("H1", "feat_tool_error_count")
    probs1 = h1.predict_proba(df)
    assert len(probs1) == len(df)
    assert np.all((probs1 >= 0.0) & (probs1 <= 1.0))

    h4 = CombinedHeuristicMonitor("H4")
    h4.fit(df, y)
    probs4 = h4.predict_proba(df)
    assert len(probs4) == len(df)
    assert np.all((probs4 >= 0.0) & (probs4 <= 1.0))

def test_logistic_baseline(dummy_data):
    df, y = dummy_data
    m1 = LogisticBaseline("M1")
    m1.fit(df, y)
    probs = m1.predict_proba(df)
    assert len(probs) == len(df)
    assert np.all((probs >= 0.0) & (probs <= 1.0))

def test_random_forest_baseline(dummy_data):
    df, y = dummy_data
    s1 = RandomForestBaseline("S1")
    s1.fit(df, y)
    probs = s1.predict_proba(df)
    assert len(probs) == len(df)
    assert np.all((probs >= 0.0) & (probs <= 1.0))

def test_baseline_registry():
    models = BaselineRegistry.get_baseline_models()
    assert "H1" in models
    assert "H2" in models
    assert "H3" in models
    assert "H4" in models
    assert "M1" in models
    assert "S1" in models
    assert models["L"] == "L_PENDING"

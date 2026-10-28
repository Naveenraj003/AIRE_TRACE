"""
Unit tests for AIRE-Trace SequenceBaseline (S2) model.
"""

import os
import pytest
import numpy as np
import pandas as pd
from src.baselines.sequence import SequenceBaseline
from src.baselines.registry import BaselineRegistry


@pytest.fixture
def sequence_dummy_data():
    """Generates synthetic episode prefix dataframe with temporal structure and variable lengths."""
    rows = []
    # 4 episodes with variable lengths (1 to 4 steps)
    ep_lengths = [3, 1, 4, 2]
    y_labels = [0, 1, 0, 1]
    
    y = []
    for ep, length in enumerate(ep_lengths):
        for step in range(1, length + 1):
            rows.append({
                "episode_id": f"ep_{ep}",
                "prefix_len": step,
                "feat_steps_so_far": step,
                "feat_tool_error_count": step % 2,
                "feat_retry_count": (step - 1) % 2,
                "feat_repeated_action_last2": 0
            })
            y.append(y_labels[ep])
            
    df = pd.DataFrame(rows)
    return df, np.array(y)


def test_sequence_baseline_fit_and_predict(sequence_dummy_data):
    df, y = sequence_dummy_data
    s2 = SequenceBaseline(model_id="S2", epochs=2, batch_size=2)
    s2.fit(df, y)

    assert s2.is_fitted
    probs = s2.predict_proba(df)

    assert isinstance(probs, np.ndarray)
    assert len(probs) == len(df)
    assert np.all((probs >= 0.0) & (probs <= 1.0))


def test_sequence_baseline_index_preservation(sequence_dummy_data):
    df, y = sequence_dummy_data
    s2 = SequenceBaseline(model_id="S2", epochs=2, batch_size=2)
    s2.fit(df, y)

    # Shuffle dataframe rows
    df_shuffled = df.sample(frac=1.0, random_state=42)
    probs_shuffled = s2.predict_proba(df_shuffled)

    assert len(probs_shuffled) == len(df_shuffled)
    assert np.all((probs_shuffled >= 0.0) & (probs_shuffled <= 1.0))

    # Verify predictions align with original indices
    probs_orig = s2.predict_proba(df)
    for orig_pos, orig_idx in enumerate(df_shuffled.index):
        np.testing.assert_allclose(probs_shuffled[orig_pos], probs_orig[orig_idx], atol=1e-5)


def test_sequence_baseline_serialization(sequence_dummy_data, tmp_path):
    df, y = sequence_dummy_data
    s2 = SequenceBaseline(model_id="S2", epochs=2, batch_size=2)
    s2.fit(df, y)

    probs_before = s2.predict_proba(df)

    save_path = os.path.join(tmp_path, "s2_model.pt")
    s2.save(save_path)
    assert os.path.exists(save_path)

    s2_loaded = SequenceBaseline()
    s2_loaded.load(save_path)

    assert s2_loaded.is_fitted
    assert s2_loaded.model_id == "S2"
    probs_after = s2_loaded.predict_proba(df)

    np.testing.assert_allclose(probs_before, probs_after, atol=1e-5)


def test_sequence_baseline_registry():
    models = BaselineRegistry.get_baseline_models()
    assert "S2" in models
    assert isinstance(models["S2"], SequenceBaseline)


def test_sequence_baseline_deterministic_training(sequence_dummy_data):
    df, y = sequence_dummy_data
    s2_1 = SequenceBaseline(model_id="S2", epochs=2, batch_size=2, random_seed=42)
    s2_1.fit(df, y)
    probs_1 = s2_1.predict_proba(df)
    
    s2_2 = SequenceBaseline(model_id="S2", epochs=2, batch_size=2, random_seed=42)
    s2_2.fit(df, y)
    probs_2 = s2_2.predict_proba(df)
    
    np.testing.assert_allclose(probs_1, probs_2, atol=1e-6)

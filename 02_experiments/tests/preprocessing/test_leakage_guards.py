import pytest
from src.leakage.validators import (
    assert_no_task_leakage,
    assert_no_episode_leakage,
    assert_no_feature_leakage,
    assert_valid_checkpoint_horizon,
    assert_unannotated_failures_preserved
)

def test_leakage_guards_pass_valid_data():
    train_tasks = {"t1", "t2"}
    calib_tasks = {"t3"}
    test_tasks = {"t4"}
    assert_no_task_leakage(train_tasks, calib_tasks, test_tasks)

    prefix_rows = [
        {
            "prefix_id": "ep1_p1",
            "prefix_len": 1,
            "total_steps": 10,
            "eventual_outcome": 1,
            "onset_annotated": False,
            "annotation_derived_onset_step": None,
            "feat_steps_so_far": 1.0,
            "feat_retry_count": 0.0
        }
    ]
    assert_no_feature_leakage(prefix_rows)
    assert_valid_checkpoint_horizon(prefix_rows, max_k=30)
    assert_unannotated_failures_preserved(prefix_rows)

def test_leakage_guard_catches_leaked_feature():
    leaked_rows = [
        {
            "prefix_id": "ep1_p1",
            "prefix_len": 1,
            "total_steps": 10,
            "feat_reward": 1.0
        }
    ]
    with pytest.raises(AssertionError):
        assert_no_feature_leakage(leaked_rows)

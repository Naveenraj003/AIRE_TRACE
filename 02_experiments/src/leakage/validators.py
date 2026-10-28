"""
AIRE-Trace Programmatic Leakage Guards & Invariant Validators
Runs before and after dataset preprocessing to guarantee strict protocol compliance.
"""

from typing import Set, List, Dict, Any

FORBIDDEN_FEATURE_KEYS = {
    "reward", "success", "solved", "passed", "final_outcome", "status",
    "incorrect_stages", "annotation_derived_onset_step", "failure_onset_step",
    "incorrect_error_stage_count", "outcome", "is_failed", "is_success"
}

def assert_no_task_leakage(train_tasks: Set[str], calib_tasks: Set[str], test_tasks: Set[str]):
    """Enforces zero task overlap across splits for primary task-group benchmark."""
    tc = train_tasks & calib_tasks
    tt = train_tasks & test_tasks
    ct = calib_tasks & test_tasks
    assert not tc, f"TASK LEAKAGE: Shared tasks in Train & Calib: {tc}"
    assert not tt, f"TASK LEAKAGE: Shared tasks in Train & Test: {tt}"
    assert not ct, f"TASK LEAKAGE: Shared tasks in Calib & Test: {ct}"


def assert_no_episode_leakage(train_episodes: Set[str], calib_episodes: Set[str], test_episodes: Set[str]):
    """Enforces disjoint episode IDs across all splits."""
    ec = train_episodes & calib_episodes
    et = train_episodes & test_episodes
    ct = calib_episodes & test_episodes
    assert not ec, f"EPISODE LEAKAGE: Shared episodes in Train & Calib: {ec}"
    assert not et, f"EPISODE LEAKAGE: Shared episodes in Train & Test: {et}"
    assert not ct, f"EPISODE LEAKAGE: Shared episodes in Calib & Test: {ct}"


def assert_no_feature_leakage(prefix_rows: List[Dict[str, Any]]):
    """Enforces Protocol Rule 2: No forbidden outcome/future keys inside feature dicts."""
    for row in prefix_rows:
        # Features are prefixed with 'feat_' in dictionary representation or stored in 'features'
        feat_dict = {k.replace("feat_", ""): v for k, v in row.items() if k.startswith("feat_")}
        if not feat_dict and "features" in row:
            feat_dict = row["features"]
            
        leaked = FORBIDDEN_FEATURE_KEYS.intersection(feat_dict.keys())
        assert not leaked, f"FEATURE LEAKAGE: Forbidden keys {leaked} in feature vector for prefix {row.get('prefix_id')}"
        
        prefix_len = row.get("prefix_len", 0)
        total_steps = row.get("total_steps", 0)
        assert prefix_len <= total_steps, (
            f"CHRONOLOGY LEAKAGE: prefix_len ({prefix_len}) > total_steps ({total_steps}) "
            f"for prefix {row.get('prefix_id')}"
        )


def assert_valid_checkpoint_horizon(prefix_rows: List[Dict[str, Any]], max_k: int = 30):
    """Enforces checkpoint horizon K <= max_k and no post-terminal padding."""
    for row in prefix_rows:
        prefix_len = row.get("prefix_len", 0)
        total_steps = row.get("total_steps", 0)
        assert prefix_len <= max_k, f"HORIZON VIOLATION: prefix_len {prefix_len} > max_k {max_k}"
        assert prefix_len <= total_steps, f"PADDING VIOLATION: prefix_len {prefix_len} > total_steps {total_steps}"


def assert_unannotated_failures_preserved(prefix_rows: List[Dict[str, Any]]):
    """Enforces Rule 11: Unannotated failures must remain onset_annotated=False and receiving no artificial onset."""
    for row in prefix_rows:
        outcome = row.get("eventual_outcome")
        onset_ann = row.get("onset_annotated")
        onset_step = row.get("annotation_derived_onset_step")
        
        if outcome == 1 and not onset_ann:
            assert onset_step is None or (isinstance(onset_step, float) and float('nan') == onset_step), (
                f"ONSET MUTATION VIOLATION: Unannotated failure received artificial onset step {onset_step}"
            )

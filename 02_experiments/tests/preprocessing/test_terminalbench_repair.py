import pytest
import yaml
import json
from unittest.mock import patch, mock_open
from src.preprocessing.terminalbench import normalize_tracebench_as_terminalbench

def test_provenance_configuration():
    # Test 1 - Provenance
    from pathlib import Path
    cfg_path = Path("02_experiments/configs/data.yaml")
    if not cfg_path.exists():
        cfg_path = Path("configs/data.yaml")
    if not cfg_path.exists():
        cfg_path = Path(__file__).resolve().parent.parent.parent / "configs" / "data.yaml"
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)
    tb_cfg = cfg["datasets"]["terminalbench"]
    assert tb_cfg["hf_repo"] == "Contextbench/Tracebench"
    assert tb_cfg["split"] == "full"
    assert "yoonholee/terminalbench-trajectories" not in json.dumps(cfg)
    assert "tracebench" not in cfg["datasets"]

def test_artifact_resolution_and_failure():
    # Test 2 & 8 - Artifact resolution & Artifact failure
    row = {
        "traj_id": "test_id",
        "task_name": "test_task",
        "artifact_path": "some_invalid_path"
    }
    
    # Missing artifact path should return None
    row_missing = row.copy()
    row_missing["artifact_path"] = None
    ep, evs = normalize_tracebench_as_terminalbench(row_missing, "test_sha")
    assert ep is None
    
    # Invalid artifact path should also fail and return None
    ep, evs = normalize_tracebench_as_terminalbench(row, "test_sha")
    assert ep is None

@patch("src.preprocessing.terminalbench.load_and_parse_artifact")
def test_real_event_reconstruction(mock_load):
    # Test 3 - Real event reconstruction & Tool extraction
    mock_load.return_value = [
        {"role": "user", "content": "initial prompt"},
        {"role": "assistant", "content": "I will run a command\n```bash\nls -la\n```"},
        {"role": "user", "content": "<returncode>0</returncode> output1"}
    ]
    
    row = {"traj_id": "1", "artifact_path": "dummy"}
    ep, evs = normalize_tracebench_as_terminalbench(row, "sha")
    
    assert len(evs) == 2
    
    # Event 1: Initial user prompt
    assert evs[0].step_index == 1
    assert evs[0].actor_role == "user"
    assert evs[0].action_type == "message"
    assert evs[0].tool_name is None
    
    # Event 2: Assistant Action + User Observation turn
    assert evs[1].step_index == 2
    assert evs[1].actor_role == "agent"
    assert evs[1].action_type == "tool_call"
    assert evs[1].tool_name in ["terminal_cmd", "ls"]
    assert evs[1].tool_status == "ok"
    assert evs[1].is_error == 0

@patch("src.preprocessing.terminalbench.load_and_parse_artifact")
def test_onset_extraction(mock_load):
    # Test 4 - Onset extraction
    mock_load.return_value = [
        {"role": "user", "content": "prompt"},
        {"role": "assistant", "content": "action1"},
        {"role": "user", "content": "obs1"},
        {"role": "assistant", "content": "action2"},
        {"role": "user", "content": "obs2"},
        {"role": "assistant", "content": "bad_action"},
        {"role": "user", "content": "obs3"}
    ]

    row = {
        "traj_id": "1",
        "solved": False,
        "incorrect_stages": json.dumps([
            {
                "steps": [
                    {
                        "action_ref": {
                            "content": json.dumps({"role": "assistant", "content": "bad_action"})
                        }
                    }
                ]
            }
        ])
    }
    ep, evs = normalize_tracebench_as_terminalbench(row, "sha")
    assert ep.onset_annotated is True
    assert ep.annotation_derived_onset_step == 4

@patch("src.preprocessing.terminalbench.load_and_parse_artifact")
def test_missing_annotations(mock_load):
    # Test 5 - Missing annotations
    mock_load.return_value = []
    
    row = {
        "traj_id": "1",
        "solved": False,
        "incorrect_stages": None
    }
    ep, evs = normalize_tracebench_as_terminalbench(row, "sha")
    assert ep.onset_annotated is False
    assert ep.annotation_derived_onset_step is None

@patch("src.preprocessing.terminalbench.load_and_parse_artifact")
def test_step_alignment(mock_load):
    # Test 6 - Step alignment
    mock_load.return_value = [
        {"role": "user", "content": "prompt"},
        {"role": "assistant", "content": "action1"},
        {"role": "user", "content": "obs1"},
        {"role": "assistant", "content": "action2"},
        {"role": "user", "content": "obs2"}
    ]
    row = {
        "traj_id": "1",
        "solved": False,
        "incorrect_stages": [
            {
                "steps": [
                    {
                        "action_ref": {
                            "content": json.dumps({"role": "assistant", "content": "action1"})
                        }
                    }
                ]
            }
        ]
    }
    ep, evs = normalize_tracebench_as_terminalbench(row, "sha")

    assert ep.onset_annotated is True
    assert ep.annotation_derived_onset_step == 2
    
    # Step indices should be 1, 2, 3 (initial prompt, turn 1, turn 2)
    step_indices = [e.step_index for e in evs]
    assert step_indices == [1, 2, 3]
    assert len(set(step_indices)) == len(step_indices)  # no duplicated step indices
    
def test_prospective_leakage():
    # Test 7 - Prospective leakage
    from src.preprocessing.prefix_generator import compute_category_a_features
    from src.schemas.canonical import EventRecord
    
    events = [
        EventRecord(episode_id="1", step_index=1, actor_role="agent", action_type="message", tool_name=None, tool_status="ok", is_error=0),
        EventRecord(episode_id="1", step_index=2, actor_role="agent", action_type="message", tool_name=None, tool_status="ok", is_error=0)
    ]
    
    feat = compute_category_a_features([e for e in events if e.step_index <= 1], 1)
    assert feat["actor_role_agent"] == 1
    
    # The feature computation is completely independent of the onset_annotated field in the episode.

import pytest
from src.schemas.canonical import EpisodeRecord, EventRecord, PrefixRecord

def test_episode_record():
    ep = EpisodeRecord(
        dataset_id="terminalbench",
        dataset_version="04e8940f5b6736a7ce8d22224fe2f2af74163ed2",
        episode_id="test_ep_01",
        task_id="test_task_A",
        split="train",
        agent_model="gpt-4o",
        agent_scaffold="mini-swe-agent",
        total_steps=15,
        eventual_outcome=1,
        onset_annotated=True,
        annotation_derived_onset_step=5
    )
    d = ep.to_dict()
    assert d["dataset_id"] == "terminalbench"
    assert d["total_steps"] == 15
    assert d["eventual_outcome"] == 1
    assert d["annotation_derived_onset_step"] == 5

def test_prefix_record():
    pref = PrefixRecord(
        dataset_id="tracebench",
        episode_id="test_ep_02",
        task_id="test_task_B",
        split="eval_diagnostic",
        prefix_id="test_ep_02_p3",
        prefix_len=3,
        total_steps=20,
        eventual_outcome=0,
        onset_annotated=False,
        annotation_derived_onset_step=None,
        features={"steps_so_far": 3.0, "tool_error_count": 0.0}
    )
    d = pref.to_dict()
    assert d["prefix_id"] == "test_ep_02_p3"
    assert d["feat_steps_so_far"] == 3.0
    assert d["feat_tool_error_count"] == 0.0

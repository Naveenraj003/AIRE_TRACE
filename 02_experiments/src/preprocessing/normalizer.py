"""
AIRE-Trace Raw Dataset Normalizers Module
Normalizes TerminalBench, Tracebench, and tau-bench raw records into EpisodeRecord and EventRecords.
Applies strip_terminal_leakage() to every event.
"""

import json
import math
from typing import Dict, Any, List, Tuple, Optional
from src.schemas.canonical import EpisodeRecord, EventRecord
from src.preprocessing.sanitization import strip_terminal_leakage



def normalize_tau2_run(run: Dict[str, Any], idx: int, filename: str) -> Tuple[EpisodeRecord, List[EventRecord]]:
    """Normalizes a raw run entry from tau-bench historical trajectories."""
    task_id = str(run.get("task_id", f"task_{idx}"))
    episode_id = f"tau2_{filename}_{idx}"
    reward = run.get("reward", 0.0)

    eventual_outcome = 0 if (reward == 1.0 or reward == 1) else 1

    traj = run.get("traj", []) or run.get("messages", [])
    events: List[EventRecord] = []
    for s_idx, msg in enumerate(traj, start=1):
        clean_msg = strip_terminal_leakage(msg if isinstance(msg, dict) else {})
        role = clean_msg.get("role", "agent")
        actor_role = "agent" if role in ("assistant", "agent") else ("tool" if role == "tool" else "user")

        tool_calls = clean_msg.get("tool_calls", [])
        if tool_calls and isinstance(tool_calls, list):
            action_type = "tool_call"
            tool_name = str(tool_calls[0].get("name") or tool_calls[0].get("function", {}).get("name") or "")
        else:
            action_type = "message"
            tool_name = None

        events.append(EventRecord(
            episode_id=episode_id,
            step_index=s_idx,
            actor_role=actor_role,
            action_type=action_type,
            tool_name=tool_name,
            tool_status="ok",
            is_error=0
        ))

    total_steps = len(events)
    episode = EpisodeRecord(
        dataset_id="tau2",
        dataset_version=filename,
        episode_id=episode_id,
        task_id=task_id,
        split="eval_only",
        agent_model="gpt-4o_or_sonnet35",
        agent_scaffold="tau_bench_agent",
        total_steps=total_steps,
        eventual_outcome=eventual_outcome,
        onset_annotated=False,
        annotation_derived_onset_step=None,
        metadata_reference={"filename": filename}
    )
    return episode, events

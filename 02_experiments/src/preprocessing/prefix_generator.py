"""
AIRE-Trace Chronological Prefix Generator Module
Generates leakage-safe prefixes t = 1 ... min(T_i, K) and computes Category A baseline features.
"""

from typing import List, Dict, Any, Optional
from src.schemas.canonical import EpisodeRecord, EventRecord, PrefixRecord

def compute_category_a_features(visible_events: List[EventRecord], t: int) -> Dict[str, float]:
    """
    Computes baseline Category A common features strictly using events with step_index <= t.
    No future events, future statistics, or outcome fields are accessed.
    """
    if not visible_events:
        return {
            "steps_so_far": float(t),
            "actor_role_agent": 0.0,
            "actor_role_tool": 0.0,
            "actor_role_user": 0.0,
            "actor_role_system": 0.0,
            "action_type_message": 0.0,
            "action_type_tool_call": 0.0,
            "action_type_tool_result": 0.0,
            "tool_error_count": 0.0,
            "retry_count": 0.0,
            "unique_tools_used": 0.0,
            "tool_call_ratio": 0.0,
            "repeated_action_last2": 0.0
        }

    n_events = len(visible_events)
    agent_steps = sum(1 for e in visible_events if e.actor_role == "agent")
    tool_steps = sum(1 for e in visible_events if e.actor_role == "tool")
    user_steps = sum(1 for e in visible_events if e.actor_role == "user")
    system_steps = sum(1 for e in visible_events if e.actor_role == "system")

    msg_actions = sum(1 for e in visible_events if e.action_type == "message")
    tool_call_actions = sum(1 for e in visible_events if e.action_type == "tool_call")
    tool_res_actions = sum(1 for e in visible_events if e.action_type == "tool_result")

    error_events = sum(1 for e in visible_events if e.is_error == 1)

    # Retry count: consecutive error sequence or repeated failed calls
    retry_counter = 0
    consec_errors = 0
    for e in visible_events:
        if e.is_error == 1:
            consec_errors += 1
            if consec_errors > 1:
                retry_counter += 1
        else:
            consec_errors = 0

    unique_tools = len(set(e.tool_name for e in visible_events if e.tool_name))

    tool_call_ratio = float(tool_call_actions / n_events) if n_events > 0 else 0.0

    # Repeated action last 2
    repeated_last2 = 0
    if n_events >= 2:
        last_e = visible_events[-1]
        prev_e = visible_events[-2]
        if last_e.action_type == prev_e.action_type and (last_e.tool_name == prev_e.tool_name or last_e.tool_name is None):
            repeated_last2 = 1

    return {
        "steps_so_far": float(t),
        "actor_role_agent": float(agent_steps),
        "actor_role_tool": float(tool_steps),
        "actor_role_user": float(user_steps),
        "actor_role_system": float(system_steps),
        "action_type_message": float(msg_actions),
        "action_type_tool_call": float(tool_call_actions),
        "action_type_tool_result": float(tool_res_actions),
        "tool_error_count": float(error_events),
        "retry_count": float(retry_counter),
        "unique_tools_used": float(unique_tools),
        "tool_call_ratio": float(tool_call_ratio),
        "repeated_action_last2": float(repeated_last2)
    }


def generate_episode_prefixes(
    episode: EpisodeRecord,
    events: List[EventRecord],
    max_k: int = 30
) -> List[PrefixRecord]:
    """
    Generates prefix records for t = 1 ... min(T_i, max_k).
    No post-terminal padding.
    """
    T_i = episode.total_steps
    if T_i < 1:
        return []

    num_checkpoints = min(T_i, max_k)
    prefixes: List[PrefixRecord] = []

    # Sort events by step_index to guarantee strictly chronological order
    sorted_events = sorted(events, key=lambda e: e.step_index)

    for t in range(1, num_checkpoints + 1):
        visible = [e for e in sorted_events if e.step_index <= t]
        feat = compute_category_a_features(visible, t)

        prefix_id = f"{episode.episode_id}_p{t}"
        prefix_rec = PrefixRecord(
            dataset_id=episode.dataset_id,
            episode_id=episode.episode_id,
            task_id=episode.task_id,
            split=episode.split,
            prefix_id=prefix_id,
            prefix_len=t,
            total_steps=T_i,
            eventual_outcome=episode.eventual_outcome,
            onset_annotated=episode.onset_annotated,
            annotation_derived_onset_step=episode.annotation_derived_onset_step,
            features=feat,
            metadata_reference=episode.metadata_reference
        )
        prefixes.append(prefix_rec)

    return prefixes

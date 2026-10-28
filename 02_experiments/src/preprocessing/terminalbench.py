import os
import json
import tarfile
import zstandard as zstd
from typing import Dict, Any, List, Tuple, Optional
from huggingface_hub import hf_hub_download
from src.schemas.canonical import EpisodeRecord, EventRecord

def load_and_parse_artifact(hf_repo: str, artifact_path: str) -> Optional[List[Dict[str, Any]]]:
    if not artifact_path:
        return None
    try:
        local_path = hf_hub_download(repo_id=hf_repo, repo_type="dataset", filename=artifact_path, local_files_only=True)
    except Exception as e:
        print(f"Error downloading {artifact_path}: {e}")
        return None

    try:
        dctx = zstd.ZstdDecompressor()
        with open(local_path, 'rb') as ifh:
            with dctx.stream_reader(ifh) as reader:
                with tarfile.open(mode='r|', fileobj=reader) as tar:
                    for member in tar:
                        if member.name.endswith('agent-logs/mini.traj.json'):
                            f = tar.extractfile(member)
                            if f is not None:
                                data = json.load(f)
                                return data.get("messages", [])
                    return None
    except Exception as e:
        print(f"Error extracting {artifact_path}: {e}")
        return None

def normalize_tracebench_as_terminalbench(row: Dict[str, Any], commit_sha: str) -> Tuple[Optional[EpisodeRecord], List[EventRecord]]:
    traj_id = str(row.get("traj_id"))
    task_name = str(row.get("task_name", "unknown_task"))
    agent = str(row.get("agent", "unknown_agent"))
    model = str(row.get("model", "unknown_model"))
    solved = row.get("solved", False)
    
    eventual_outcome = 0 if solved is True else 1
    
    # Onset annotation extraction
    inc_stages = row.get("incorrect_stages", [])
    if isinstance(inc_stages, str):
        try:
            inc_stages = json.loads(inc_stages)
        except:
            inc_stages = []
            


    artifact_path = row.get("artifact_path")
    messages = load_and_parse_artifact("Contextbench/Tracebench", artifact_path)
    
    if messages is None:
        return None, []
        
    events = []
    
    msgs = [m for m in messages if m.get("role") != "system"]
    
    task_instruction = ""
    for m in msgs:
        if m.get("role") == "user":
            task_instruction = str(m.get("content", ""))
            break
            
    # Tracebench artifacts often start with a user message (the initial prompt).
    # This might not represent a "turn" that can fail or have a tool call.
    # However, to preserve chronological order, we can pair each assistant message
    # with its following user message (if any).
    # If the sequence starts with a user message, we can emit it as a separate turn,
    # or just treat each Agent Action as the start of a turn.
    
    current_step = 1
    idx = 0
    msg_idx_to_canonical = {}
    
    while idx < len(msgs):
        msg = msgs[idx]
        role = msg.get("role")
        msg_idx_to_canonical[idx] = current_step
        
        if role == "assistant":
            content = str(msg.get("content", ""))
            
            # Detect tool_call
            action_type = "message"
            tool_name = None
            if "```bash" in content or "```python" in content or "```sh" in content:
                action_type = "tool_call"
                import re
                match = re.search(r"```(?:bash|python|sh)\s*(.*?)```", content, re.DOTALL)
                if match:
                    code_block = match.group(1).strip()
                    tokens = code_block.split()
                    tool_name = tokens[0] if tokens else "terminal_cmd"
                else:
                    tool_name = "terminal_cmd"
                
            # Look ahead for user observation
            is_err = 0
            obs_content = ""
            
            next_idx = idx + 1
            if next_idx < len(msgs) and msgs[next_idx].get("role") == "user":
                obs_content = str(msgs[next_idx].get("content", ""))
                msg_idx_to_canonical[next_idx] = current_step
                
                if "<returncode>" in obs_content:
                    if "<returncode>0</returncode>" not in obs_content:
                        is_err = 1
                elif "error" in obs_content.lower() or "traceback" in obs_content.lower() or "failed" in obs_content.lower():
                    is_err = 1
                    
                idx = next_idx # Consume the observation
            
            events.append(EventRecord(
                episode_id=traj_id,
                step_index=current_step,
                actor_role="agent",
                action_type=action_type,
                tool_name=tool_name,
                tool_status="error" if is_err else "ok",
                is_error=is_err
            ))
            current_step += 1
            idx += 1
            
        elif role == "user":
            # Orphan user message (e.g. initial prompt)
            events.append(EventRecord(
                episode_id=traj_id,
                step_index=current_step,
                actor_role="user",
                action_type="message",
                tool_name=None,
                tool_status="ok",
                is_error=0
            ))
            current_step += 1
            idx += 1
            
        else:
            idx += 1

    total_steps = current_step - 1

    # Onset annotation mapping via reference chain
    onset_step = None
    onset_annotated = False
    
    if eventual_outcome == 1 and isinstance(inc_stages, list) and len(inc_stages) > 0:
        target_a_refs = []
        for st in inc_stages:
            if isinstance(st, dict):
                steps = st.get("steps", [])
                for step_obj in steps:
                    a_ref_obj = step_obj.get("action_ref")
                    if a_ref_obj is not None:
                        a_content = a_ref_obj.get("content", "")
                        if a_content:
                            target_a_refs.append(a_content)
                            
        canonical_onsets = []
        for a_content in target_a_refs:
            try:
                clean_content = a_content.strip().rstrip(",")
                target_dict = json.loads(clean_content)
            except:
                continue
                
            target_ts = target_dict.get("timestamp")
            matched_indices = []
            
            for i, m in enumerate(msgs):
                if target_ts is not None and m.get("timestamp") == target_ts:
                    matched_indices.append(i)
                elif target_ts is None:
                    if m.get("role") == target_dict.get("role") and m.get("content") == target_dict.get("content"):
                        matched_indices.append(i)
                        
            if len(matched_indices) == 1:
                raw_idx = matched_indices[0]
                canon_step = msg_idx_to_canonical.get(raw_idx)
                if canon_step is not None:
                    canonical_onsets.append(canon_step)
                    
        if canonical_onsets:
            onset_annotated = True
            onset_step = min(canonical_onsets)

    episode = EpisodeRecord(
        dataset_id="terminalbench",
        dataset_version=commit_sha,
        episode_id=traj_id,
        task_id=task_name,
        split="unassigned", # Set by task-group splitter
        agent_model=model,
        agent_scaffold=agent,
        total_steps=total_steps,
        eventual_outcome=eventual_outcome,
        onset_annotated=onset_annotated,
        annotation_derived_onset_step=onset_step,
        task_instruction=task_instruction,
        metadata_reference={
            "difficulty": row.get("difficulty"),
            "category": row.get("category"),
            "artifact_path": artifact_path
        }
    )
    return episode, events

"""
AIRE-Trace Canonical Schemas
Defines EpisodeRecord, EventRecord, and PrefixRecord.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List

@dataclass
class EpisodeRecord:
    dataset_id: str                          # "terminalbench" | "tracebench" | "tau2"
    dataset_version: str                     # HF commit SHA or repo version
    episode_id: str                          # Unique episode identifier
    task_id: str                             # Task name / task identifier for grouping
    split: str                               # "train" | "calibration" | "test" | "eval_only"
    agent_model: str                         # Underlying LLM model name
    agent_scaffold: str                      # Agent framework / scaffold name
    total_steps: int                         # Total trajectory length T_i
    eventual_outcome: int                    # 0 = success, 1 = failure (canonical mapping)
    onset_annotated: bool                    # True if step-level error annotation exists
    annotation_derived_onset_step: Optional[int] # min(incorrect_step_ids) or None
    task_instruction: str = ""               # Initial user prompt/task description
    metadata_reference: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EventRecord:
    episode_id: str
    step_index: int                          # 1-indexed step number
    actor_role: str                          # "agent" | "tool" | "user" | "system"
    action_type: str                         # "message" | "tool_call" | "tool_result" | "terminal"
    tool_name: Optional[str]
    tool_status: Optional[str]               # "ok" | "error" | None
    is_error: int                            # 1 if error/traceback occurred, else 0


@dataclass
class PrefixRecord:
    dataset_id: str
    episode_id: str
    task_id: str
    split: str
    prefix_id: str                           # e.g., "{episode_id}_p{t}"
    prefix_len: int                          # Checkpoint t (1 ... min(T_i, K))
    total_steps: int                         # T_i
    eventual_outcome: int                    # 0 = success, 1 = failure
    onset_annotated: bool                    # True if annotation-derived onset available
    annotation_derived_onset_step: Optional[int] # min(incorrect_step_ids) or None
    features: Dict[str, float]               # Category A common baseline features ONLY
    metadata_reference: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # Flatten features dict into top-level for tabular / parquet storage
        feat = d.pop("features")
        for fk, fv in feat.items():
            d[f"feat_{fk}"] = fv
        return d

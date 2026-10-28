"""
AIRE-Trace / prospective failure-warning project
Phase 1: dataset ingestion + unified trace schema + leakage-safe prefix generation

Run this LOCALLY (needs network + the two source repos/datasets).

Sources:
  - tau2-bench historical trajectories:
      git clone https://github.com/sierra-research/tau-bench
      -> ./historical_trajectories/{airline,retail}/*.json  (verify exact path after cloning)
  - TerminalBench trajectories (HuggingFace):
      pip install datasets
      from datasets import load_dataset
      ds = load_dataset("Contextbench/Tracebench", split="full")

IMPORTANT: field names below are best-effort from public docs/snippets, NOT confirmed
against the actual downloaded files. Run `inspect_raw()` first on a few files, compare
against the assumptions in `TAU2_FIELD_MAP` / `TB_FIELD_MAP`, and patch before trusting
the normalized output.

Canonical schema
-----------------
Run record:
  run_id, source, domain, task_id, agent_model,
  total_steps, final_outcome ("success"|"failure"), failure_onset_step (int|None)

Event record (one row per step, per run):
  run_id, step_index, actor ("agent"|"tool"|"user"|"env"),
  action_type ("message"|"tool_call"|"tool_result"|"terminal"),
  tool_name, tool_output_status ("ok"|"error"|None), latency_ms, retry_count, error_code

Prefix table (generated, not raw):
  run_id, prefix_len, label_eventual_failure (0/1), lead_time (int|None, only if label=1),
  feature_dict (JSON, computed ONLY from events with step_index <= prefix_len)
"""

import json
import csv
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any

MAX_PREFIXES_PER_RUN = 30  # cap for compute; sample evenly if trajectory is longer

# ---------------------------------------------------------------------------
# FROZEN EXPERIMENTAL PROTOCOL — hard correctness constraints, not defaults.
# Any change to these four rules must be a deliberate, documented protocol
# amendment, not a quiet code edit.
# ---------------------------------------------------------------------------
#
# R1 (checkpoints):     evaluate at t = 1, 2, ..., T (every step), capped at
#                        MAX_PREFIXES_PER_RUN via deterministic stride sampling
#                        for long trajectories. Selection must be fixed BEFORE
#                        any test results are examined.
#
# R2 (feature leakage): Features(t) may depend only on steps 1..t. This
#                        includes t = T: the terminal event, if it structurally
#                        encodes the final outcome (reward field, "task
#                        failed"-style content, explicit terminal action_type),
#                        must be stripped to a neutral placeholder BEFORE it
#                        enters the Event list — for every checkpoint,
#                        including the last one. final_outcome and
#                        failure_onset_step exist only as evaluation targets,
#                        never as features.
#
# R3 (split leakage):   splitting unit = episode (run_id), never prefix.
#                        Train / Calibration / Test are three disjoint sets of
#                        run_ids. No episode's prefixes may appear in more
#                        than one set.
#
# R4 (alert convention): an alert at checkpoint t is VALID iff
#                        t <= failure_onset_step. lead_time = failure_onset_step
#                        - t_first_valid_alert (>= 0; 0 means caught exactly at
#                        onset). Alerts with t > failure_onset_step are
#                        excluded from the lead-time distribution and reported
#                        separately as "late detections". Runs without a known
#                        failure_onset_step (e.g. tau2-bench) cannot contribute
#                        to lead-time analysis at all — report AUROC/AUPRC/
#                        calibration/FAR only for those.
# ---------------------------------------------------------------------------

TERMINAL_ACTION_TYPES = {"terminal"}
OUTCOME_LEAK_KEYS = {"reward", "success", "final_outcome", "task_failed", "task_success"}


def strip_terminal_leakage(raw_event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply R2 at ingestion time: neutralize any event whose action_type or
    content field-names structurally encode the final outcome. Call this on
    EVERY event dict before it is turned into an Event(), not just the last one
    (agents occasionally emit early self-assessment statements too).
    """
    cleaned = dict(raw_event)
    if cleaned.get("action_type") in TERMINAL_ACTION_TYPES:
        cleaned["action_type"] = "message"
        cleaned["content"] = "[terminal event redacted for leakage prevention]"
        for k in OUTCOME_LEAK_KEYS:
            cleaned.pop(k, None)
    else:
        for k in OUTCOME_LEAK_KEYS:
            cleaned.pop(k, None)
    return cleaned

# ---------------------------------------------------------------------------
# Step 0: inspect raw files before trusting any field mapping below
# ---------------------------------------------------------------------------

def inspect_raw(path: str, n_chars: int = 2000):
    """Print the first n_chars of a raw file so you can eyeball real field names."""
    p = Path(path)
    text = p.read_text(errors="replace")
    print(f"--- {path} (first {n_chars} chars) ---")
    print(text[:n_chars])


# ---------------------------------------------------------------------------
# Canonical data structures
# ---------------------------------------------------------------------------

@dataclass
class Run:
    run_id: str
    source: str          # "tau2" | "terminalbench"
    domain: str           # e.g. "airline", "retail", "terminal"
    task_id: str
    agent_model: str
    total_steps: int
    final_outcome: str    # "success" | "failure"
    failure_onset_step: Optional[int]  # None if success


@dataclass
class Event:
    run_id: str
    step_index: int
    actor: str
    action_type: str
    tool_name: Optional[str]
    tool_output_status: Optional[str]
    latency_ms: Optional[float]
    retry_count: int
    error_code: Optional[str]


# ---------------------------------------------------------------------------
# tau2-bench normalizer  --  ADJUST after inspect_raw() on a real file
# ---------------------------------------------------------------------------

def normalize_tau2_file(raw_path: str) -> (Run, List[Event]):
    """
    ASSUMPTION (verify with inspect_raw first):
    raw JSON looks roughly like:
    {
      "task_id": "...",
      "domain": "airline" | "retail",
      "agent_model": "...",
      "reward": 1 or 0,               # 1 = success
      "messages": [ {"role": "...", "tool_calls": [...], ...}, ... ]
    }
    """
    data = json.loads(Path(raw_path).read_text())

    task_id = data.get("task_id", Path(raw_path).stem)
    domain = data.get("domain", "unknown")
    agent_model = data.get("agent_model", data.get("model", "unknown"))
    reward = data.get("reward", None)
    final_outcome = "success" if reward == 1 else "failure"

    events: List[Event] = []
    retry_counter = 0
    for i, msg in enumerate(data.get("messages", [])):
        role = msg.get("role", "agent")
        actor = "agent" if role in ("assistant", "agent") else ("tool" if role == "tool" else "user")
        tool_calls = msg.get("tool_calls") or []
        if tool_calls:
            action_type = "tool_call"
            tool_name = tool_calls[0].get("name") or tool_calls[0].get("function", {}).get("name")
        else:
            action_type = "message"
            tool_name = None

        status = msg.get("status")  # ADJUST: field may not exist; infer from content/error keys instead
        if status == "error" or msg.get("error"):
            retry_counter += 1

        events.append(Event(
            run_id=task_id,
            step_index=i,
            actor=actor,
            action_type=action_type,
            tool_name=tool_name,
            tool_output_status=status,
            latency_ms=msg.get("latency_ms"),
            retry_count=retry_counter,
            error_code=msg.get("error_code"),
        ))

    total_steps = len(events)
    failure_onset_step = None
    if final_outcome == "failure":
        # ASSUMPTION: no ground-truth onset step exists in tau2-bench (it's outcome-only).
        # For the "eventual failure" label this is fine (we only need final_outcome).
        # Lead-time analysis will therefore only be computable for datasets with
        # step-level annotations (e.g. TerminalBench/Tracebench "incorrect_stages").
        # Flag this explicitly in the paper as a dataset limitation.
        failure_onset_step = None

    run = Run(
        run_id=task_id,
        source="tau2",
        domain=domain,
        task_id=task_id,
        agent_model=agent_model,
        total_steps=total_steps,
        final_outcome=final_outcome,
        failure_onset_step=failure_onset_step,
    )
    return run, events


# ---------------------------------------------------------------------------
# TerminalBench / Tracebench normalizer  --  ADJUST after inspect_raw()
# ---------------------------------------------------------------------------

def normalize_terminalbench_row(row: Dict[str, Any]) -> (Run, List[Event]):
    """
    ASSUMPTION (verify against real HF row):
    row = {
      "task_name": ..., "agent": ..., "model": ..., "reward": 0/1,
      "steps": "<json string>",              # list of {"src","msg","tools","obs"}
      "incorrect_stages": "<json string>",   # optional, Tracebench-specific
    }
    """
    steps = json.loads(row["steps"])
    reward = row.get("reward", 0)
    final_outcome = "success" if reward == 1 else "failure"

    events: List[Event] = []
    retry_counter = 0
    for i, s in enumerate(steps):
        actor = "agent" if s.get("src") == "agent" else "tool"
        tools = s.get("tools") or []
        if tools:
            action_type = "tool_call"
            tool_name = tools[0].get("fn")
        else:
            action_type = "message"
            tool_name = None
        obs = s.get("obs", "") or ""
        errored = "error" in obs.lower() or "traceback" in obs.lower()
        if errored:
            retry_counter += 1

        events.append(Event(
            run_id=row.get("task_name", "unknown") + "_" + str(row.get("model", "")),
            step_index=i,
            actor=actor,
            action_type=action_type,
            tool_name=tool_name,
            tool_output_status="error" if errored else "ok",
            latency_ms=None,   # ADJUST if timing is available in the real schema
            retry_count=retry_counter,
            error_code=None,
        ))

    total_steps = len(events)
    failure_onset_step = None
    if "incorrect_stages" in row and row["incorrect_stages"]:
        try:
            stages = json.loads(row["incorrect_stages"])
            if stages:
                failure_onset_step = min(stages)  # ADJUST: confirm this is a step index, not a name
        except Exception:
            pass

    run = Run(
        run_id=events[0].run_id if events else "unknown",
        source="terminalbench",
        domain="terminal",
        task_id=row.get("task_name", "unknown"),
        agent_model=str(row.get("model", "unknown")),
        total_steps=total_steps,
        final_outcome=final_outcome,
        failure_onset_step=failure_onset_step,
    )
    return run, events


# ---------------------------------------------------------------------------
# Leakage-safe prefix generation
# ---------------------------------------------------------------------------

def compute_features_up_to(events: List[Event], t: int) -> Dict[str, Any]:
    """Feature extraction using ONLY events with step_index <= t. This is the leakage boundary."""
    visible = [e for e in events if e.step_index <= t]
    tool_events = [e for e in visible if e.action_type == "tool_call"]
    error_events = [e for e in visible if e.tool_output_status == "error"]
    tools_used = set(e.tool_name for e in tool_events if e.tool_name)
    action_sequence = [e.action_type for e in visible]
    repeated_action = int(len(action_sequence) >= 2 and action_sequence[-1] == action_sequence[-2])

    return {
        "steps_so_far": len(visible),
        "retry_count": visible[-1].retry_count if visible else 0,
        "tool_error_count": len(error_events),
        "unique_tools": len(tools_used),
        "repeated_action_last2": repeated_action,
        "tool_call_ratio": (len(tool_events) / len(visible)) if visible else 0.0,
    }


def generate_prefixes(run: Run, events: List[Event]) -> List[Dict[str, Any]]:
    """
    One row per checkpoint t. label = whether the RUN eventually fails (known only
    from the final outcome, never from events beyond t). lead_time is only filled
    in when failure_onset_step is known (dataset-dependent, see normalizer notes).
    """
    T = run.total_steps
    if T < 1:
        return []

    # R1: t = 1..T (terminal event itself is neutralized by strip_terminal_leakage
    # at ingestion, so t=T is safe to include here).
    candidate_steps = list(range(1, T + 1))
    if len(candidate_steps) > MAX_PREFIXES_PER_RUN:
        stride = len(candidate_steps) // MAX_PREFIXES_PER_RUN
        candidate_steps = candidate_steps[::max(stride, 1)]
        if candidate_steps[-1] != T:
            candidate_steps.append(T)  # always keep the final checkpoint

    label = 1 if run.final_outcome == "failure" else 0
    rows = []
    for t in candidate_steps:
        features = compute_features_up_to(events, t)

        # R4: alert-timing convention
        lead_time = None
        alert_window = "n/a"  # "valid" | "late" | "n/a" (no onset label available)
        if label == 1 and run.failure_onset_step is not None:
            if t <= run.failure_onset_step:
                lead_time = run.failure_onset_step - t
                alert_window = "valid"
            else:
                alert_window = "late"

        rows.append({
            "run_id": run.run_id,
            "source": run.source,
            "domain": run.domain,
            "prefix_len": t,
            "total_steps": T,
            "label_eventual_failure": label,
            "lead_time_if_positive": lead_time,
            "alert_window": alert_window,
            **features,
        })
    return rows


# ---------------------------------------------------------------------------
# Driver (adjust paths once real data is downloaded)
# ---------------------------------------------------------------------------

def build_prefix_dataset(runs_and_events: List[tuple], out_csv: str):
    all_rows = []
    for run, events in runs_and_events:
        all_rows.extend(generate_prefixes(run, events))

    if not all_rows:
        print("No rows generated — check normalizers against real data first.")
        return

    fieldnames = list(all_rows[0].keys())
    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"Wrote {len(all_rows)} prefix rows from {len(runs_and_events)} runs -> {out_csv}")


# ---------------------------------------------------------------------------
# Enforced leakage guards — run these before every experiment, not just once.
# They must FAIL LOUDLY (raise), never warn-and-continue.
# ---------------------------------------------------------------------------

def assert_no_feature_leakage(prefix_rows: List[Dict[str, Any]]):
    """R2 check: no leaked keys anywhere in a prefix row's feature dict."""
    forbidden = {"final_outcome", "failure_onset_step", "reward"}
    for row in prefix_rows:
        leaked = forbidden.intersection(row.keys())
        assert not leaked, f"LEAKAGE: forbidden keys {leaked} present in prefix row for run {row.get('run_id')}"
        assert row["prefix_len"] <= row["total_steps"], (
            f"LEAKAGE: prefix_len {row['prefix_len']} exceeds total_steps {row['total_steps']} "
            f"for run {row.get('run_id')}"
        )
    print(f"[OK] R2 feature-leakage guard passed on {len(prefix_rows)} rows.")


def assert_no_split_leakage(train_ids: set, calib_ids: set, test_ids: set):
    """R3 check: episode-level disjointness across all three splits."""
    tc = train_ids & calib_ids
    tt = train_ids & test_ids
    ct = calib_ids & test_ids
    assert not tc, f"LEAKAGE: {len(tc)} run_ids in both train and calibration: {list(tc)[:5]}"
    assert not tt, f"LEAKAGE: {len(tt)} run_ids in both train and test: {list(tt)[:5]}"
    assert not ct, f"LEAKAGE: {len(ct)} run_ids in both calibration and test: {list(ct)[:5]}"
    print(f"[OK] R3 split-leakage guard passed: "
          f"{len(train_ids)} train / {len(calib_ids)} calib / {len(test_ids)} test episodes, all disjoint.")


def make_episode_disjoint_split(run_ids: List[str], train_frac=0.6, calib_frac=0.2, seed=42):
    """Deterministic episode-level split. Fix the seed and the split BEFORE looking at results."""
    import random
    rng = random.Random(seed)
    ids = sorted(set(run_ids))  # sort first so shuffle is reproducible regardless of input order
    rng.shuffle(ids)
    n = len(ids)
    n_train = int(n * train_frac)
    n_calib = int(n * calib_frac)
    train_ids = set(ids[:n_train])
    calib_ids = set(ids[n_train:n_train + n_calib])
    test_ids = set(ids[n_train + n_calib:])
    assert_no_split_leakage(train_ids, calib_ids, test_ids)
    return train_ids, calib_ids, test_ids


if __name__ == "__main__":
    print(__doc__)
    print("Next: run inspect_raw() on one real downloaded file from each source,")
    print("patch the two normalize_* functions to match the real fields (remember to")
    print("route every raw event through strip_terminal_leakage() first), then:")
    print("  1. build_prefix_dataset(...)")
    print("  2. assert_no_feature_leakage(rows)")
    print("  3. train_ids, calib_ids, test_ids = make_episode_disjoint_split([r['run_id'] for r in rows])")
    print("Only after all three pass do you touch a model.")

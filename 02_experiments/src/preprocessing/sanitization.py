"""
AIRE-Trace Terminal Event Sanitization Module
Enforces Protocol Rule 2 and Rule 6 invariants.
"""

from typing import Dict, Any

# Scalar keys that leak final task outcome or ground-truth evaluations
OUTCOME_LEAK_KEYS = {
    "reward", "success", "solved", "passed", "final_outcome",
    "status", "task_failed", "task_success", "incorrect_stages",
    "incorrect_error_stage_count"
}

# Action types that correspond to terminal submission or evaluation triggers
TERMINAL_ACTION_TYPES = {"terminal", "submit", "eval"}

def strip_terminal_leakage(raw_event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitizes trace events to guarantee Rule 2 & Rule 6 invariants.
    Neutralizes outcome-bearing content in terminal events and strips scalar outcome keys.
    Call this on EVERY event dictionary at ingestion time before turning it into an EventRecord.
    """
    cleaned = dict(raw_event)
    
    # 1. Neutralize action type if terminal
    action_type = cleaned.get("action_type")
    if action_type in TERMINAL_ACTION_TYPES:
        cleaned["action_type"] = "message"
        cleaned["content"] = "[TERMINAL EVENT REDACTED FOR LEAKAGE PREVENTION]"
        if "observation" in cleaned:
            cleaned["observation"] = "[TERMINAL OBSERVATION REDACTED]"
    
    # 2. Strip any embedded outcome keys
    for k in OUTCOME_LEAK_KEYS:
        cleaned.pop(k, None)
        
    return cleaned

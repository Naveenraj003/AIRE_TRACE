import pytest
from src.preprocessing.sanitization import strip_terminal_leakage

def test_strip_terminal_leakage_removes_outcome_keys():
    raw_event = {
        "action_type": "tool_call",
        "reward": 1.0,
        "solved": True,
        "passed": True,
        "status": "success",
        "incorrect_stages": [{"stage_id": 1}],
        "content": "Running git status"
    }
    cleaned = strip_terminal_leakage(raw_event)
    assert "reward" not in cleaned
    assert "solved" not in cleaned
    assert "passed" not in cleaned
    assert "status" not in cleaned
    assert "incorrect_stages" not in cleaned
    assert cleaned["content"] == "Running git status"

def test_strip_terminal_leakage_neutralizes_terminal_event():
    raw_event = {
        "action_type": "terminal",
        "content": "AssertionError: 1 != 0 in evaluation harness test",
        "observation": "FAILED (failures=1)"
    }
    cleaned = strip_terminal_leakage(raw_event)
    assert cleaned["action_type"] == "message"
    assert cleaned["content"] == "[TERMINAL EVENT REDACTED FOR LEAKAGE PREVENTION]"
    assert cleaned["observation"] == "[TERMINAL OBSERVATION REDACTED]"

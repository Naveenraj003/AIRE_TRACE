# AIRE-Trace Research Ideas & Open Questions

**New Log Format Mandate:** All new entries in this log MUST use the following format:

```markdown
## YYYY-MM-DD HH:MM — EVENT-ID

Type: IDEA 
Track: FUTURE-RESEARCH

### Event
What happened or what is the idea.

### Motivation
Why it was done or considered.

### Evidence
Exact file, command, artifact, test output, or user decision supporting the event.

### Decision
What was decided.

### Files Affected
Exact files changed, if any.

### Result
Observed result only.

### Scientific Impact
Whether the event affects: protocol, implementation, evaluation, statistics, demo only, documentation only.

### Status
PROPOSED | IN PROGRESS | COMPLETED | FROZEN | REJECTED | BLOCKED

### Next Action
The next concrete action, if any.
```

---

## Existing Open Questions (Transferred from OPEN_RESEARCH_QUESTIONS.md)

1. **Full Form of AIRE-Trace:** What does the acronym AIRE-Trace stand for? [UNKNOWN — REQUIRES HUMAN DECISION]
2. **TerminalBench Dataset Volume:** Does TerminalBench contain a sufficient number of episodes to reliably support a true three-way TRAIN/CALIBRATION/TEST split? -> **RESOLVED (VERIFIED)**
3. **Tracebench Onset Semantics:** What is the operational definition of failure onset represented by Tracebench's `incorrect_stages`? -> **RESOLVED (VERIFIED)**
4. **Checkpoint Horizon Dependency:** Does a fixed absolute checkpoint horizon create a dataset-dependent observation-window bias? -> **RESOLVED (VERIFIED)**
5. **Feature Overlap:** What exact trace features are legitimately computable on *both* datasets without leakage? -> **RESOLVED (VERIFIED)**
6. **Hardware Feasibility for L (LLM Monitor):** Can a local open-weight semantic monitor (L) run within the project's strict hardware budget? -> **RESOLVED (FROZEN/REJECTED DUE TO HARDWARE CONSTRAINT)**
49. 
50. ## Foundational Research Questions (Recovered from PROJECT_CONTROL.md)
51. 
52. *(Evidence level: LEVEL 1 — DIRECTLY OBSERVED. Recovered exactly from the original `PROJECT_CONTROL.md` artifact).*
53. 
54. - Do comparative performance claims for online agent-failure warning methods remain consistent when different methods are evaluated under identical information, target, alert, calibration, lead-time, and compute constraints?

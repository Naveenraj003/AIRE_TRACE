# AIRE-Trace Demo Plan

**New Log Format Mandate:** All new entries in this log MUST use the following format:

```markdown
## YYYY-MM-DD HH:MM — EVENT-ID

Type: IMPLEMENTATION | DECISION | IDEA | FUTURE-WORK
Track: LIVE-DEMO

### Event
What happened.

### Motivation
Why it was done or considered.

### Evidence
Exact file, command, artifact, test output, or user decision supporting the event.

### Decision
What was decided.

### Files Affected
Exact files changed, if any.

### Result
Observed result only. Do not convert assumptions into results.

### Scientific Impact
Whether the event affects: demo only, documentation only.

### Status
PROPOSED | IN PROGRESS | COMPLETED | FROZEN | REJECTED | BLOCKED

### Next Action
The next concrete action, if any.
```

---

## The Scientific Boundary (Demo vs. Research)

```text
CURRENT IEEE RESEARCH (TRACK A)
Offline evaluation of static, pre-recorded trajectories.

CURRENT FINAL-YEAR DEMO (TRACK B)
Dynamic visual replay of those recorded, already-evaluated trajectories.

FUTURE RUNTIME RESEARCH (TRACK C)
Actual agent execution and live monitoring of newly generated trajectories.
```

---

## 1. CURRENT FINAL-YEAR DEMO (Track B)

The current demo is defined as:
> A dynamic streaming/replay interface over real, already-evaluated AIRE-Trace episodes and their recorded prefix-level predictions.

The demo should allow an examiner to:
1. Select an actual evaluated episode from the frozen datasets.
2. Start playback.
3. Observe trajectory events/prefixes appearing progressively.
4. Observe the corresponding risk score update.
5. Observe the threshold crossing/warning at the actual evaluated point.
6. Observe the actual recorded outcome.
7. Compare warning timing against actual failure/outcome timing.
8. View the final episode-level summary.

**Requirements:**
- The UI MUST be dynamic/animated during playback.
- It MUST NOT merely display a static screenshot, static table, or manually typed fake prediction sequence.
- The replay MUST use existing verified evaluation artifacts (e.g. Parquet/JSON files) wherever possible.
- **Scientific constraint:** Do not generate new scientific results merely to support the demo. Do not alter frozen thresholds or evaluation semantics.

---

## 2. FUTURE RUNTIME DEMO (Track C - Future Work)

The future runtime concept is entirely separate from the current IEEE research and replay demo.

**Future Concept Flow:**
```text
USER ENTERS NEW SUPPORTED TASK
        ↓
ACTUAL AI AGENT EXECUTION
        ↓
CONTROLLED EXECUTION ENVIRONMENT
        ↓
LIVE TRAJECTORY
        ↓
LIVE PREFIX MONITORING
        ↓
RISK ESTIMATION
        ↓
WARNING
        ↓
OPTIONAL INTERVENTION
        ↓
FINAL OUTCOME
```

**Explicit Scientific Distinctions:**
- This is **NOT** the current IEEE experiment.
- This is **NOT** the source of current published metrics.
- It requires additional engineering (sandbox, live agents).
- It introduces new scientific questions.
- Arbitrary novel-task scoring may be out-of-distribution relative to current model training/calibration.
- It requires separate validation before risk scores can be scientifically interpreted.
- Runtime intervention and token/cost reduction are future research questions.
- **Do not implement this runtime system now.**

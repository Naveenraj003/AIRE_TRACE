# AIRE-Trace Future Work

**New Log Format Mandate:** All new entries in this log MUST use the following format:

```markdown
## YYYY-MM-DD HH:MM — EVENT-ID

Type: FUTURE-WORK
Track: FUTURE-RESEARCH | LIVE-DEMO

### Event
What happened or what is the future work direction.

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

## Validated Future Directions & Extensions

### Runtime AIRE-Trace
Prompt → agent → environment → live trace → warning → outcome.

### Controlled Agent Sandbox
Reproducible execution environment for dynamic agent tasks.

### Runtime Intervention
Warning → intervention policy → agent correction → continued execution.

### Token/Cost Analysis
Investigate whether early warning can reduce unnecessary tool calls, tokens, execution time or API cost.

### Additional Agent Families
Evaluate traces produced by additional agent architectures.

### Additional Datasets
Adapt new datasets to the canonical AIRE-Trace trace representation and evaluate them under the same protocol.

### Additional Warning Methods
Add new warning methods through the established evaluation interface where scientifically appropriate.

---

## Historical Roadmap (Superseded)

- **GATE 0 — Artifact understanding**: COMPLETE
- **GATE 1 — Data and experimental specification**: COMPLETE 
- **GATE 2 — Trace preprocessing and labeling**: COMPLETE
- **GATE 3 — Baseline implementation**: COMPLETE 
- **GATE 4 (Design) — AIRE-Trace implementation design freeze**: COMPLETE 
- **GATE 4 (Implementation) — AIRE-Trace Sequence Model Implementation**: COMPLETE
- **GATE 5 — Controlled experiments**: COMPLETE
- **GATE 6 — Failure analysis**: COMPLETE
- **GATE 7 — Ablation and robustness**: COMPLETE
- **GATE 8 — Reproducibility**: COMPLETE
- **GATE 9 — IEEE paper evidence**: COMPLETE
- **GATE 10 — Final-year demo/report/viva**: PLANNED (Track B)

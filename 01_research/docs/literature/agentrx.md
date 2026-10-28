# AgentRx (Feb 2026)

**Key Technical Feature:** Automated diagnostic framework for failure step localization
**Status:** Published
**Link:** [alphaxiv](https://www.alphaxiv.org/abs/2602.02475)

## Detailed Report

AI agents often fail in ways that are difficult to localize because executions are probabilistic, long-horizon, multi-agent, and mediated by noisy tool outputs. We address this gap by manually annotating failed agent runs and release a novel benchmark of 170 trajectories across 11 diverse task settings, including structured API workflows, incident management, and open-ended web/file tasks. Each trajectory is annotated with a critical failure step and a category from a grounded-theory derived, cross-domain failure taxonomy. To mitigate the human cost of failure attribution, we present AgentRx, an automated diagnostic framework that pinpoints the critical failure step in a failed agent trajectory. It synthesizes constraints, evaluates them step-by-step, and produces an auditable validation log of constraint violations with associated evidence; an LLM-based judge uses this log to localize the critical step and category. AgentRx improves step localization by 75% on average over prior work, while providing failure category attribution.

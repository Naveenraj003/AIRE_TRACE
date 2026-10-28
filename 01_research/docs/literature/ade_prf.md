# ADE-PRF: Agent Delivery Engineering Predictive Reliability Framework (July 2026)

**Category:** Related Technical Approaches — Monitoring
**arXiv:** [2607.07689](https://arxiv.org/abs/2607.07689)
**Published:** July 2026

---

## What the Paper Is

ADE-PRF is a **proactive health trajectory prediction framework** for long-horizon LLM multi-agent systems, aggregating 20 heterogeneous signals across 5 layers into a **Trust Margin (TM) metric**.

### Key Metrics and Results
- **Trust Margin (TM)**: 39.2-point dynamic range composite metric
- **Triple-method parallel prediction** for 8-hour forecasts:
  - Exponential method: MAE=1.228, Direction Accuracy=76.8%, 99.65% within ±10-point tolerance
  - Outperforms Kalman filter
- **Production validation**: 380,227 predictions and 280,579 validations across 6 agent profiles over 15 continuous days, plus 7 sandbox-controlled experiments
- Detects **"false prosperity"** — degradation concealed by normal surface metrics
- 16/20 factors rely on ADE-collected data (instrumentation requirement)

## What It Solves

- Long-horizon health forecasting (8-hour predictive window) for production LLM agents
- Detects false prosperity — systems that appear healthy on surface metrics while degrading internally
- Provides forward-looking warnings rather than retrospective failure detection

## What It Lacks

- Requires deep ADE plugin instrumentation (16/20 factors) — not observable from external telemetry alone
- The TM metric is a composite score; decomposition into individual failure modes is unclear
- Validated on 6 specific agent profiles — may not generalize
- 8-hour prediction window is appropriate for long-running production systems, not short episode-level detection
- No benchmark on standard agent datasets (TerminalBench, τ²-Bench)

## Relevance to AIRE-TRACE

- ADE-PRF operates at **system health level** (multi-day production trends); AIRE-TRACE operates at **episode level** (prefix-to-outcome within a single run) — different scales
- The "false prosperity" concept is relevant to our **sanitization invariant** (Rule 6): surface-level success signals may not reflect true episode health
- TM's multi-layer signal aggregation (5 layers) parallels our feature extraction from heterogeneous step telemetry
- 8-hour forecast horizon could complement AIRE-TRACE's episode-level alarms for production deployment
- Exponential method outperforming Kalman for health trajectory prediction is a useful calibration insight for time-series modeling choices

---

## Key Terms
`Trust Margin` · `health trajectory` · `predictive reliability` · `false prosperity` · `multi-agent systems` · `production monitoring`

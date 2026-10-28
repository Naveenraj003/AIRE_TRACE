# Patents Prior Art Summary

**Category:** Patents (Prior Art)

---

## US20260086538A1 — Detection and Prevention of Equipment Failure Using a Plurality of Agents

- **Priority:** July 2024
- **Published:** March 2026
- **Key Feature:** Multi-agent system for detecting and preventing equipment failures; uses multiple AI agents in parallel to improve fault detection coverage
- **Relevance to AIRE-TRACE:** Demonstrates prior art for multi-agent monitoring architectures. Our approach differs in targeting LLM software agents (not physical equipment) and focusing on trajectory-level monitoring rather than equipment sensor fusion.

---

## US20260200498A1 — Method and System for Addressing Failure in Autonomous Vehicles

- **Published:** July 2026
- **Key Feature:** Failure detection and response pipeline for autonomous vehicle agents; failure classification and fallback strategy selection
- **Relevance to AIRE-TRACE:** Domain-specific (autonomous vehicles) prior art. Establishes the patent landscape for failure-response in autonomous agent systems. Our work is in the LLM software agent space, which is not covered by this patent's claims.

---

## US20260220278A1 — Autonomous Agent Observation and Control System (Citibank)

- **Published:** July 2026
- **Status:** Active
- **Assignee:** Citibank
- **Key Feature:** Distributed observing platform for autonomous financial agents; real-time monitoring of agent state, action logging, intervention capability
- **Relevance to AIRE-TRACE:** Closest commercial prior art to our monitoring approach. Citibank's system targets financial domain agents; our system targets general-purpose LLM agents on open benchmarks. Key distinction: our monitors are lightweight (μs-scale) and trained from traces only; theirs is a full distributed observing infrastructure.

---

## Microsoft US2026/0148126 — Self-Updating AI Agent Node Networks

- **Filed:** November 2024
- **Published:** May 2026
- **Key Feature:** AI agent node networks that automatically update/reconfigure themselves after detecting failures — self-healing topology
- **Relevance to AIRE-TRACE:** Covers repair/reconfiguration layer, not detection. Our work focuses on the detection side (prefix monitoring, anomaly scoring). The repair strategy in RT Detection paper (rollback + re-run) is simpler and more empirically validated. This patent is relevant as prior art if AIRE-TRACE extends to automated repair recommendations.

---

## US12592897 — Detecting Anomalous Resource Distribution Patterns in AI Agent Networks

- **Granted:** March 2026
- **Key Feature:** System for detecting anomalous resource usage patterns (compute, memory, network) in networks of AI agents; feature-based anomaly detection on resource telemetry
- **Relevance to AIRE-TRACE:** Resource telemetry (token consumption, API call counts) is one feature class our monitors use. Our approach is broader (full step telemetry including tool outputs and state changes, not just resource metrics). This patent's granted status means we must ensure our resource-based features are not covered by its claims if we file IP.

---

## CN121071760B — Convergent Trajectory Feature Analysis for Time-Series Anomaly Detection (Chinese Patent)

- **Published:** November 2025
- **Key Feature:** Time-series anomaly detection using convergent trajectory feature analysis; models convergence patterns in sequential data to identify anomalies
- **Original Title:** 基于收敛轨迹特征分析的时序数据异常检测方法及系统
- **Relevance to AIRE-TRACE:** The "convergent trajectory" concept (modeling when a trajectory converges vs. diverges from expected patterns) is related to our echo-state-network's detection of prefix deviation. This is Chinese prior art — check during any future patent filing. Methodologically, convergent trajectory features could be added to our feature set.

---

## Summary Table

| Patent | Assignee | Domain | Key Distinction from AIRE-TRACE |
|--------|----------|--------|--------------------------------|
| US20260086538A1 | Unknown | Physical equipment | Multi-agent equipment sensors, not LLM traces |
| US20260200498A1 | Unknown | Autonomous vehicles | Domain-specific (vehicles), not software agents |
| US20260220278A1 | Citibank | Financial agents | Distributed observation platform, not lightweight monitors |
| US2026/0148126 | Microsoft | General AI agents | Self-repair/reconfiguration, not detection |
| US12592897 | Unknown | AI agent networks | Resource telemetry only, not full step telemetry |
| CN121071760B | Unknown | Time-series | Convergent trajectory features, Chinese jurisdiction |

# Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command-Line Environments (ICLR 2026)

**Category:** Benchmarks / Datasets
**arXiv:** [2601.11868](https://arxiv.org/abs/2601.11868)
**Published:** January 2026 (ICLR 2026)
**Website:** https://tbench.ai

---

## What the Paper Is

Terminal-Bench (TB) is a benchmark of **hard, realistic agentic tasks** in **command-line interface (CLI) environments**, designed to stress-test frontier AI agents beyond current benchmarks' difficulty level.

### Key Features
- **89 curated tasks** (v2.0/2.1) covering:
  - Software engineering
  - System administration
  - Data processing
  - Model training
  - Cybersecurity
- **Isolated Docker sandbox**: agents interact with a real shell
- **State-based verification**: success determined by automated inspection of files, processes, or exit codes — NOT text output matching
- **No reward hacking**: task completion requires genuine capability

### Version History
- v1.5: 74 tasks
- v2.0/2.1: 89 tasks with refined environments and verification suites

## What It Solves

- Addresses the saturation of existing benchmarks (WebArena, etc.) for frontier models
- Provides realistic, long-horizon tasks requiring actual system-level capabilities
- Automated verification eliminates ambiguity in success/failure labeling

## What It Lacks

- 89 tasks is still a relatively small dataset for training monitors — primarily a test/evaluation benchmark
- Tasks are CLI-domain-specific; generalization to API agents (like τ²-Bench) is indirect
- Reward hacking (Terminal Wrench paper) identified some residual issues even in v2.1

## Relevance to AIRE-TRACE

- **Primary benchmark dataset for AIRE-TRACE** (Mode A: TerminalBench evaluation)
- State-based verification provides clean, unambiguous `eventual_success`/`eventual_failure` labels — our Rule 10 (always route through canonical outcome mapping) is easy to implement here
- The Docker sandbox environment generates rich step telemetry (file operations, process states, exit codes) for our feature extraction
- Long-horizon tasks with genuine difficulty mean many failure episodes will have meaningful pre-onset prefixes — good for prefix monitor training
- **Important**: TerminalBench uses state verification, not LLM judge → ground truth is deterministic, not probabilistic
- PrefixGuard reported AUPRC 0.557 on TerminalBench — our protocol must beat this as a primary goal
- The 89-task scale requires careful attention to our episode-level split rules (Rule 3)

---

## Key Terms
`command-line interface` · `CLI` · `Docker sandbox` · `state verification` · `long-horizon tasks` · `ICLR 2026`

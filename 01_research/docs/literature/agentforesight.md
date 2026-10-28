# AgentForesight: Online Auditing for Early Failure Prediction in Multi-Agent Systems (May 2026)

**Category:** Failure Warning / Monitoring Systems
**arXiv:** [2605.08715](https://arxiv.org/abs/2605.08715)
**Published:** May 2026
**Project Page:** https://zbox1005.github.io/agent-foresight/

---

## What the Paper Is

AgentForesight reframes failure detection as **online auditing**: at each step of an unfolding trajectory, an auditor observes only the current prefix and must either **continue** or **alarm** at the earliest decisive error — without access to future steps.

### Key Contributions

1. **AFTraj-2K Dataset** — A corpus of agentic trajectories across Coding, Math, and Agentic domains:
   - Safe trajectories kept under strict curation
   - Unsafe trajectories annotated at the **step of decisive error** via consensus among multiple LLM judges
2. **AgentForesight-7B** — A compact (7B) online auditor trained with a two-stage **coarse-to-fine RL recipe**:
   - Stage 1: Risk-anticipation prior at failure boundary (adjacent safe/unsafe prefix pairs)
   - Stage 2: Sharpened into precise step-level localization under a **three-axis reward** (what, where, who of audit verdict)

### Results
- Outperforms GPT-4.1 and DeepSeek-V4-Pro on AFTraj-2K and external Who\&When benchmark
- **+19.9% performance gain** over leading proprietary models
- **3× lower step localization error**
- Transfers to external benchmark without retraining

## What It Solves

- Opens the loop from post-hoc failure detection → **deployment-time intervention**
- Creates a high-quality, step-annotated dataset (AFTraj-2K) for training online auditors
- Shows that a 7B fine-tuned model can surpass much larger proprietary models for this task

## What It Lacks

- Requires **fine-tuning a 7B model** — significant compute cost; not a lightweight monitor
- AFTraj-2K annotation relies on LLM judge consensus — may inherit LLM biases in failure attribution
- Does not provide calibrated false-alarm rate guarantees (statistical)
- Coverage is on Coding, Math, Agentic — does not include command-line/terminal environments (TerminalBench)

## Relevance to AIRE-TRACE

- **AgentForesight is a primary literature baseline** explicitly named in our protocol (Rule 7: never pool AgentForesight literature-reported numbers with locally measured AIRE-TRACE numbers)
- The AFTraj-2K dataset's annotation methodology (LLM judge consensus for decisive error step) is relevant for our Gate 1 ground truth inspection
- Three-axis reward (what, where, who) maps to our own evaluation dimensions: episode-level, step-level, and agent attribution
- Key contrast: AgentForesight uses a 7B fine-tuned LLM as the monitor; AIRE-TRACE uses an echo-state-network running in μs → different cost/latency profiles worth explicitly discussing
- Who\&When benchmark used for transfer is a useful external evaluation target for AIRE-TRACE as well

---

## Key Terms
`online auditing` · `coarse-to-fine RL` · `step localization` · `AFTraj-2K` · `decisive error step` · `multi-agent`

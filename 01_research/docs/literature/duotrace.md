# DUOTRACE (Aug 2026)

**Key Technical Feature:** VAE-based anomaly detection on agent trajectories with dual-view semantic-structural representations, Tree-LSTM encoder, prefix-chain augmentation
**Status:** Published
**Link:** [arxiv](https://arxiv.org/abs/2608.29646v1)

## Detailed Report

Large language model (LLM)-based agents have shown strong potential in solving complex tasks through multi-step reasoning, yet they remain vulnerable to execution failures. Accurate failure attribution is therefore critical for improving agent reliability. Existing topology- and spectrum-based methods exploit trajectory structures but often overlook fine-grained semantics, while LLM-based attribution methods capture semantic cues but suffer from long-context degradation over lengthy trajectories. To address these challenges, we propose DUOTRACE, a plug-and-play detection filter for LLM-based failure attribution. DUOTRACE follows a detect-before-attribute paradigm: it first detects anomalous executions and then supplies focused trajectory evidence to downstream LLM-based attribution methods. For effective VAE-based anomaly detection on agent trajectories, DUOTRACE integrates dual-view semantic-structural node representations, a Tree-LSTM-based trajectory encoder, and prefix-chain- and LLM-based data augmentation to handle heterogeneous nodes, hierarchical execution structures, and limited failure data. Experiments with six LLM-based attribution baselines show that DUOTRACE improves agent-level and step-level attribution accuracy by 8.7% and 7.0%, respectively.
